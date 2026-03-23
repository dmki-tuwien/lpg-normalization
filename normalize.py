import logging
import uuid
from typing import Any

from caseconverter import pascalcase, camelcase

from neo4j import Driver
from tqdm_loggable.auto import tqdm


from gnfd import DependencySet, GNFD, Node, Reference, Edge, GraphObject


def perform_graph_native_normalization(
    driver: Driver,
    database,
    provided_dependencies: DependencySet,
    dep_filter: str = "all",
) -> (DependencySet, list[str]):
    """
    Performs graph-native normalization under consideration of the provided parameters.

    :param driver: The connection to the graph database
    :type driver: neo4j.Driver
    :param database: The name of the database in which the to be normalized graph is contained. Supported databases are: ``"neo4j"`` and ``"memgraph"``
    :type: str
    :param provided_dependencies: The dependencies to be considered for the normalization
    :type: gnfd.DependencySet
    :param dep_filter: Whether only a subset of dependencies should be used. Possible values: ``"node-left"``, ``"edge-left"``, ``"within-node"``, ``"within-go"``, ``"between-go"``, ``"all"``. Defaults to ``"all"``.
    :type: str
    :return:
    """

    """A local copy of the provided dependencies that, e.g., may be filtered."""
    deps = provided_dependencies

    """A list of strings of queries that create indices"""
    index_queries: set[str] = set()
    """A list of strings of the queries that perform the transformations"""
    transformation_queries: set[str] = set()
    """A list of strings of the queries that remove properties"""
    remove_queries: set[str] = set()
    """A list of strings of the queries that delete graph objects"""
    delete_queries: set[str] = set()

    """The set of dependencies after all transformations have been applied."""
    transformed_deps: DependencySet
    """A list of the string representations of the transformed dependencies."""
    transformed_deps_list: list[str] = []

    applied_transformations: list[str] = []

    def _apply_transformation_query(query: str):
        """Runs a query string on the graph connected through :any:`driver`.

        :param query: The to be run query.
        :type query: str"""
        with driver.session(database=database) as session:
            session.run(query)

    def validate_dep(dep):
        """Validates whether a functional dependency holds"""
        if dep.is_trivial:
            return # The dependency is technically valid, although not minimal!

        with driver.session(database=database) as session:
            query = f"""
{dep.pattern.to_gql_match_where_string()}
WITH DISTINCT
{",".join(map(lambda ref: str(ref)+" AS "+pascalcase(str(ref)), dep.left.union(dep.right)))}
WITH
{",".join(map(lambda ref: pascalcase(str(ref)), dep.left))},
COUNT([{",".join(map(lambda ref: pascalcase(str(ref)), dep.right))}]) AS card
RETURN avg(card) AS res

"""
            res = session.run(query)
            record = res.single()
            if record is not None:
                if record["res"] != 1:
                    raise ValueError(f'The dependency "{str(dep)}" is not functional!')

    # Phase 0: Filter deps according to parameter from evaluation.
    logging.info("Filter dependencies")
    match dep_filter:
        case "within-node":
            deps = DependencySet(filter(lambda dep: dep.is_within_node, deps))
        case "within-go":
            deps = DependencySet(filter(lambda dep: dep.is_within_graph_object, deps))
        case "between-go":
            deps = DependencySet(filter(lambda dep: dep.is_inter_graph_object, deps))
        case "node-left":
            deps = DependencySet(
                filter(
                    lambda dep: dep.is_within_node
                    or isinstance(next(iter(dep.left)).get_graph_object(), Node),
                    deps,
                )
            )
        case "edge-left":
            deps = DependencySet(
                filter(
                    lambda dep: isinstance(
                        next(iter(dep.left)).get_graph_object(), Edge
                    ),
                    deps,
                )
            )

    if len(deps) == 0:
        return (
            provided_dependencies,
            applied_transformations,
        )  # Nothing will happen --> Return original dependencies

    i = 0

    for dep in deps:
        validate_dep(dep)

        if dep.is_inter_graph_object:
            inter_dep = dep
            left_gos: set[GraphObject] = set(
                map(lambda ref: ref.get_graph_object(), dep.left)
            )

            if len(left_gos) == 1:  # Multiple GOs are not supported for the left side
                left_go = left_gos.pop()
                if isinstance(left_go, Edge):
                    edge = left_go
                    for right_ref in dep.right:
                        left_references: set[Reference] = set(
                            filter(lambda ref: ref.is_property_variable, dep.left)
                        )

                        if (
                            right_ref.is_property_variable
                            and len(left_references) > 0
                            and isinstance(right_ref.get_graph_object(), Node)
                            and (
                                right_ref.get_graph_object() is left_go.src
                                or right_ref.get_graph_object() is left_go.tgt
                            )
                        ):
                            logging.info("between-ep-np")
                            assert isinstance(right_ref.get_graph_object(), Node)

                            merge_key_elements = list(
                                map(str, left_references.union({right_ref}))
                            )
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_references.union({right_ref}))
                            new_props.sort(key=str)
                            new_label: str = pascalcase(within_merge_key)

                            index_queries.add(
                                f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                            )

                            orig_edge_label = next(iter(left_go.labels))
                            index_queries.add(
                                f"CREATE INDEX IF NOT EXISTS FOR (xi:{orig_edge_label}) ON (xi.{", xi.".join(left_go.properties)})"
                            )
                            index_queries.add(
                                f"CREATE INDEX IF NOT EXISTS FOR ()-[e:{orig_edge_label}]-() ON (e.{", e.".join(left_go.properties)})"
                            )
                            if len(left_go.src.properties) > 0:
                                index_queries.add(
                                    f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(left_go.src.labels)}) ON (n.{", n.".join(left_go.src.properties)})"
                                )
                            if len(left_go.tgt.properties) > 0:
                                index_queries.add(
                                    f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(left_go.tgt.labels)}) ON (n.{", n.".join(left_go.tgt.properties)})"
                                )

                            new_properties: str = ", ".join(
                                map(
                                    lambda ref: f"{pascalcase(ref)} : {ref}",
                                    map(str, new_props),
                                )
                            )

                            reify_and_extract_to_new_node(
                                edge,
                                i,
                                dep,
                                new_label,
                                new_properties,
                                new_props,
                                transformation_queries,
                            )
                            rand = str(uuid.uuid4())[:8]
                            node = right_ref.get_graph_object()

                            index_queries.add(
                                f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(node.labels)}) ON (n.`{rand}`)"
                            )

                            index_queries.add(
f"""
{dep.pattern.to_gql_match_where_string()} 
WITH DISTINCT {node.symbol}
SET {node.symbol}.`{rand}`="{rand}"
"""
                            )
                            # Remove old redundant properties in the end
                            cleanup_pattern = (
                                inter_dep.pattern.to_gql_match_where_string().split(
                                    "WHERE"
                                )[0]
                            )
                            remove_queries.add(
    f"""
{cleanup_pattern} 
WHERE {node.symbol}.`{rand}`="{rand}"
WITH DISTINCT {node.symbol}
REMOVE {right_ref}
REMOVE {node.symbol}.`{rand}`
"""
                            )


                            delete_queries.add(
                                f"""
MATCH ({"".join(map(lambda lab: f":{lab}", edge.src.labels))})-[{edge.symbol}{"".join(map(lambda lab: f":{lab}", edge.labels))}]->({"".join(map(lambda lab: f":{lab}", edge.tgt.labels))})
WITH DISTINCT {edge.symbol}
DELETE {edge.symbol}"""
                            )


                            remove_queries.add(
                                f"""
MATCH ({edge.symbol}) - [:{new_label.upper()}]->(x{i})
REMOVE {", ".join(map(str, left_references))}"""
                            )  # Connect normalized nodes with reified nodes and remove redundant properties

                            transformed_deps_list.append(
                                f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, left_references.union({right_ref}))))})
