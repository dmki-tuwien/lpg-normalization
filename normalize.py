import re
from typing import Literal

from caseconverter import pascalcase
from dtgraph import Rule, Transformation
from dtgraph.backend.neo4j.graph import Neo4jGraph
from neo4j import GraphDatabase, Driver

from gnfd import DependencySet, GNFD, Node, Reference, Edge


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
    global_deps: set[GNFD] = set(
        filter(lambda dep: dep.is_inter_graph_object, provided_dependencies)
    )

    # TODO: Add notion of trivial dep to paper!

    for dep in global_deps:
        #             match len(dep.left):
        #                 case 1:
        #                     if isinstance(dep.right, Property):
        #                         transformations.append(
        #                             f"""MATCH {self.dependency_pattern}
        # SET {next(iter(dep.left)).get_graph_object()}.{pascalcase(str(dep.right))}
        # REMOVE {dep.right}"""
        #                         )
        #                 case _:
        #                     pass
        pass




    # # # # # # # # # # # # # # # # # # # # # # #
    #  Local (ψ_L1 (psi_L1) and  ψ_L2 (psi_L2)) #
    # # # # # # # # # # # # # # # # # # # # # # #

    within_rules = []
    within_queries = []
    within_deps: set[GNFD] = set(filter(lambda dep: dep.is_within_graph_object, provided_dependencies))
    for within_dep in within_deps:
        # First filter References that are Graph Object IDs. We don't need them here
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
            {str(within_dep.pattern)},
            ({node.symbol})-[:{new_label.upper()}]->(x{i}:{new_label}:{"&".join(map(pascalcase, map(str, right.union(left))))})
            ::
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, left)))}
=>{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, right)))}""".replace(" ","").replace("\n",""))

            applied_transformations.append(("within1",0))


        # # # # # # # # # #
        #  ψ_L2 (psi_L2)  #
        # # # # # # # # # #
        elif within_dep.is_within_edge:  # ψ_L2 (psi_L2)  --> Reification
            edge: Edge = next(iter(within_dep.right)).reference.graphObject

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
    t = transformation.apply_on(con)
    transformation.eject()

    for within_query in within_queries:
        _apply_transformation_query(within_query)
    for query in cleanup_queries:
        with driver.session(database=database) as session:
            session.run(query)

    transformed_deps = DependencySet.from_string_list(transformed_deps_list)



    return transformed_deps, applied_transformations
