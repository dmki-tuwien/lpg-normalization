import logging
import time
import uuid
from typing import Literal

import neo4j
from caseconverter import camelcase, pascalcase
from neo4j import Driver
from tqdm_loggable.auto import tqdm

from lpg_norm.gofd import GOFD, DependencySet, Edge, GraphObject, Node, Reference
from lpg_norm.logger import QueryLogger


def perform_graph_native_normalization(
        driver: Driver,
        database: Literal["neo4j", "memgraph"],
        provided_dependencies: DependencySet,
        dep_filter: Literal["all",
        "within-node",
        "within-edge",
        "within-graph-object",
        "between-graph-object",
        "with-reification",
        "without-reification"] = "all",
        logger: logging.Logger | None = None,
) -> (DependencySet, list[str]):
    """
    Performs graph-native normalization under consideration of the provided parameters.

    :param driver: The connection to the graph database
    :type driver: neo4j.Driver
    :param database: The name of the database in which the to be normalized graph is contained.
    :type: Literal["neo4j",
        "memgraph"]
    :param provided_dependencies: The dependencies to be considered for the normalization
    :type: gnfd.DependencySet
    :param dep_filter: Whether only a subset of dependencies should be used.
    :type: Literal["all",
        "within-node",
        "within-edge",
        "within-graph-object",
        "between-graph-object",
        "with-reification",
        "without-reification"]
    :param logger: Optionally a logger can be provided, if none is provided, an own logger for this method is created and used.
    :type logger: logging.Logger
    :return:
    """

    """A local instance of the logger, if no logger was provided"""
    if logger is None:
        logging.setLoggerClass(QueryLogger)
        logger = logging.getLogger(__name__)

    """A local copy of the provided dependencies that, e.g., may be filtered."""
    deps: DependencySet = provided_dependencies

    """A list of query strings that create indices"""
    index_queries: set[str] = set()
    """A list of query strings that perform the transformations"""
    transformation_queries: set[str] = set()
    """A list of strings of the queries that remove properties"""
    remove_queries: set[str] = set()
    """A list of strings of the queries that delete graph objects"""
    delete_queries: set[str] = set()

    """The set of dependencies after all transformations have been applied."""
    transformed_deps: DependencySet
    """A list of the string representations of the transformed dependencies."""
    transformed_deps_list: list[str] = []

    """The types of transformations in the order they were applied."""
    applied_transformations: list[str] = []

    """Enumerates fresh pattern variables"""
    i = 0

    def _apply_transformation_query(query: str):
        """Runs a query string on the graph connected through :any:`driver`.

        :param query: The to be run query.
        :type query: str"""
        with driver.session(database=database) as session:
            responsive = False
            while not responsive:
                responsive = True
                try:
                    session.run(query)
                    logger.query(query)
                except neo4j.exceptions.TransientError:
                    # Neo4j may still be busy with the previous query
                    responsive = False
                    time.sleep(1)

    def _create_index_for_edge(edge: Edge):
        """Creates a range of indices that facilitate transforamtions involving edges.

        :param edge: The edge to create indices for.
        :type edge: Edge"""
        orig_edge_label = next(iter(edge.labels)) # This retrieves the one and only label of an edge without removing it from the set
        if database == "neo4j":
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
        else:
            assert database == "memgraph"
            index_queries.add(
                f"CREATE INDEX on :{orig_edge_label}({",".join(edge.properties)})"
            )
            index_queries.add(
                f"CREATE EDGE INDEX ON :{orig_edge_label} ({next(iter(edge.properties))})"
            )

    def _create_index_for_new_nodes(new_label: str, left_property_variables: set[Reference]):
        """Adds queries for creating indices for the nodes resulting from transformations.

        :param new_label: The label that identifies the nodes resulting from transformations.
        :type new_label: str
        :param left_property_variables: The variables of the left hand side of the dependency, which form the key of the nodes resulting from the transformations.
        :type set[Reference]
        """
        if database == "neo4j":
            index_queries.add(
                f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_property_variables)))}) IS UNIQUE"
            )
        else:
            assert database == "memgraph"
            index_queries.add(
                f"""CREATE INDEX ON :{new_label}({",".join(map(pascalcase, map(str, left_property_variables)))})""")

    def _create_index_for_existing_nodes_rand(rand: str, node: Node):
        """Creates an index for existing nodes on a random property to ease property removal after the transformations."""
        if database == "neo4j":
            index_queries.add(
                f"CREATE INDEX IF NOT EXISTS FOR (n:{next(iter(node.labels))}) ON (n.`{rand}`)"
            )
        else:
            index_queries.add(
                f"CREATE INDEX ON :{next(iter(node.labels))}(`{rand}`)"
            )

    def _filter_dependencies(dep_filter: Literal["all",
        "within-node",
        "within-edge",
        "within-graph-object",
        "between-graph-object",
        "with-reification",
        "without-reification"],
        deps: DependencySet) -> DependencySet:
        logger.info("Filter dependencies")
        match dep_filter:
            case "within-node":
                deps = DependencySet(filter(lambda dep: dep.is_within_node, deps))
            case "within-edge":
                deps = DependencySet(filter(lambda dep: dep.is_within_edge, deps))
            case "within-graph-object":
                deps = DependencySet(filter(lambda dep: dep.is_within_graph_object, deps))
            case "between-graph-object":
                deps = DependencySet(filter(lambda dep: dep.is_between_graph_object, deps))
            case "with-reification":
                deps = DependencySet(
                    filter(
                        lambda dep: dep.is_within_node
                                    or isinstance(next(iter(dep.left)).get_graph_object(), Node),
                        deps,
                    )
                )
            case "without-reification":
                deps = DependencySet(
                    filter(
                        lambda dep: isinstance(
                            next(iter(dep.left)).get_graph_object(), Edge
                        ),
                        deps,
                    )
                )
        logger.info(f"Dependencies after filtering: {"\n".join({str(dep) for dep in deps})}")
        return deps

    def _get_random_string() -> str:
        return str(uuid.uuid4())[:8]

    def _reify_and_extract_to_new_node(
            edge: Edge,
            inter_dep: GOFD,
            new_label: str,
            new_properties_gql: str,
    ):
        edge_label = next(iter(edge.labels))

        # the "naive" way of encoding it
        transformation_queries.add(
            f"""
        {inter_dep.pattern.to_gql_match_where_string()} 
        CREATE (x{i}:{edge_label})
        CREATE ({edge.src.symbol})-[:SRC_{edge_label}]->(x{i})
        CREATE (x{i})-[:TGT_{edge_label}]->({edge.tgt.symbol})
        MERGE (newNode:{new_label} {{{new_properties_gql}}})
        MERGE (x{i})-[:{new_label.upper()}]->(newNode)
        ON CREATE SET x{i} += properties({edge.symbol})
    """
        )  # Reification may have already happened for another dep. --> Merge!

    # Phase 0: Filter deps (useful for the evaluation.)
    deps = _filter_dependencies(dep_filter, deps)

    if len(deps) == 0:
        logger.warning("No dependencies were provided.")
        return (
            provided_dependencies,
            applied_transformations,
        )  # Nothing will happen --> Return original dependencies



    sorted_deps = list[GOFD](deps)
    sorted_deps.sort()

    for dep in sorted_deps:
        validate_dependency(driver, database, dep, logger)

        if dep.is_between_graph_object:
            inter_dep = dep
            left_gos: set[GraphObject] = {ref.get_graph_object() for ref in dep.left}

            if len(left_gos) == 1:  # Multiple GOs are not supported for the left side
                left_go = left_gos.pop()
                if isinstance(left_go, Edge):
                    edge = left_go
                    for right_ref in dep.right:
                        left_property_variables: set[Reference] = set(
                            filter(lambda ref: ref.is_property_variable, dep.left)
                        )

                        if (
                                right_ref.is_property_variable
                                and len(left_property_variables) > 0
                                and isinstance(right_ref.get_graph_object(), Node)
                                and (
                                right_ref.get_graph_object() is left_go.src
                                or right_ref.get_graph_object() is left_go.tgt
                        )
                        ):
                            logger.info("between-ep-np")
                            assert isinstance(right_ref.get_graph_object(), Node)

                            merge_key_elements = list(
                                map(str, left_property_variables.union({right_ref}))
                            )
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_property_variables.union({right_ref}))
                            new_props.sort(key=str)
                            new_label: str = pascalcase(within_merge_key)


                            _create_index_for_new_nodes(new_label, left_property_variables)
                            _create_index_for_edge(edge)


                            new_properties_gql: str = ", ".join(f"{pascalcase(s := str(ref))} : {s}" for ref in new_props)

                            _reify_and_extract_to_new_node(
                                edge,
                                dep,
                                new_label,
                                new_properties_gql,
                            )

                            rand = _get_random_string()
                            node = right_ref.get_graph_object()

                            _create_index_for_existing_nodes_rand(rand, node)

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
MATCH ({"".join(f":{lab}" for lab in edge.src.labels)})-[{edge.symbol}{"".join(f":{lab}" for lab in edge.labels)}]->({"".join(f":{lab}" for lab in edge.tgt.labels)})
WITH DISTINCT {edge.symbol}
DELETE {edge.symbol}"""
                            )

                            remove_queries.add(
                                f"""