::
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left_references)))}
=>x{i}""".replace(
                                    " ", ""
                                ).replace(
                                    "\n", ""
                                )
                            )

                            applied_transformations.append("between-ep-np")

                        elif (
                            right_ref.is_graph_object_variable
                            and len(left_references) > 0
                            and isinstance(right_ref.get_graph_object(), Node)
                            and (
                                right_ref.get_graph_object() is left_go.src
                                or right_ref.get_graph_object() is left_go.tgt
                            )
                        ):
                            logging.info("between-ep-n")

                            merge_key_elements = list(map(str, left_references))
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_references)
                            new_props.sort(key=str)
                            new_label: str = pascalcase(within_merge_key)


                            index_queries.add(
                                f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                            )

                            orig_edge_label = next(iter(left_go.labels))
                            index_queries.add(
                                f"CREATE INDEX IF NOT EXISTS FOR (n:{orig_edge_label}) ON (n.{", n.".join(left_go.properties)})"
                            )
                            index_queries.add(
                                f"CREATE INDEX IF NOT EXISTS FOR ()-[e:{orig_edge_label}]-() ON (e.{", e.".join(left_go.properties)})"
                            )
                            if len(left_go.src.properties) > 0:
                                index_queries.add(
                                    f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(left_go.src.labels)}) ON (n.{", n.".join(left_go.src.properties)})"
                                )
                            if len(left_go.tgt.properties) > 0:
                                index_queries.add(
                                    f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(left_go.tgt.labels)}) ON (n.{", n.".join(left_go.tgt.properties)})"
                                )

                            new_properties: str = ", ".join(
                                map(
                                    lambda ref: f"{pascalcase(ref)} : {ref}",
                                    map(str, new_props),
                                )
                            )

                            reify_and_extract_to_new_node(
                                edge,
                                i,
                                dep,
                                new_label,
                                new_properties,
                                new_props,
                                transformation_queries,
                            )

                            delete_queries.add(
                                f"""
