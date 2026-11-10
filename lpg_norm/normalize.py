import logging
import time
import uuid
from typing import Literal

import neo4j
from caseconverter import camelcase, pascalcase
from neo4j import Driver
from tqdm_loggable.auto import tqdm
from openai import OpenAI

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
        useLlm: bool = False,
        llmUrl: str | None = None,
        llmKey: str | None = None,
        llmModel: str | None = None,
) -> (DependencySet, list[str]):
    """
    Performs graph-native normalization under consideration of the provided parameters.

    :param driver: The connection to the graph database
    :type driver: neo4j.Driver
    :param database: The name of the database in which the to be normalized graph is contained.
    :type: Literal["neo4j",
        "memgraph"]
    :param provided_dependencies: The dependencies to be considered for the normalization
    :type provided_dependencies: gnfd.DependencySet
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
    :param useLlm: Whether to use an LLM to generate fresh labels
    :type useLlm: bool
    :param llmUrl: URL of an OpenAI API compatible LLM endpoint
    :type llmUrl: str
    :param llmKey: API Key for the provided LLM API
    :type llmKey: str
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

    """Keeps track of the fresh labels."""
    labels: dict[str, str] = {}

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
            case "all":
                deps = DependencySet(filter(lambda dep: not dep.is_trivial, deps))
            case "within-node":
                deps = DependencySet(filter(lambda dep: dep.is_within_node and not dep.is_trivial, deps))
            case "within-edge":
                deps = DependencySet(filter(lambda dep: dep.is_within_edge and not dep.is_trivial, deps))
            case "within-graph-object":
                deps = DependencySet(filter(lambda dep: dep.is_within_graph_object and not dep.is_trivial, deps))
            case "between-graph-object":
                deps = DependencySet(filter(lambda dep: dep.is_between_graph_object and not dep.is_trivial, deps))
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

    def _get_fresh_labels(merge_key: str, properties: list[str]) -> str:
        if merge_key in labels.keys():
            return labels[merge_key]

        if merge_key not in labels.keys():
            if not useLlm or llmKey == "" or llmKey is None or llmUrl == "" or llmUrl is None or llmModel == "" or llmModel is None:
                labels[merge_key] = pascalcase(within_merge_key)
            else:
                assert useLlm

                existing_labels: list[str] = []

                with driver.session(database=database) as session:
                    result = session.run("""MATCH (n)
UNWIND labels(n) AS label
RETURN DISTINCT label;""")
                    existing_labels = [record["label"] for record in result]

                llm_client = OpenAI(
                    base_url=llmUrl,
                    api_key=llmKey,
                )

                response = llm_client.chat.completions.create(
                    model=llmModel,  # Replace with the model served by your provider
                    messages=[
                        {"role": "system", "content": "You are a concise assistant for data modeling purposes."},
                        {"role": "user", "content": f"Find a label for a node with the following properties: {", ".join(properties)}\n\nThe label must not be one of the following: {", ".join(existing_labels)}\n\nThe Return a single word that starts with an uppercase letter."},
                    ],
                    temperature=0.7,
                )

                # Extract and use the response text
                reply = response.choices[0].message.content
                labels[merge_key] = reply.split()[0] # In case the LLM returned more than one word: use only the first one

        return labels[merge_key]

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
        logger.warning("No non-trivial dependencies were provided.")
        return (
            deps,
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

                            merge_key_elements = [str(left) for left in left_property_variables]
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_property_variables.union({right_ref}))
                            new_props.sort(key=str)
                            new_label: str = _get_fresh_labels(within_merge_key, merge_key_elements)


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

                            merge_key_elements = [str(left) for left in left_property_variables]
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_property_variables)
                            new_props.sort(key=str)
                            new_label: str = _get_fresh_labels(within_merge_key, merge_key_elements)

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

                            merge_key_elements = [str(left) for left in left_property_variables]
                            merge_key_elements.sort()
                            within_merge_key: str = ",".join(merge_key_elements)
                            new_props = list(left_property_variables.union({right_ref}))
                            new_props.sort(key=str)
                            new_label: str = _get_fresh_labels(within_merge_key, [str(prop) for prop in new_props])

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
            merge_key_elements: list[str] = [str(v) for v in left_property_variables]
            merge_key_elements.sort()

            within_merge_key: str = ",".join(merge_key_elements)
            new_props = list(right_property_variables.union(left_property_variables))
            new_props.sort(key=str)
            new_label: str = _get_fresh_labels(within_merge_key, merge_key_elements)

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





def perform_structural_normalization(driver: Driver,
                                     database: Literal["neo4j", "memgraph"],
                                     logger: logging.Logger | None = None) -> (DependencySet, list[str]):

    """A local instance of the logger, if no logger was provided"""
    if logger is None:
        logging.setLoggerClass(QueryLogger)
        logger = logging.getLogger(__name__)

    def _apply_query(query: str) -> list[neo4j.Record]:
        """Runs a query string on the graph connected through :any:`driver`.

        :param query: The to be run query.
        :type query: str"""
        with driver.session(database=database) as session:
            responsive = False
            while not responsive:
                responsive = True
                try:
                    logger.query(query)
                    res = session.run(query)
                    return list(res)
                except neo4j.exceptions.TransientError:
                    # Neo4j may still be busy with the previous query
                    responsive = False
                    time.sleep(1)

    # Refiy all non-empty Edges
    logger.info("Reify all non-empty edges")
    get_edge_types_query = """
MATCH ()-[m]-()
WHERE size(keys(m)) > 0
RETURN DISTINCT type(m) AS t"""
    res = _apply_query(get_edge_types_query)
    for record in res:
        edge_type = record["t"]
        reify_query = f"""
MATCH (s)-[e:{edge_type}]->(t)
CREATE (x:{edge_type})
CREATE (s)-[:SRC_{edge_type}]->(x)
CREATE (x)-[:TGT_{edge_type}]->(t)
SET x += CASE 
    WHEN size(keys(properties(e))) > 0 THEN properties(e) 
    ELSE {{}} 
END"""
        _apply_query(reify_query)

        remove_edge_query = f"""
MATCH ()-[e:{edge_type}]->()
DELETE e
"""
        _apply_query(remove_edge_query)


    # Create nodes for all properties
    get_properties_query = """
MATCH (n)
UNWIND keys(n) AS p
RETURN DISTINCT p"""
    res = _apply_query(get_properties_query)
    for record in res:
        property = record["p"]
        extract_property_query = f"""
MATCH (n) 
WHERE n.{property} IS NOT NULL
MERGE (m:{property} {{{property}: n.{property}}})
MERGE (n)-[:{property.upper()}]->(m)
REMOVE n.{property}
"""
        _apply_query(extract_property_query)


    return DependencySet(), []


def validate_dependency(driver, database, dep, logger):
    """Validates whether a functional dependency holds"""
    logger.info(f"Validate dependency \"{str(dep)}\"")
    if dep.is_trivial:
        logger.warning(f"\"{str(dep)}\" is trivial.")
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
            logger.error(f'The dependency "{dep}" is not functional!')


