import re
from typing import Literal

from caseconverter import pascalcase
from dtgraph import Rule, Transformation
from dtgraph.backend.neo4j.graph import Neo4jGraph
from neo4j import GraphDatabase, Driver

from slpgd import DependencySet, Dependency, Node


def perform_graph_native_normalization(driver: Driver, database: Literal["memgraph"] | str,
                                       provided_dependencies: DependencySet, semantics: int) -> DependencySet:

    # Create a DTGraph Neo4jGraph instance with a non-sense driver
    con = Neo4jGraph("URI", database="DATABASE", username="USERNAME", password="PASSWORD")
    con.driver = driver # Replace the driver with the actual driver

    def _apply_transformation_rule(rule: Rule):
        transformation = Transformation([rule])
        transformation.apply_on(con)
        transformation.eject()

    def _apply_transformation_query(query: str):
        with GraphDatabase.driver(URI, auth=auth if database == "neo4j" else None) as driver:
            with driver.session(database=DATABASE) as session:
                session.run(query)

    pattern = str(provided_dependencies.dependency_pattern)

    print(semantics)
    i = 0

    # Get canonical cover of dependencies
    minimal_dep_set: DependencySet = provided_dependencies.get_minimal_cover()
    transformed_deps_list: list[str] = []

    cleanup_queries: list[str] = []

    # Global
    global_deps: set[Dependency] = set(
        filter(lambda dep: dep.is_inter_graph_object, minimal_dep_set)
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

    local_deps: set[Dependency] = set(filter(lambda dep: dep.is_intra_graph_object, minimal_dep_set))
    for local_dep in local_deps:
        local_dep_left_concat: str = ",".join(map(str, local_dep.left))
        new_properties: str = ", ".join(
            map(lambda ref: f"{pascalcase(ref)} = {ref}", map(str, local_dep.get_references())))
        new_label: str = pascalcase(" ".join(map(str, local_dep.get_references())))

        # # # # # # # # # #
        #  ψ_L1 (psi_L1)  #
        # # # # # # # # # #
        if local_dep.involves_only_nodes:
            node: Node = local_dep.right.reference.graphObject

            _apply_transformation_rule(Rule(f'''
                        MATCH {pattern.replace("&", ":")} 
                        GENERATE
                        (x = ({local_dep_left_concat}):{new_label} {{
                        {new_properties}
                        }})
                                '''))  # Create new nodes for dep., nodes with same values for properties on left side should be merged!

            _apply_transformation_query(f"""
                        MATCH {pattern.replace("&", ":")} 
                        MATCH (x{i}:{new_label})
                        WHERE {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = {ref}", map(str, local_dep.get_references())))}
                        MERGE ({node.symbol})-[:{new_label.upper()}]->(x{i})
                                """)

            pattern += f", ({node.symbol})-[:{new_label.upper()}]->(x{i}:{new_label})"

            # Remove old redundant properties in the end
            cleanup_queries.append(f"""
                        MATCH {pattern.replace("&", ":")} 
                        REMOVE {", ".join(map(str, local_dep.get_references()))}
                                """)
            transformed_deps_list.append(f"""
{",".join(map(lambda ref: f"x{i}.{pascalcase(ref)}", map(str, local_dep.left)))}
->x{i}.{pascalcase(str(local_dep.right.reference))}""")


        # # # # # # # # # #
        #  ψ_L2 (psi_L2)  #
        # # # # # # # # # #
        if local_dep.involves_only_edges:  # ψ_L2 (psi_L2)  --> Reification
            edge: Edge = local_dep.right.reference.graphObject

            # First reification
            _apply_transformation_query(f"""
                        MATCH {pattern.replace("&", ":")} 
                        CREATE ({edge.src.symbol})-[:$("SRC"+type({edge.symbol}))]->(x{i}:$(type({edge.symbol})))
                        CREATE (x{i})-[:$("TGT"+type({edge.symbol}))]->({edge.tgt.symbol})
                        SET x{i} += properties({edge.symbol})
                        DELETE {edge.symbol}
                                """)  # relies on Neo4j >= 5.26
            pattern = re.sub(f"\\[{edge.symbol}\\]", f"[]->({edge.symbol})-[]", pattern)

            # Then normalization
            _apply_transformation_rule(Rule(f"""
                        MATCH {pattern.replace("&", ":")} 
                        GENERATE
                        (y = ({local_dep_left_concat}) :{new_label} {{{new_properties}}})
                        """))  # nodes with same values for properties on left side should be merged!

            cleanup_queries.append(f"""
                        MATCH {pattern.replace("&", ":")} 
                        MATCH (x{i}:{new_label})
                        WHERE {" AND ".join(map(lambda ref: f"x{i}.{pascalcase(ref)} = {ref}", map(str, local_dep.get_references())))}
                        MERGE ({edge.symbol})-[:{new_label.upper()}]->(x{i})
                        REMOVE {", ".join(map(str, local_dep.get_references()))}
                        """)  # Connect normalized nodes with reified nodes and remove redundant properties

        i += 1


    for query in cleanup_queries:
        with GraphDatabase.driver(URI, auth=auth if database == "neo4j" else None) as driver:
            with driver.session(database=DATABASE) as session:
                session.run(query)

    provided_dependencies = DependencySet.from_string_list(list(map(lambda x: f"{pattern}:{x}", transformed_deps_list)))
    return provided_dependencies