MATCH ({"".join(map(lambda lab: f":{lab}", edge.src.labels))})-[{edge.symbol}{"".join(map(lambda lab: f":{lab}", edge.labels))}]->({"".join(map(lambda lab: f":{lab}", edge.tgt.labels))})
WITH DISTINCT {edge.symbol}
DELETE {edge.symbol}"""
                            )

                            remove_queries.add(
                                f"""
MATCH ({edge.symbol})-[:{new_label.upper()}]->(x{i})
WITH DISTINCT {edge.symbol}
REMOVE {", ".join(map(str, left_references))}"""
                            )  # Connect normalized nodes with reified nodes and remove redundant properties

                            transformed_deps_list.append(
                                f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, left_references.union({right_ref}))))})
::
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left_references)))}
=>x{i}""".replace(
                                    " ", ""
                                ).replace(
                                    "\n", ""
                                )
                            )
                            applied_transformations.append("between-ep-n")

                elif isinstance(left_go, Node):
                    node = left_go
                    for right_ref in inter_dep.right:
                        left_is_go = (
                            len(
                                set(
                                    filter(
                                        lambda ref: "." not in str(ref), inter_dep.left
                                    )
                                )
                            )
                            > 0
                        )
                        left_references: set[Reference] = set(
                            filter(lambda ref: "." in str(ref), inter_dep.left)
                        )

                        if (
                            "." in str(right_ref)
                            and left_is_go
                            and isinstance(right_ref.get_graph_object(), Edge)
                            and (
                                right_ref.get_graph_object().src is node
                                or right_ref.get_graph_object().tgt is node
                            )
                        ):
                            logging.info("between-n-ep")

                            edge = right_ref.get_graph_object()
                            assert isinstance(edge, Edge)

                            transformation_queries.add(
                                f"""
{inter_dep.pattern.to_gql_match_where_string()}
WITH DISTINCT {left_go.symbol}, {right_ref} AS {camelcase(str(right_ref))}
SET {left_go.symbol}.{pascalcase(str(right_ref))} = {camelcase(str(right_ref))}"""
                            )
                            remove_queries.add(
                                f"""
{inter_dep.pattern.to_gql_match_where_string()}
WITH DISTINCT {edge.symbol}
REMOVE {right_ref}"""
                            )
                            node.properties.add(pascalcase(str(right_ref)))
                            right_ref.get_graph_object().properties.remove(
                                str(right_ref).split(".")[1]
                            )
                            transformed_deps_list.append(
                                f"({node.symbol}:{"&".join(node.labels)}:{pascalcase(str(right_ref))})::{node.symbol}=>{node.symbol}.{pascalcase(str(right_ref))}"
                            )
                            applied_transformations.append("between-n-ep")

                        elif (
                            right_ref.is_property_variable
                            and not left_is_go
                            and isinstance(right_ref.get_graph_object(), Edge)
                            and (
                                right_ref.get_graph_object().src is node
                                or right_ref.get_graph_object().tgt is node
                            )
                        ):
                            logging.info("between-np-ep")

                            merge_key_elements = list(
                                map(str, left_references.union({right_ref}))
                            )
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_references.union({right_ref}))
                            new_props.sort(key=str)
                            new_label: str = pascalcase(within_merge_key)

                            index_queries.add(
                                f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                            )

                            new_properties: str = ", ".join(
                                map(
                                    lambda ref: f"{pascalcase(ref)} : {ref}",
                                    map(str, new_props),
                                )
                            )

                            rand = str(uuid.uuid4())[:8]
                            index_queries.add(
                                f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(node.labels)}) ON (n.`{rand}`)"
                            )


                            transformation_queries.add(
                                f"""
                            {dep.pattern.to_gql_match_where_string()} 
MERGE (newNode:{new_label} {{{new_properties}}})
MERGE ({node.symbol})-[:{new_label.upper()}]->(newNode)
WITH DISTINCT {node.symbol}
SET {node.symbol}.`{rand}`="{rand}"
"""
                            )

                            # Remove old redundant properties in the end
                            cleanup_pattern = (
                                inter_dep.pattern.to_gql_match_where_string().split(
                                    "WHERE"
                                )[0]
                            )
                            remove_queries.add(
                                f"""
{cleanup_pattern} 
WHERE {node.symbol}.`{rand}`="{rand}"
REMOVE {", ".join(map(str, left_references.union({right_ref})))}
WITH DISTINCT {node.symbol}
REMOVE {node.symbol}.`{rand}`
"""
                            )

                            right_ref.get_graph_object().properties -= {right_ref}
                            node.properties -= left_references

                            transformed_deps_list.append(
                                f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, left_references.union({right_ref}))))})