MATCH ({edge.symbol}) - [:{new_label.upper()}]->(x{i})
REMOVE {", ".join(map(str, left_property_variables))}"""
                            )  # Connect normalized nodes with reified nodes and remove redundant properties

                            transformed_deps_list.append(
                                f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, left_property_variables.union({right_ref}))))})
::
{",".join(f"x{i}.{pascalcase(str(ref))}" for ref in left_property_variables)}
=>x{i}""".replace(
                                    " ", ""
                                ).replace(
                                    "\n", ""
                                )
                            )

                            applied_transformations.append("between-ep-np")

                        elif (
                                right_ref.is_graph_object_variable
                                and len(left_property_variables) > 0
                                and isinstance(right_ref.get_graph_object(), Node)
                                and (
                                        right_ref.get_graph_object() is left_go.src
                                        or right_ref.get_graph_object() is left_go.tgt
                                )
                        ):
                            logger.info("between-ep-n")

                            merge_key_elements = list(map(str, left_property_variables))
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_property_variables)
                            new_props.sort(key=str)
                            new_label: str = pascalcase(within_merge_key)


                            _create_index_for_new_nodes(new_label, left_property_variables)
                            _create_index_for_edge(edge)


                            new_properties_gql: str = ", ".join(f"{pascalcase(s := str(ref))} : {s}" for ref in new_props)

                            _reify_and_extract_to_new_node(
                                edge,
                                dep,
                                new_label,
                                new_properties_gql,
                            )

                            delete_queries.add(
                                f"""
MATCH ({"".join(f":{lab}" for lab in edge.src.labels)})-[{edge.symbol}{"".join(f":{lab}" for lab in edge.labels)}]->({"".join(f":{lab}" for lab in edge.tgt.labels)})
WITH DISTINCT {edge.symbol}
DELETE {edge.symbol}"""
                            )

                            remove_queries.add(
                                f"""
MATCH ({edge.symbol})-[:{new_label.upper()}]->(x{i})
WITH DISTINCT {edge.symbol}
REMOVE {", ".join(str(ref) for ref in left_property_variables)}"""
                            )  # Connect normalized nodes with reified nodes and remove redundant properties

                            transformed_deps_list.append(
                                f"""
(x{i}:{new_label}:{"&".join(pascalcase(str(ref)) for ref in left_property_variables.union({right_ref}))})
::
{",".join(f"x{i}.{pascalcase(str(ref))}" for ref in left_property_variables)}
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
                        left_property_variables: set[Reference] = set(
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
                            logger.info("between-n-ep")

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
                            logger.info("between-np-ep")

                            merge_key_elements = list(
                                map(str, left_property_variables)
                            )
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_property_variables.union({right_ref}))
                            new_props.sort(key=str)
                            new_label: str = pascalcase(within_merge_key)

                            if database == "neo4j":
                                index_queries.add(
                                    f"CREATE CONSTRAINT IF NOT EXISTS FOR (newNode:{new_label}) REQUIRE (newNode.{", newNode.".join(map(pascalcase, map(str, left_property_variables)))}) IS UNIQUE"
                                )
                            else:
                                assert database == "memgraph"
                                index_queries.add(
                                    f"""CREATE INDEX ON :{new_label}({",".join(map(pascalcase, map(str, left_property_variables)))})""")

                            new_properties_gql: str = ", ".join(f"{pascalcase(s := str(ref))} : {s}" for ref in new_props)

                            rand = _get_random_string()
                            _create_index_for_existing_nodes_rand(rand, node)

                            transformation_queries.add(
                                f"""
                            {dep.pattern.to_gql_match_where_string()} 
MERGE (newNode:{new_label} {{{new_properties_gql}}})
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
REMOVE {", ".join(map(str, left_property_variables.union({right_ref})))}
WITH DISTINCT {node.symbol}
REMOVE {node.symbol}.`{rand}`
"""
                            )

                            right_ref.get_graph_object().properties -= {right_ref}
                            node.properties -= left_property_variables

                            transformed_deps_list.append(
                                f"""
(x{i}:{new_label}:{"&".join(pascalcase(str(ref)) for ref in left_property_variables.union({right_ref}))})
::
{",".join(f"x{i}.{pascalcase(str(ref))}" for ref in left_property_variables)}
=>x{i}""".replace(
                                    " ", ""
                                ).replace(
                                    "\n", ""
                                )
                            )

                            applied_transformations.append("between-np-ep")

            else:
                assert len(left_gos) > 1
                logger.warning("Invalid 'between-graph-object' dependency provided, only one graph object on the left-hand side is supported for now.")

        elif dep.is_within_graph_object:
            # First filter References that are Graph Object IDs. We don't need them here as their occurrence is a sign for structurally implied or to limiting dep.s.
            left_property_variables: set[Reference] = set(
                filter(lambda ref: ref.is_property_variable, dep.left)
            )
            right_property_variables: set[Reference] = set(
                filter(lambda ref: ref.is_property_variable, dep.right)
            )
            all_property_variables: set[Reference] = left_property_variables.union(right_property_variables)

            # Nodes resulting from transformation are identified tby
            merge_key_elements: list[str] = [str(v) for v in all_property_variables]
            merge_key_elements.sort()

            within_merge_key: str = ",".join(merge_key_elements)
            new_props = list(right_property_variables.union(left_property_variables))
            new_props.sort(key=str)
            new_label: str = pascalcase(within_merge_key)

            i += 1

            # # # # # # # # # #
            #   within-node   #
            # # # # # # # # # #
            if (
                    dep.is_within_node
                    and len(left_property_variables) > 0
                    and len(right_property_variables) > 0
            ):
                logger.info("within-n")

                node: Node = dep.right.pop().get_graph_object() # since this is a within-node dependency, the only graph object of the right hand side is a node!

                # Add indices for the to be created nodes to speed up transformation
                _create_index_for_new_nodes(new_label, left_property_variables)

                new_properties_gql: str = ", ".join(
                    f"{pascalcase(s := str(prop))} : {s}" for prop in new_props
                )

                rand = _get_random_string()
                _create_index_for_existing_nodes_rand(rand, node)

                transformation_queries.add(
                    f"""
{dep.pattern.to_gql_match_where_string()} 
MERGE (newNode:{new_label} {{{new_properties_gql}}})
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
REMOVE {", ".join(map(str, right_property_variables.union(left_property_variables)))}
"""
                )

                dep.pattern.properties -= all_property_variables

                transformed_deps_list.append(
                    f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, right_property_variables.union(left_property_variables))))})
::
{",".join(f"x{i}.{pascalcase(str(ref))}" for ref in left_property_variables)}
=>x{i}""".replace(
                        " ", ""
                    ).replace(
                        "\n", ""
                    )
                )

                applied_transformations.append("within-n")

            # # # # # # # # # #
            #   within-edge   #
            # # # # # # # # # #
            elif (
                    dep.is_within_edge
                    and len(left_property_variables) > 0
                    and len(right_property_variables) > 0
            ):  # --> Reification
                logger.info("Within e")

                edge: Edge = dep.right.pop().get_graph_object()

                _create_index_for_new_nodes(new_label, left_property_variables)
                _create_index_for_edge(edge)

                new_properties_gql: str = ", ".join(
                    f"{pascalcase(s := str(ref))} : {s}" for ref in new_props
                )

                # Reification + create new node
                _reify_and_extract_to_new_node(
                    edge,
                    dep,
                    new_label,
                    new_properties_gql,
                )

                delete_queries.add(
                    f"""
MATCH ({"".join(f":{lab}" for lab in edge.src.labels)})-[{edge.symbol}{"".join(f":{lab}" for lab in edge.labels)}]->({"".join(f":{lab}" for lab in edge.tgt.labels)})
REMOVE {", ".join(map(str, all_property_variables))}
WITH DISTINCT {edge.symbol}
DELETE {edge.symbol}"""
                )

                remove_queries.add(
                    f"""
MATCH ({edge.symbol})-[:{new_label.upper()}]->(x{i})
WITH DISTINCT {edge.symbol}
REMOVE {", ".join(map(str, all_property_variables))}"""
                )  # Connect normalized nodes with reified nodes and remove redundant properties

                transformed_deps_list.append(
                    f"""
(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, right_property_variables.union(left_property_variables))))})
::
{",".join(f"x{i}.{pascalcase(str(ref))}" for ref in left_property_variables)}
=>x{i}""".replace(
                        " ", ""
                    ).replace(
                        "\n", ""
                    )
                )

                applied_transformations.append("within-e")

        i += 1

    logger.info("Create indices for transformations")
    for query in tqdm(index_queries, desc="  Indices"):
        _apply_transformation_query(query)

    logger.info("Create and merge new graph objects")
    for query in tqdm(transformation_queries, desc="  Query"):
        _apply_transformation_query(query)

    logger.info("Remove no longer needed property values")
    for query in tqdm(remove_queries, desc="  Cleanup (REMOVE)"):
        _apply_transformation_query(query)

    logger.info("Delete no longer needed graph objects")
    for query in tqdm(delete_queries, desc="  Cleanup (DELETE)"):
        _apply_transformation_query(query)

    transformed_deps = DependencySet.from_string_list(transformed_deps_list)

    return transformed_deps, applied_transformations





