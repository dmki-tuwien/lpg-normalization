import logging
import re
from typing import Literal

from caseconverter import pascalcase
from dtgraph import Rule, Transformation
from dtgraph.backend.neo4j.graph import Neo4jGraph
from neo4j import GraphDatabase, Driver
from tqdm_loggable.auto import tqdm


from gnfd import DependencySet, GNFD, Node, Reference, Edge, GraphObject


def perform_graph_native_normalization(driver: Driver, database,
                                       provided_dependencies: DependencySet,
                                       dep_filter: str = "all",
                                       ordered: bool = True) -> (DependencySet, list[tuple[str,int]]):
    """
    Performs graph native normalization under consideration of the provided parameters.
    :param driver: The connection to the graph DBMS to be used
    :type driver: Driver
    :param database: The name of the database in which the to be normalized graph is contained
    :param provided_dependencies: The dependencies to be considered for the normalization
    :param dep_filter: Whether only a subset of dependencies should be used. Possible values: intra-node, intra-go, inter-go, all
    :return:
    """


    # Create a DTGraph Neo4jGraph instance with a non-sense driver
    con = Neo4jGraph("bolt://memgraph:7687", database="DATABASE", username="USERNAME", password="PASSWORD")
    con.driver = driver # Replace the driver with the actual driver

    """A local copy of the provided dependencies, that e.g., may be filtered."""
    deps = provided_dependencies

    transformed_deps = DependencySet()
    applied_transformations: list[tuple[str,int]] = []

    def _apply_transformation_rule(rule: Rule):
        transformation = Transformation([rule])
        t = transformation.apply_on(con)
        transformation.eject()
        return t

    def _apply_transformation_query(query: str):
        with driver.session(database=database) as session:
            session.run(query)


    # Phase 0: Filter deps according to eval.
    match dep_filter:
        case "within-node":
            deps = DependencySet(filter(lambda dep: dep.is_within_node, deps))
        case "within-go":
            deps = DependencySet(filter(lambda dep: dep.is_within_graph_object, deps))
        case "inter-go":
            deps = DependencySet(filter(lambda dep: dep.is_inter_graph_object, deps))

    if len(deps) == 0:
        return (provided_dependencies, applied_transformations)  # Return original dependencies

   # pattern = str(provided_dependencies.dependency_pattern)


    transformed_deps_list: list[str] = []

    cleanup_queries: list[str] = []

    i = 0

    # Global
    inter_rules = []
    inter_queries = []
    inter_deps: set[GNFD] = set(
        filter(lambda dep: dep.is_inter_graph_object, provided_dependencies)
    )
    for inter_dep in inter_deps:
        left_gos: set[GraphObject] = set(map(lambda ref: ref.get_graph_object(), inter_dep.left))
        right_gos: set[GraphObject] = set(map(lambda ref: ref.get_graph_object(), inter_dep.right))

        if len(left_gos) == 1: # Multiple GOs are currently not supported for the left side
            left_go = left_gos.pop()
            if isinstance(left_go, Edge):
                edge = left_go
                for right_ref in inter_dep.right:
                    left: set[Reference] = set(filter(lambda ref: "." in str(ref), inter_dep.left))

                    if ("." in str(right_ref) and len(left) > 0 and
                            isinstance(right_ref.get_graph_object(), Node) and
                            (right_ref.get_graph_object() is left_go.src or right_ref.get_graph_object() is left_go.tgt)):

                        merge_key_elements = list(map(str, left.union({right_ref})))
                        merge_key_elements.sort()
                        within_merge_key: str = ",".join(merge_key_elements)
                        new_props = list(left.union({right_ref}))
                        new_props.sort(key=str)
                        new_properties: str = ", ".join(
                            map(lambda ref: f"{pascalcase(ref)} = {ref}", map(str, new_props)))
                        new_label: str = pascalcase(within_merge_key)

                        # First reification
                        # _apply_transformation_query(
                        inter_queries.append(f"""
                        {inter_dep.pattern.to_gql_match_where_string()} 
                        CREATE ({edge.src.symbol})-[:$("SRC_"+type({edge.symbol}))]->(x{i}:$(type({edge.symbol})))
                        CREATE (x{i})-[:$("TGT_"+type({edge.symbol}))]->({edge.tgt.symbol})
                        SET x{i} += properties({edge.symbol})
                                                        """)  # relies on Neo4j >= 5.26

                        cleanup_queries.append(f"""
                        {inter_dep.pattern.to_gql_match_where_string()}
                        DELETE {edge.symbol}
                        """)

                        # Then normalization
                        # _apply_transformation_rule(
                        inter_rules.append(Rule(f"""
                                                {inter_dep.pattern.to_gql_match_where_string()} 
                                                GENERATE
                                                (y = ({within_merge_key}) :{new_label} {{{new_properties}}})
                                                """))  # nodes with same values for properties on left side should be merged!

                        inter_queries.append(f"""
                                                {inter_dep.pattern.to_gql_match_where_string()} 
                                                MATCH (x{i}:{new_label})
                                                MATCH (old:$(type({edge.symbol})))
                                                WHERE {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = old.{ref.split(".")[1]}", map(str, left)))} AND x{i}.{pascalcase(str(right_ref))} = {right_ref}
                                                MERGE (old) - [:{new_label.upper()}]->(x{i})
                                                """)  # Connect normalized nodes with reified nodes and remove redundant properties

                        # MATCH(x
                        # {i}: {new_label})
                        # WHERE
                        # {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = {ref}", map(str, local_dep.get_references())))}
                        # MERGE({edge.symbol}) - [: {new_label.upper()}]->(x{i})
                        # REMOVE
                        # {", ".join(map(str, local_dep.get_references()))}

                        cleanup_pattern = inter_dep.pattern.to_gql_match_where_string().split("WHERE")[0]

                        right_ref_label_delim = ":" if len(right_ref.get_graph_object().labels) > 0 else ""
                        cleanup_queries.append(f"""
                                                            MATCH ({right_ref.get_graph_object().symbol}{right_ref_label_delim}{"&".join(right_ref.get_graph_object().labels)})
                                                            REMOVE {right_ref}
                                                            """)  # Connect normalized nodes with reified nodes and remove redundant properties

                        cleanup_queries.append(f"""
                                                MATCH ({edge.symbol}) - [:{new_label.upper()}]->(x{i})
                                                                        REMOVE {", ".join(map(str, left))}
                                                                        """)  # Connect normalized nodes with reified nodes and remove redundant properties

                        transformed_deps_list.append(f"""
                                                ({edge.symbol})-[:{new_label.upper()}]->(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, left.union({right_ref}))))})
                                                ::
                                    {",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left)))}
                                    =>x{i}.{pascalcase(str(right_ref))}""".replace(
                            " ", "").replace("\n",
                                             ""))

                        applied_transformations.append(("inter1", 2))
                    # if there is no "." in the reference on the right its just cardinality limiting
                    # if its no Node its more than one hop for sure
            elif isinstance(left_go, Node):
                node = left_go
                for right_ref in inter_dep.right:
                    left_is_go = len(set(filter(lambda ref: "." not in str(ref), inter_dep.left))) > 0
                    left: set[Reference] = set(filter(lambda ref: "." in str(ref), inter_dep.left))

                    if ("." in str(right_ref) and left_is_go and
                            isinstance(right_ref.get_graph_object(), Edge) and
                            (
                                    right_ref.get_graph_object().src is node or right_ref.get_graph_object().tgt is node)):
                        inter_queries.append(f"""
                            {inter_dep.pattern.to_gql_match_where_string()}
                            SET {left_go.symbol}.{pascalcase(str(right_ref))} = {right_ref}
"""
                        )
                        cleanup_queries.append(f"""
                                                    {inter_dep.pattern.to_gql_match_where_string()}
                                                    REMOVE {right_ref}
                        """
                                             )
                        node.properties.add(pascalcase(str(right_ref)))
                        right_ref.get_graph_object().properties.remove(str(right_ref).split(".")[1])
                        transformed_deps_list.append(f"""
{inter_dep.pattern}::{node.symbol}=>{node.symbol}.{pascalcase(str(right_ref))}
""")
                        applied_transformations.append(("inter2", 2))

                    elif("." in str(right_ref) and not left_is_go and
                            isinstance(right_ref.get_graph_object(), Edge) and
                            (
                                    right_ref.get_graph_object().src is node or right_ref.get_graph_object().tgt is node)):
                        merge_key_elements = list(map(str, left.union({right_ref})))
                        merge_key_elements.sort()
                        within_merge_key: str = ",".join(merge_key_elements)
                        new_props = list(left.union({right_ref}))
                        new_props.sort(key=str)
                        new_properties: str = ", ".join(
                            map(lambda ref: f"{pascalcase(ref)} = {ref}", map(str, new_props)))
                        new_label: str = pascalcase(within_merge_key)

                        # count = _apply_transformation_rule(
                        inter_rules.append(Rule(f'''
                                                {inter_dep.pattern.to_gql_match_where_string()} 
                                                GENERATE
                                                (x = ({within_merge_key}):{new_label} {{
                                                {new_properties}
                                                }})
                                                        '''))  # Create new nodes for dep., nodes with same values for properties on left side should be merged!

                        # _apply_transformation_query(
                        inter_queries.append(f"""
                                                {inter_dep.pattern.to_gql_match_where_string()} 
                                                MATCH (x{i}:{new_label})
                                                WHERE {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = {ref}", map(str, left.union({right_ref}))))}
                                                MERGE ({node.symbol})-[:{new_label.upper()}]->(x{i})
                                                        """)  # Connect the new nodes with the existing nodes

                        #    pattern += f", ({node.symbol})-[:{new_label.upper()}]->(x{i}:{new_label})"

                        # Remove old redundant properties in the end
                        cleanup_pattern = inter_dep.pattern.to_gql_match_where_string().split("WHERE")[0]
                        cleanup_queries.append(f"""
                                                {cleanup_pattern} 
                                                REMOVE {", ".join(map(str, left.union({right_ref})))}
                                                        """)

                        right_ref.get_graph_object().properties -= {right_ref}
                        node.properties -= left

                        transformed_deps_list.append(f"""
                                    (x{i}:{new_label}:{"&".join(map(pascalcase, map(str, left.union({right_ref}))))})
                                    ::
                        {",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left)))}
                        =>x{i}.{pascalcase(str(right_ref))}""".replace(" ",
                                                                                                             "").replace(
                            "\n", ""))

                        applied_transformations.append(("inter3", 0))
        pass

    transformation = Transformation(inter_rules)
    t = transformation.apply_on(con)
    transformation.eject()

    for inter_query in inter_queries:
        _apply_transformation_query(inter_query)


    # # # # # # # # # # # # # # # # # # # # # # #
    #  Local (ψ_L1 (psi_L1) and  ψ_L2 (psi_L2)) #
    # # # # # # # # # # # # # # # # # # # # # # #

    within_rules = []
    within_queries = []
    within_deps: set[GNFD] = set(filter(lambda dep: dep.is_within_graph_object, provided_dependencies))
    for within_dep in within_deps:
        # First filter References that are Graph Object IDs. We don't need them here as their occurrence is a sign for structurally implied or to limiting dep.s.
        left: set[Reference] = set(filter(lambda ref: "." in str(ref), within_dep.left))
        right: set[Reference] = set(filter(lambda ref: "." in str(ref), within_dep.right))


        merge_key_elements = list(map(str, left.union(right)))
        merge_key_elements.sort()
        within_merge_key: str = ",".join(merge_key_elements)
        new_props = list(right.union(left))
        new_props.sort(key=str)
        new_properties: str = ", ".join(
            map(lambda ref: f"{pascalcase(ref)} = {ref}", map(str, new_props)))
        new_label: str = pascalcase(within_merge_key)

        i += 1

        # # # # # # # # # #
        #  ψ_L1 (psi_L1)  #
        # # # # # # # # # #
        if within_dep.is_within_node and len(left) > 0 and len(right) > 0:
            node: Node = within_dep.right.pop().get_graph_object()


            #count = _apply_transformation_rule(
            within_rules.append(Rule(f'''
                        {within_dep.pattern.to_gql_match_where_string()} 
                        GENERATE
                        (x = ({within_merge_key}):{new_label} {{
                        {new_properties}
                        }})
                                '''))  # Create new nodes for dep., nodes with same values for properties on left side should be merged!

            #_apply_transformation_query(
            within_queries.append(f"""
                        {within_dep.pattern.to_gql_match_where_string()} 
                        MATCH (x{i}:{new_label})
                        WHERE {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = {ref}", map(str, right.union(left))))}
                        MERGE ({node.symbol})-[:{new_label.upper()}]->(x{i})
                                """)  # Connect the new nodes with the existing nodes

        #    pattern += f", ({node.symbol})-[:{new_label.upper()}]->(x{i}:{new_label})"

            # Remove old redundant properties in the end
            cleanup_pattern = within_dep.pattern.to_gql_match_where_string().split("WHERE")[0]
            cleanup_queries.append(f"""
                        {cleanup_pattern} 
                        REMOVE {", ".join(map(str, right.union(left)))}
                                """)

            within_dep.pattern.properties -= right
            within_dep.pattern.properties -= left

            transformed_deps_list.append(f"""
            (x{i}:{new_label}:{"&".join(map(pascalcase, map(str, right.union(left))))})
            ::
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left)))}
=>{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, right)))}""".replace(" ","").replace("\n",""))

            applied_transformations.append(("within1",0))


        # # # # # # # # # #
        #  ψ_L2 (psi_L2)  #
        # # # # # # # # # #
        elif within_dep.is_within_edge and len(left) > 0 and len(right) > 0:  # ψ_L2 (psi_L2)  --> Reification
            edge: Edge = within_dep.right.pop().get_graph_object()

            # First reification
            #_apply_transformation_query(
            within_queries.append(f"""
{within_dep.pattern.to_gql_match_where_string()} 
CREATE ({edge.src.symbol})-[:$("SRC_"+type({edge.symbol}))]->(x{i}:$(type({edge.symbol})))
CREATE (x{i})-[:$("TGT_"+type({edge.symbol}))]->({edge.tgt.symbol})
SET x{i} += properties({edge.symbol})
                                """)  # relies on Neo4j >= 5.26

            cleanup_queries.append(f"""
{within_dep.pattern.to_gql_match_where_string()}
DELETE {edge.symbol}
""")
         #   pattern = re.sub(f"\\[{edge.symbol}\\]", f"[]->({edge.symbol})-[]", pattern)

            # Then normalization
            #_apply_transformation_rule(
            within_rules.append(Rule(f"""
                        {within_dep.pattern.to_gql_match_where_string()} 
                        GENERATE
                        (y = ({within_merge_key}) :{new_label} {{{new_properties}}})
                        """))  # nodes with same values for properties on left side should be merged!


            within_queries.append(f"""
                        {within_dep.pattern.to_gql_match_where_string()} 
                        MATCH (x{i}:{new_label})
                        MATCH (old:$(type({edge.symbol})))
                        WHERE {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = old.{ref.split(".")[1]}", map(str, left.union(right))))}
                        MERGE (old) - [:{new_label.upper()}]->(x{i})
                        """)  # Connect normalized nodes with reified nodes and remove redundant properties

            # MATCH(x
            # {i}: {new_label})
            # WHERE
            # {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = {ref}", map(str, local_dep.get_references())))}
            # MERGE({edge.symbol}) - [: {new_label.upper()}]->(x{i})
            # REMOVE
            # {", ".join(map(str, local_dep.get_references()))}

            cleanup_pattern = within_dep.pattern.to_gql_match_where_string().split("WHERE")[0]



            cleanup_queries.append(f"""
                                    {cleanup_pattern} 
                                    REMOVE {", ".join(map(str, left.union(right)))}
                                    """)  # Connect normalized nodes with reified nodes and remove redundant properties

            cleanup_queries.append(f"""
                        MATCH ({edge.symbol}) - [:{new_label.upper()}]->(x{i})
                                                REMOVE {", ".join(map(str, left.union(right)))}
                                                """)  # Connect normalized nodes with reified nodes and remove redundant properties

            transformed_deps_list.append(f"""
                        ({edge.symbol})-[:{new_label.upper()}]->(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, right.union(left))))})
                        ::
            {",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left)))}
            =>{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, right)))}""".replace(" ", "").replace("\n",
                                                                                                                  ""))

            applied_transformations.append(("within2", 2))

        i += 1

    transformation = Transformation(within_rules)
    logging.info("Created transformations, start applying them")
    t = transformation.apply_on(con)
    logging.info("Applied transformations, start clean up")
    transformation.eject()
    logging.info("Finished transformations")

    for inter_query in tqdm(within_queries, desc="Query"):
        _apply_transformation_query(inter_query)
    for query in tqdm(cleanup_queries, desc="Cleanup"):
        with driver.session(database=database) as session:
            session.run(query)

    transformed_deps = DependencySet.from_string_list(transformed_deps_list)



    return transformed_deps, applied_transformations