::
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left_references)))}
=>x{i}""".replace(
                                    " ", ""
                                ).replace(
                                    "\n", ""
                                )
                            )

                            applied_transformations.append("between-np-ep")

        elif dep.is_within_graph_object:
            # First filter References that are Graph Object IDs. We don't need them here as their occurrence is a sign for structurally implied or to limiting dep.s.
            left_references: set[Reference] = set(
                filter(lambda ref: ref.is_property_variable, dep.left)
            )
            right_references: set[Reference] = set(
                filter(lambda ref: ref.is_property_variable, dep.right)
            )
            all_references: set[Reference] = left_references.union(right_references)

            merge_key_elements = list(map(str, all_references))
            merge_key_elements.sort()
            within_merge_key: str = ",".join(merge_key_elements)
            new_props = list(right_references.union(left_references))
            new_props.sort(key=str)
            new_label: str = pascalcase(within_merge_key)

            i += 1

            # # # # # # # # # #
            #  ψ_L1 (psi_L1)  #
            # # # # # # # # # #
            if (
                dep.is_within_node
                and len(left_references) > 0
                and len(right_references) > 0
            ):
                logging.info("within-n")
                node: Node = dep.right.pop().get_graph_object()

                index_queries.add(
                    f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                )

                new_properties: str = ", ".join(
                    map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
                )

                rand = str(uuid.uuid4())[:8]
                index_queries.add(
                    f"CREATE INDEX IF NOT EXISTS FOR (n:{next(iter(node.labels))}) ON (n.`{rand}`)"
                ) # Neo4J only supports _single labels_ in indices!

                transformation_queries.add(
                    f"""
{dep.pattern.to_gql_match_where_string()} 
MERGE (newNode:{new_label} {{{new_properties}}})
MERGE ({node.symbol})-[:{new_label.upper()}]->(newNode)
WITH DISTINCT {node.symbol}
SET {node.symbol}.`{rand}`="{rand}"
"""
                )

                # Remove old redundant properties in the end
                cleanup_pattern = dep.pattern.to_gql_match_where_string().split(
                    "WHERE"
                )[0]
                remove_queries.add(
                    f"""
{cleanup_pattern} 
WITH DISTINCT {node.symbol}
WHERE {node.symbol}.`{rand}`="{rand}"
REMOVE {node.symbol}.`{rand}`
REMOVE {", ".join(map(str, right_references.union(left_references)))}
"""
                )

                dep.pattern.properties -= all_references

                transformed_deps_list.append(
                    f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, right_references.union(left_references))))})
::
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left_references)))}
=>x{i}""".replace(
                        " ", ""
                    ).replace(
                        "\n", ""
                    )
                )

                applied_transformations.append("within-n")

            # # # # # # # # # #
            #  ψ_L2 (psi_L2)  #
            # # # # # # # # # #
            elif (
                dep.is_within_edge
                and len(left_references) > 0
                and len(right_references) > 0
            ):  # ψ_L2 (psi_L2)  --> Reification
                logging.info("Within e")

                edge: Edge = dep.right.pop().get_graph_object()

                index_queries.add(
                    f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                )

                orig_edge_label = next(iter(edge.labels))
                index_queries.add(
                    f"CREATE INDEX IF NOT EXISTS FOR (n:{orig_edge_label}) ON (n.{", n.".join(edge.properties)})"
                )
                index_queries.add(
                    f"CREATE INDEX IF NOT EXISTS FOR ()-[e:{orig_edge_label}]-() ON (e.{", e.".join(edge.properties)})"
                )
                if len(edge.src.properties) > 0:
                    index_queries.add(
                        f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(edge.src.labels)}) ON (n.{", n.".join(edge.src.properties)})"
                    )
                if len(edge.tgt.properties) > 0:
                    index_queries.add(
                        f"CREATE INDEX IF NOT EXISTS FOR (n:{":".join(edge.tgt.labels)}) ON (n.{", n.".join(edge.tgt.properties)})"
                    )

                new_properties: str = ", ".join(
                    map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
                )

                # Reification + create new node
                reify_and_extract_to_new_node(
                    edge,
                    i,
                    dep,
                    new_label,
                    new_properties,
                    new_props,
                    transformation_queries,
                )

                delete_queries.add(
                    f"""
MATCH ({"".join(map(lambda lab: f":{lab}", edge.src.labels))})-[{edge.symbol}{"".join(map(lambda lab: f":{lab}", edge.labels))}]->({"".join(map(lambda lab: f":{lab}", edge.tgt.labels))})
REMOVE {", ".join(map(str, all_references))}
WITH DISTINCT {edge.symbol}
DELETE {edge.symbol}"""
                )

                remove_queries.add(
                    f"""
MATCH ({edge.symbol})-[:{new_label.upper()}]->(x{i})
WITH DISTINCT {edge.symbol}
REMOVE {", ".join(map(str, all_references))}"""
                )  # Connect normalized nodes with reified nodes and remove redundant properties

                transformed_deps_list.append(
                    f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, right_references.union(left_references))))})