# def perform_structural_normalization(driver: Driver,
#                                      database: Literal["neo4j", "memgraph"],
#                                      normal_form: Literal["1GNF", "2GNF", "3GNF", "3+GNF", "EGNF"],
#                                      provided_dependencies: DependencySet = DependencySet(),
#                                      dep_filter: str = "all",
#                                      ):
#     """
#     Performs Structural Normalization as described by Egger et al. in https://doi.org/10.14778/3797919.3797943.
#     Currently, this implementation of Structural Normalization is still incomplete and experimental.
#     :param driver: A :any:`neo4j.Driver`
#     :param database: The graph database system containing the graph to be normalized. Currently only Neo4j is supported, Memgraph will follow eventually.
#     :param normal_form: The normal form the normalized graph should fulfill.
#     """
#     if database == "memgraph":
#         raise NotImplementedError("Structural Normalization is currently only implemented for `Nseo4j`.")
#
#     def get_or_create_single_prop(property_name: str, value) -> str:
#         # Mimics `getOrCreate` from https://doi.org/10.14778/3797919.3797943
#         return get_or_create_dict(frozendict({property_name: value}))
#
#     def get_or_create_dict(d: dict) -> str:
#         """:returns: the node id"""
#         query: str = ""
#
#         if len(d) > 0:
#             query = "MERGE (n {"
#             props = []
#             for k,v in d.items():
#                 if v is not None and isinstance(v, bool | int | float):
#                     props.append(f"`{k}`:{v}")
#                 elif v is not None:
#                     props.append(f"`{k}`:\"{v}\"")
#             query += ", ".join(props)
#             query += "}) RETURN elementId(n) as nodeId LIMIT 1"
#         else:
#             query = """MERGE (n) RETURN elementId(n) as nodeId LIMIT 1"""
#         res = session.run(query)
#
#         for record in res:
#             return str(record["nodeId"])
#
#     match normal_form:
#         case "1GNF":
#             with driver.session() as session:
#
#                 found_non_atomic = True  # To check whether there are non-atomic properties, we assume there are some!
#
#                 # Retrieve all non-atomic values in edges and reify them
#                 session.run("""
#                 MATCH (n)-[e]->(m)
#                 UNWIND keys(e) AS key
#                 WITH n, m, e, key, e[key] AS propValue
#                 WHERE propValue IS :: LIST<ANY>
#                 CREATE (re:$(type(e)))
#                 CREATE (n)-[:$("SRC_"+type(e))]->(re)
#                 CREATE (re)-[:$("TGT_"+type(e))]->(m)
#                 SET re += properties(e)
#                 DELETE e""")  # happens only once; after this only nodes can have complex property values.
#
#                 while found_non_atomic:
#
#                     # Retrieve all non-atomic values in nodes (original nodes + reified)
#                     result = session.run("""
#     MATCH (n)
#     UNWIND keys(n) AS key
#     WITH n, key, n[key] AS propValue
#     WHERE propValue IS :: LIST<ANY>
#     RETURN elementId(n) AS nodeId, key AS propName, propValue
#                     """)
#
#                     found_non_atomic = False
#                     for record in result:
#                         # The loop is accessed when there were non-atomic values
#                         found_non_atomic = True  # There were non-atomic values, so we need another iteration!
#                         i = 0
#                         for atomic_value in record["propValue"]:
#                             get_or_create_single_prop(record["propName"], atomic_value)
#
#                             if isinstance(atomic_value, bool | int | float):
#                                 session.run(f"""
#                                 MATCH (n) WHERE elementId(n) = "{record["nodeId"]}"
#                                 MATCH (m) WHERE size(keys(m)) = 1 AND m.{record["propName"]} = {atomic_value}
#                                 CREATE (n)-[:`{i}`]->(m)
#                                 """)
#                             else:
#                                 session.run(f"""
#                                 MATCH (n) WHERE elementId(n) = "{record["nodeId"]}"
#                                 MATCH (m) WHERE size(keys(m)) = 1 AND m.{record["propName"]} = "{atomic_value}"
#                                 CREATE (n)-[:`{record["propName"]}` {{`{i}`:{i}}}]->(m)
#                                 """)
#
#                             i += 1
#                         session.run(f"""
#     MATCH (n) WHERE elementId(n) = "{record["nodeId"]}"
#     REMOVE n.{record["propName"]}
#     """)
#
#         case "2GNF":
#             deps: DependencySet
#             if dep_filter != all:
#                 deps = filter_dependencies(dep_filter, provided_dependencies)
#             else:
#                 deps = provided_dependencies
#
#             L: DependencySet = DependencySet()
#             C: set(tuple[GOFD, GOFD]) = set()
#             # TODO: use a named tuple for the conflicting deps
#             for dep in deps:
#                 if len(set(map(lambda r: r.get_graph_object(), dep.left)).intersection(
#                         set(map(lambda r: r.get_graph_object(), dep.right)))) == 0:
#                     # TODO check whether left side is part of a key ...
#                     L.add(dep)
#                     for d in deps:
#                         if dep.is_conflicting_with(d):
#                             if len(set(filter(lambda tup: tup[0] == d and tup[1] == dep, C))) == 0:
#                                 C.add((dep, d))
#                             L.remove(dep)
#                             L.remove(d)
#             # this corresponds to the end of line 7 in the pseudo code
#
#             with driver.session() as session:
#                 result = session.run("""
#                     MATCH (n)
#                     RETURN elementId(n) as nodeId, labels(n) as nodeLabels
#                                     """)
#                 for record in result:
#                     for c in C:
#                         # As B should be the same in c0 and c1, we use the one from c0
#                         a1: set[Reference] = c[0].left
#                         a2: set[Reference] = c[1].left
#
#                         b: set[Reference] = c[0].right
#                         if next(iter(b)).get_graph_object().labels.issubset(set(record["nodeLabels"])):
#                             # The algorithm suddenly treats A1, A2 and B as a single reference, so we just assume they are all references of one node each ...
#                             resB = session.run(f"""
#                                                 MATCH (n)
#                                                 WHERE elementId(n) = {record["nodeId"]}
#                                                 RETURN {", ".join(map(lambda ref: f"n.{ref.reference.key} as {ref.reference.key}", b))}
#                                                                 """)
#                             resA1 = session.run(f"""
#                                                 MATCH (n)
#                                                 WHERE labels(n) = [{", ".join(next(iter(a1)).get_graph_object().labels)}]
#                                                 RETURN {", ".join(map(lambda ref: f"n.{ref.reference.key} as {ref.reference.key}", a1))}
#                                                                 """)
#                             resA2 = session.run(f"""
#                                                 MATCH (n)
#                                                 WHERE labels(n) = [{", ".join(next(iter(a2)).get_graph_object().labels)}]
#                                                 RETURN {", ".join(map(lambda ref: f"n.{ref.reference.key} as {ref.reference.key}", a2))}
#                                                                 """)
#
#                             bId: dict = get_or_create_dict(resB.single().data())
#                             a1Id: dict = get_or_create_dict(resA1.single().data())
#                             a2Id: dict = get_or_create_dict(resA2.single().data())
#
#                             session.run(
#                                 f"MERGE (n)-[m:NO_LABEL_PROVIDED]->(o) WHERE elementId(n) = {a1Id} AND elementId(o) = {bId}")
#                             session.run(
#                                 f"MERGE (n)-[m:NO_LABEL_PROVIDED]->(o) WHERE elementId(n) = {a2Id} AND elementId(o) = {bId}")
#
#                     for dep in L:
#                         if len({r.get_graph_object() for r in dep.left}.intersection(
#                                 {r.get_graph_object() for r in dep.right})) == 0:
#                             pass
#
#         case _:
#             raise ValueError(f"The normal form \"{normal_form}\" is not supported (yet) for Structural Normalization")
#
#     return DependencySet.from_string_list([]), []


def validate_dependency(driver, database, dep, logger):
    """Validates whether a functional dependency holds"""
    logger.info(f"Validate dependency \"{str(dep)}\"")
    if dep.is_trivial:
        logger.info(f"\"{str(dep)}\" is trivial.")
        return  # The dependency is technically valid, although not minimal!

    with driver.session(database=database) as session:
        query = f"""
{dep.pattern.to_gql_match_where_string()}
WITH DISTINCT
{",".join((s := str(ref)) + " AS " + pascalcase(s) for ref in dep.left.union(dep.right))}
WITH
{",".join(pascalcase(str(ref)) for ref in dep.left)},
COUNT([{",".join(pascalcase(str(ref)) for ref in  dep.right)}]) AS card
RETURN avg(card)=1 AS res
"""
        res = session.run(query)
        logger.query(query)
        record = res.single()
        if record is not None and not record["res"]:
            raise ValueError(f'The dependency "{dep!s}" is not functional!')


