import logging
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
) -> (DependencySet, list[tuple[str, int]]):
    """
    Performs graph-native normalization under consideration of the provided parameters.

    :param driver: The connection to the graph database
    :type driver: neo4j.Driver
    :param database: The name of the database in which the to be normalized graph is contained. Supported databases are: ``"neo4j"`` and ``"memgraph"``
    :type: str
    :param provided_dependencies: The dependencies to be considered for the normalization
    :type: gnfd.DependencySet
    :param dep_filter: Whether only a subset of dependencies should be used. Possible values: ``"within-node"``, ``"within-go"``, ``"between-go"``, ``"all"``. Defaults to ``"all"``.
    :type: str
    :return:
    """

    """A local copy of the provided dependencies that, e.g., may be filtered."""
    deps = provided_dependencies


    """A list of strings of queries that create indices"""
    index_queries: set[str] = set()
    """A list of strings of the queries that perform the transformations"""
    transformation_queries: set[str] = set()
    """A list of strings of the queries that """
    cleanup_queries: set[str] = set()

    """The set of dependencies after all transformations have been applied."""
    transformed_deps: DependencySet
    """A list of the string representations of the transformed dependencies."""
    transformed_deps_list: list[str] = []

    applied_transformations: list[tuple[str, int]] = []

    def _apply_transformation_query(query: str):
        """Runs a query string on the graph connected through :any:`driver`.

        :param query: The to be run query.
        :type query: str"""
        with driver.session(database=database) as session:
            session.run(query)

    def validate_dep(dep):
        """Validates whether a functional dependency holds"""
        with driver.session(database=database) as session:
            query = f"""
{dep.pattern.to_gql_match_where_string()}
WITH DISTINCT
{",".join(map(lambda ref: str(ref)+" AS "+camelcase(str(ref)), dep.left.union(dep.right)))}
WITH
{",".join(map(lambda ref: camelcase(str(ref)), dep.left))},
COUNT([{",".join(map(lambda ref: camelcase(str(ref)), dep.right))}]) AS card
RETURN avg(card) AS res

"""
            res = session.run(query)
            record = res.single()
            if record is not None:
                if record["res"] != 1:
                    raise ValueError(f"The dependency \"{str(dep)}\" is not functional!")


    # Phase 0: Filter deps according to parameter from evaluation.
    logging.info("Filter dependencies")
    match dep_filter:
        case "within-node":
            deps = DependencySet(filter(lambda dep: dep.is_within_node, deps))
        case "within-go":
            deps = DependencySet(filter(lambda dep: dep.is_within_graph_object, deps))
        case "between-go":
            deps = DependencySet(filter(lambda dep: dep.is_inter_graph_object, deps))

    if len(deps) == 0:
        return (
            provided_dependencies,
            applied_transformations,
        )  # Return original dependencies


    i = 0

    for dep in deps:
        validate_dep(dep)

        if dep.is_inter_graph_object:
            inter_dep = dep
            left_gos: set[GraphObject] = set(
                map(lambda ref: ref.get_graph_object(), inter_dep.left)
            )

            if (
                len(left_gos) == 1
            ):  # Multiple GOs are not supported for the left side
                left_go = left_gos.pop()
                if isinstance(left_go, Edge):
                    edge = left_go
                    for right_ref in inter_dep.right:
                        left_references: set[Reference] = set(
                            filter(lambda ref: ref.is_property_variable, inter_dep.left)
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
                            logging.info("Ep -> Np")

                            merge_key_elements = list(map(str, left_references.union({right_ref})))
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_references.union({right_ref}))
                            new_props.sort(key=str)
                            new_properties: str = ", ".join(
                                map(
                                    lambda ref: f"{pascalcase(ref)} : {ref}",
                                    map(str, new_props),
                                )
                            )
                            new_label: str = pascalcase(within_merge_key)

                            index_queries.add(
                                f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                            )

                            new_properties: str = ", ".join(
                                map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
                            )

                            reify_and_extract_to_new_node(edge, i, dep, new_label, new_properties, new_props,
                                                          transformation_queries)

                            cleanup_queries.add(
                                f"""
{inter_dep.pattern.to_gql_match_where_string()}
DELETE {edge.symbol}
                            """
                            )


                            right_ref_label_delim = (
                                ":" if len(right_ref.get_graph_object().labels) > 0 else ""
                            )
                            cleanup_queries.add(
                                f"""
MATCH ({right_ref.get_graph_object().symbol}{right_ref_label_delim}{"&".join(right_ref.get_graph_object().labels)})
REMOVE {right_ref}"""
                            )  # Connect normalized nodes with reified nodes and remove redundant properties

                            cleanup_queries.add(
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

                            applied_transformations.append(("inter1", 2))
                        # if its no Node its more than one hop for sure

                        elif (
                            right_ref.is_graph_object_variable
                            and len(left_references) > 0
                            and isinstance(right_ref.get_graph_object(), Node)
                            and (
                                right_ref.get_graph_object() is left_go.src
                                or right_ref.get_graph_object() is left_go.tgt
                            )
                        ):
                            logging.info("Ep -> N")

                            merge_key_elements = list(map(str, left_references))
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_references)
                            new_props.sort(key=str)
                            new_properties: str = ", ".join(
                                map(
                                    lambda ref: f"{pascalcase(ref)} : {ref}",
                                    map(str, new_props),
                                )
                            )
                            new_label: str = pascalcase(within_merge_key)

                            index_queries.add(
                                f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                            )

                            new_properties: str = ", ".join(
                                map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
                            )

                            reify_and_extract_to_new_node(edge, i, dep, new_label, new_properties, new_props,
                                                          transformation_queries)


                            cleanup_queries.add(
                                f"""
{inter_dep.pattern.to_gql_match_where_string()}
DELETE {edge.symbol}"""
                            )


                            right_ref_label_delim = (
                                ":" if len(right_ref.get_graph_object().labels) > 0 else ""
                            )

                            cleanup_queries.add(
                                f"""
MATCH ({edge.symbol})-[:{new_label.upper()}]->(x{i})
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

                            applied_transformations.append(("inter1", 2))
                elif isinstance(left_go, Node):
                    node = left_go
                    for right_ref in inter_dep.right:
                        left_is_go = (
                            len(
                                set(filter(lambda ref: "." not in str(ref), inter_dep.left))
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
                            logging.info("N -> Ep")

                            transformation_queries.add(
                                f"""
{inter_dep.pattern.to_gql_match_where_string()}
WITH {left_go.symbol}, {right_ref} AS {camelcase(str(right_ref))}
SET {left_go.symbol}.{pascalcase(str(right_ref))} = {camelcase(str(right_ref))}"""
                            )
                            cleanup_queries.add(
                                f"""
{inter_dep.pattern.to_gql_match_where_string()}
REMOVE {right_ref}"""
                            )
                            node.properties.add(pascalcase(str(right_ref)))
                            right_ref.get_graph_object().properties.remove(
                                str(right_ref).split(".")[1]
                            )
                            transformed_deps_list.append(
                                f"{inter_dep.pattern}::{node.symbol}=>{node.symbol}.{pascalcase(str(right_ref))}"
                            )
                            applied_transformations.append(("inter2", 2))

                        elif (
                            right_ref.is_property_variable
                            and not left_is_go
                            and isinstance(right_ref.get_graph_object(), Edge)
                            and (
                                right_ref.get_graph_object().src is node
                                or right_ref.get_graph_object().tgt is node
                            )
                        ):
                            logging.info("Np -> Ep")

                            merge_key_elements = list(map(str, left_references.union({right_ref})))
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_references.union({right_ref}))
                            new_props.sort(key=str)
                            new_properties: str = ", ".join(
                                map(
                                    lambda ref: f"{pascalcase(ref)}: {ref}",
                                    map(str, new_props),
                                )
                            )
                            new_label: str = pascalcase(within_merge_key)

                            index_queries.add(
f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                            )

                            new_properties: str = ", ".join(
                                map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
                            )

                            # _apply_transformation_query(
#                             transformation_queries.add(
#                                 f"""
# {dep.pattern.to_gql_match_where_string()}
# WITH {",".join(map(lambda ref: f"{ref} AS {camelcase(ref)}", map(str, new_props)))}, collect({node.symbol}) AS collect{node.symbol}
# MERGE (newNode:{new_label} {{{new_properties}}})
# WITH newNode, collect{node.symbol}
# UNWIND collect{node.symbol} AS orig{node.symbol}
# CREATE (orig{node.symbol})-[:{new_label.upper()}]->(newNode)"""
#                             )
                            transformation_queries.add(f"""
                            {dep.pattern.to_gql_match_where_string()} 
MERGE (newNode:{new_label} {{{new_properties}}})
MERGE ({node.symbol})-[:{new_label.upper()}]->(newNode)"""
                            )
                            #    pattern += f", ({node.symbol})-[:{new_label.upper()}]->(x{i}:{new_label})"

                            # Remove old redundant properties in the end
                            cleanup_pattern = (
                                inter_dep.pattern.to_gql_match_where_string().split(
                                    "WHERE"
                                )[0]
                            )
                            cleanup_queries.add(
                                f"""
{cleanup_pattern} 
REMOVE {", ".join(map(str, left_references.union({right_ref})))}"""
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

                            applied_transformations.append(("inter3", 0))

        elif dep.is_within_graph_object:
            # First filter References that are Graph Object IDs. We don't need them here as their occurrence is a sign for structurally implied or to limiting dep.s.
            left_references: set[Reference] = set(filter(lambda ref: ref.is_property_variable, dep.left))
            right_references: set[Reference] = set(filter(lambda ref: ref.is_property_variable, dep.right))
            all_references: set[Reference] = left_references.union(right_references)

            merge_key_elements = list(map(str, all_references))
            merge_key_elements.sort()
            within_merge_key: str = ",".join(merge_key_elements)
            new_props = list(right_references.union(left_references))
            new_props.sort(key=str)
            new_properties: str = ", ".join(
                map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
            )
            new_label: str = pascalcase(within_merge_key)

            i += 1

            # # # # # # # # # #
            #  ψ_L1 (psi_L1)  #
            # # # # # # # # # #
            if dep.is_within_node and len(left_references) > 0 and len(right_references) > 0:
                logging.info("Within n")
                node: Node = dep.right.pop().get_graph_object()

                index_queries.add(
                    f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                )

                new_properties: str = ", ".join(
                    map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
                )

                transformation_queries.add(f"""
{dep.pattern.to_gql_match_where_string()} 
MERGE (newNode:{new_label} {{{new_properties}}})
MERGE ({node.symbol})-[:{new_label.upper()}]->(newNode)"""
                )

                # Remove old redundant properties in the end
                cleanup_pattern = dep.pattern.to_gql_match_where_string().split("WHERE")[0]
                cleanup_queries.add(
                    f"""
{cleanup_pattern} 
REMOVE {", ".join(map(str, right_references.union(left_references)))}"""
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

                applied_transformations.append(("within1", 0))

            # # # # # # # # # #
            #  ψ_L2 (psi_L2)  #
            # # # # # # # # # #
            elif (
                dep.is_within_edge and len(left_references) > 0 and len(right_references) > 0
            ):  # ψ_L2 (psi_L2)  --> Reification
                logging.info("Within e")

                edge: Edge = dep.right.pop().get_graph_object()

                index_queries.add(
f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_references)))}) IS UNIQUE"
                )

                new_properties: str = ", ".join(
                    map(lambda ref: f"{pascalcase(ref)} : {ref}", map(str, new_props))
                )

                # Reification + create new node
                reify_and_extract_to_new_node(edge, i, dep, new_label, new_properties, new_props,
                                              transformation_queries)

                cleanup_queries.add(
                    f"""
{dep.pattern.to_gql_match_where_string()}
REMOVE {", ".join(map(str, all_references))}
DELETE {edge.symbol}"""
                )

                cleanup_queries.add(f"""
MATCH ({edge.symbol})-[:{new_label.upper()}]->(x{i})
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

                applied_transformations.append(("within-edge", 2))

        i += 1
    if database == "neo4j":
        for query in tqdm(index_queries, desc="  Indices"):
            _apply_transformation_query(query)
    for query in tqdm(transformation_queries, desc="  Query"):
        _apply_transformation_query(query)
    for query in tqdm(cleanup_queries, desc="  Cleanup"):
        _apply_transformation_query(query)

    transformed_deps = DependencySet.from_string_list(transformed_deps_list)

    return transformed_deps, applied_transformations


def reify_and_extract_to_new_node(edge: Edge, i: int | Any, inter_dep: GNFD, new_label: str, new_properties: str,
                                  new_props: list[Reference], transformation_queries: set[str]):
    # the "naive" way of encoding it
    transformation_queries.add(
            f"""
    {inter_dep.pattern.to_gql_match_where_string()} 
    CREATE ({edge.src.symbol})-[:$("SRC_"+type({edge.symbol}))]->(x{i}:$(type({edge.symbol})))
    CREATE (x{i})-[:$("TGT_"+type({edge.symbol}))]->({edge.tgt.symbol})
    SET x{i} += properties({edge.symbol})
    MERGE (newNode:{new_label} {{{new_properties}}})
    MERGE (x{i})-[:{new_label.upper()}]->(newNode)""")
    ## Uses less database hits but 10x more ram
#     transformation_queries.add(
#         f"""
# {inter_dep.pattern.to_gql_match_where_string()}
# CREATE ({edge.src.symbol})-[:$("SRC_"+type({edge.symbol}))]->(x{i}:$(type({edge.symbol})))
# CREATE (x{i})-[:$("TGT_"+type({edge.symbol}))]->({edge.tgt.symbol})
# SET x{i} += properties({edge.symbol})
# WITH {",".join(map(lambda ref: f"{ref} AS {camelcase(ref)}", map(str, new_props)))}, collect(x{i}) AS collectx{i}
# MERGE (newNode:{new_label} {{{new_properties}}})
# WITH newNode, collectx{i}
# UNWIND collectx{i} AS origx{i}
# CREATE (origx{i})-[:{new_label.upper()}]->(newNode)""")