::
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left_references)))}
=>x{i}""".replace(
                        " ", ""
                    ).replace(
                        "\n", ""
                    )
                )

                applied_transformations.append("within-e")

        i += 1
    if database == "neo4j":
        for query in tqdm(index_queries, desc="  Indices"):
            _apply_transformation_query(query)
    for query in tqdm(transformation_queries, desc="  Query"):
        _apply_transformation_query(query)
    for query in tqdm(remove_queries, desc="  Cleanup (REMOVE)"):
        _apply_transformation_query(query)
    for query in tqdm(delete_queries, desc="  Cleanup (DELETE)"):
        _apply_transformation_query(query)

    transformed_deps = DependencySet.from_string_list(transformed_deps_list)

    return transformed_deps, applied_transformations


def reify_and_extract_to_new_node(
    edge: Edge,
    i: int | Any,
    inter_dep: GNFD,
    new_label: str,
    new_properties: str,
    new_props: list[Reference],
    transformation_queries: set[str],
):
    edge_label = next(iter(edge.labels))

    # the "naive" way of encoding it
    transformation_queries.add(
        f"""
    {inter_dep.pattern.to_gql_match_where_string()} 
    CREATE (x{i}:{edge_label})
    CREATE ({edge.src.symbol})-[:SRC_{edge_label}]->(x{i})
    CREATE (x{i})-[:TGT_{edge_label}]->({edge.tgt.symbol})
    MERGE (newNode:{new_label} {{{new_properties}}})
    MERGE (x{i})-[:{new_label.upper()}]->(newNode)
    ON CREATE SET x{i} += properties({edge.symbol})
"""
    ) # Reification may have already happened for another dep. --> Merge!

    print(        f"""
    {inter_dep.pattern.to_gql_match_where_string()} 
    CREATE (x{i}:$(type({edge.symbol})))
    CREATE ({edge.src.symbol})-[:$("SRC_"+type({edge.symbol}))]->(x{i})
    CREATE (x{i})-[:$("TGT_"+type({edge.symbol}))]->({edge.tgt.symbol})
    MERGE (newNode:{new_label} {{{new_properties}}})
    MERGE (x{i})-[:{new_label.upper()}]->(newNode)
    ON CREATE SET x{i} += properties({edge.symbol})
""")
