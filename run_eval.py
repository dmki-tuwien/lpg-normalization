import logging
import os
import time

import yaml
import pandas as pd

from caseconverter import pascalcase
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.neo4j import Neo4jContainer

from neo4j import GraphDatabase, Query, Driver, Neo4jDriver
from plotnine import *
from dotenv import load_dotenv

import slpgd

from constants import *
from normalize import perform_graph_native_normalization
from slpgd import DependencySet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
neo4j_log = logging.getLogger("neo4j")
"""The logger used by the Neo4J Python driver. Not to confuse with actual Neo4J instances!"""
neo4j_log.setLevel(logging.INFO)

load_dotenv() # Required to get content of .env when not using Docker

GRAPHS_PATH = os.getenv("GRAPHS_PATH")

# Memgraph Connection
MEMGRAPH_DATABASE = "memgraph" if os.getenv("MEMGRAPH_DATABASE") is None else os.getenv("MEMGRAPH_DATABASE")
MEMGRAPH_URI = "bolt://localhost:7688" if os.getenv("MEMGRAPH_URI") is None else os.getenv("MEMGRAPH_URI")

# Neo4J Connection
NEO4J_URI = "neo4j://localhost" if os.getenv("NEO4J_URI") is None else os.getenv("NEO4J_URI")
NEO4J_DATABASE = "neo4j" if os.getenv("NEO4J_DATABASE") is None else os.getenv("NEO4J_DATABASE")

# Statistics and Metrics Export configuration
per_graph_metrics_df = pd.DataFrame(columns=[GRAPH_COL,
                                             METHOD_COL,
                                             METRIC_COL,
                                             VALUE_COL,
                                             TIMESTAMP_COL,
                                             DATABASE_COL,
                                             RUN_ID_COL])
per_dep_metrics_df = pd.DataFrame(columns=[GRAPH_COL,
                                           DATABASE_COL,
                                           DEPENDENCY_COL,
                                           METHOD_COL,
                                           MAX_RED_COUNT_COL,
                                           AVG_RED_COUNT_COL,
                                           MINIMALITY_COL,
                                           MAX_INC_COUNT_COL])
graph_overview_df = pd.DataFrame(columns=[GRAPH_COL,
                                          GRAPH_SOURCE_COL,
                                          NO_INTER_GRAPH_DEPS_COL,
                                          NO_INTRA_GRAPH_DEPS_COL,
                                          ORIGIN_OF_DEPS_COL,
                                          ORIGINAL_NF_COL,
                                          LP_POSSIBLE_COL])


setup: dict
"""The configuration of the evaluation. Defines the used datasets and dependencies."""
with open("setup.yaml", 'r') as file:
    setup = yaml.safe_load(file)

def main():
    # try:
    #     test_connection_to_neo4j()
    # except neo4j.exceptions.ServiceUnavailable:
    #     logger.error("Could not connect to Neo4j")
    #     exit(1)
    # logger.info("✅ Connection to Neo4J was successful")
    #
    # try:
    #     test_connection_to_memgraph()
    # except neo4j.exceptions.ServiceUnavailable:
    #     logger.error("Could not connect to Memgraph")
    #     exit(1)
    # logger.info("✅ Connection to Memgraph was successful")
    #

    test_docker_container_creation()

    logger.info("🚀 Start evaluation")

    if len(setup["graphs"]) < 1:
        logger.error("\"setup.yaml\" does not contain any graph.")
        exit(1)

    for database in ["memgraph", "neo4j"]:
        for graph in setup["graphs"]:
            perform_evaluation(graph, database)

    logger.info("✅ Finished evaluation")

    export_tables_and_plots()



def export_tables_and_plots():
    """Exports the computed statistics as CSV and LaTeX tables, as well as PDF plots (only per graph statistics)."""
    logger.info("📊 Create plot and export CSV results.")
    plot_height = 2 * len(setup["graphs"])
    plot_metrics = (ggplot(per_graph_metrics_df, aes(x=METHOD_COL, y=VALUE_COL, fill=DATABASE_COL))
                    + geom_col(position="dodge")
                    + geom_text(
                aes(label=f"{VALUE_COL}.round(3).astype(str)"),
                nudge_y=0.1,
                size=10,
                va='bottom'
            )
                    + facet_grid(f"{GRAPH_COL} ~ {METRIC_COL}", scales='free_y')
                    #         + scale_y_continuous(limits=(0, max(metrics_df[VALUE_COL])*1.1))  # Set the new upper limit
                    + scale_y_continuous(expand=(0, 0, 0.1, 0))
                    + theme_bw()
                    + theme(axis_text_x=element_text(
                angle=45,
                ha='right'
            ),
                figure_size=(8, plot_height)
            )
                    )

    try:
        os.mkdir("out")
    except FileExistsError:
        pass  # It's fine if the output folder is already there :)

    plot_metrics.save("out/plot.pdf", metadata=PDF_METADATA, verbose=False)

    graph_overview_df.to_csv("out/graph_overview.csv", index=False)
    graph_overview_df.to_latex("out/graph_overview.tex", index=False)

    per_graph_metrics_df.to_csv("out/metrics.csv", index=False)

    global per_dep_metrics_df
    per_dep_metrics_df = per_dep_metrics_df.loc[per_dep_metrics_df[DATABASE_COL] == "Neo4J"]
    per_dep_metrics_df = per_dep_metrics_df.set_index([GRAPH_COL, DATABASE_COL, METHOD_COL, DEPENDENCY_COL])
    per_dep_metrics_df.to_csv("out/per_dep_metrics.csv")
    per_dep_metrics_df.style.format(precision=3).to_latex("out/per_dep_metrics.latex", hrules=True, clines="all;index",
                                                          siunitx=True)


def perform_evaluation(graph: dict, database: str):
    logger.info(f"\tPerform experiment with graph \"{graph['name']}\" and database \"{database}\".")

    DATABASE = database
    container: DockerContainer | Neo4jContainer
    """A testcontainer Container of Neo4j or Memgraph. By using it in a \"with\" clause, testcontainers automatically cleans used containers up."""
    driver: Driver
    """A Neo4J driver connected to the database running in :any:`container`."""

    for method in ["slpgd"]:  # ,"slpgd1","slpgd2"]: #, "semantics1", "semantics2"]: # TODO: Enum?
        # 1. Get a fresh database container
        if database == "memgraph":
            container = DockerContainer("alpine")
        else:
            assert database == "neo4j"
            container = Neo4jContainer("neo4j:2025.11")
            container.with_volume_mapping(GRAPHS_PATH, "/tmp/graphs") #"/var/lib/neo4j/import/graphs")
            container.with_env("NEO4J_PLUGINS",'["apoc","apoc-extended"]')
            container.with_env("NEO4J_dbms_security_procedures_unrestricted", "apoc.*")
            container.with_env("NEO4J_apoc_export_file_enabled", "true")
            container.with_env("NEO4J_apoc_import_file_enabled", "true")

            start_sh: str = "ls -la /var/lib/neo4j/import && cp -R /tmp/graphs /var/lib/neo4j/import &&"

            # # Copy the required file(s) into the newly created Neo4J container
            # if "from_file" in graph.keys():
            #     start_sh += f"cp /tmp/{graph['from_file']} /var/lib/neo4j/import/{graph['from_file']} && "
            # elif "neo4j" in graph.keys() and "from_file" in graph["neo4j"].keys():
            #     start_sh += f"cp /tmp/{graph["neo4j"]['from_file']} /var/lib/neo4j/import/{graph["neo4j"]['from_file']} && "
            # elif "neo4j" in graph.keys() and "from_dump" in graph["neo4j"].keys():
            #     start_sh += f"cp /tmp/{graph["neo4j"]['from_dump']} /var/lib/neo4j/import/{graph["neo4j"]['from_dump']} && "

            start_sh += f"chown -R 7474:7474 /var/lib/neo4j/import && ls -la /var/lib/neo4j/import && "
            if "neo4j" in graph.keys() and "from_dump" in graph["neo4j"].keys():
                start_sh += f"neo4j-admin load --from /var/lib/neo4j/import/{graph["neo4j"]['from_dump']} [--database \"database\"] && "

            start_sh += "exec /startup/docker-entrypoint.sh neo4j"

            container.with_command(f'bash -c "{start_sh}"')

        with container:
            if database == "memgraph":
                uri = f"bolt://memgraph:7687"
                print("Hi from memgraph path")

            with container.get_driver() if database == "neo4j" else GraphDatabase.driver(uri, auth=None) as driver:

                # 2. Insert denormalized graph
                match database:
                    case "memgraph":
                        # We dont have a fresh database for memgraph --> delete everything first!
                        with driver.session(database=DATABASE) as session:
                            session.run("MATCH (n) DETACH DELETE n")
                        if "from_file" in graph.keys():
                            file = graph['from_file']
                        elif "memgraph" in graph.keys():
                            file = graph['memgraph']['from_file']
                        else:
                            break
                        with open(file, 'r') as filename:
                            create_graph_queries_str = filename.read()
                            create_graph_queries = [s.strip() for s in (create_graph_queries_str.split(';')) if s.strip()]

                            with driver.session(database=DATABASE) as session:
                                for query in create_graph_queries:
                                 #   print(query)
                                    session.run(query)
                    case _:
                        with driver.session(database=DATABASE) as session:
                            if "from_file" in graph.keys():
                                file = graph['from_file']
                            elif "neo4j" in graph.keys():
                                file = graph['neo4j']['from_file']
                            else:
                                break
                            res = session.run(f"CALL apoc.cypher.runFile(\"{file}\");")
                            print(res)

                provided_dependencies = DependencySet.from_string_list(graph["dependencies"])

                measured_denormalized = False

                # 3. Get initial statistics
                get_graph_statistics(driver, graph["name"], "denormalized", database, provided_dependencies, measured_denormalized) # None = no normalization performed yet --> TODO: Enum?
                measured_denormalized = True # Measurements for denomalized graphs have been taken and are not performed again


                # 4. Perform normalization

                match method:
                    case "relational":
                        # provided_dependants = provided_dependencies.dependants
                        # with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
                        #     dependencies = DependencySet.from_string_list(graph["dependencies"]).infer_structural_deps(driver, except_dependants=provided_dependants)
                        #     # print(dependencies)
                        #     transformations: list[str]
                        #     new_pattern: str
                        #     transformations, new_pattern = dependencies.get_transformations_rel_synthesize(driver)
                        #     with driver.session(database=NEO4J_DATABASE) as session:
                        #         for transformation in transformations:
                        #         #    print(transformation)
                        #         #    print(new_pattern)
                        #             session.run(transformation)

                        pass
                    case "slpgd" | "slpgd2":
                        semantics = 0
                        if method == "slpgd":
                            semantics = 1
                        else:
                            semantics = 2

                        provided_dependencies = perform_graph_native_normalization(driver, database, DATABASE,
                                                                                   provided_dependencies, semantics)

                    case _:
                        pass

                # 5. Get statistics after normalization
                get_graph_statistics(driver, graph["name"], method, database, provided_dependencies, measured_denormalized)
                # TODO replace with transformed dependencies

                #input("Press any key to continue...")

    logger.info(f"\tFinished experiment with graph \"{graph['name']}\"")


def get_graph_statistics(driver, graph_name: str, method: str | None, database: str, dependencies: DependencySet, measured_denormalized) -> None:
    """
    Calculates statistics about graphs and stores them to global dataframes
    (`:any:graph_overview_df` and `:any:graph_statistics_df`).

    :param graph_name:
    :param method:
    :param database:
    :param measured_denormalized: Flag, whether statistics for denormalized graphs should be measured.
    """



    timestamp: int = 0
    if method != "denormalized":
        timestamp = time.time_ns()
    statistics_res: list[dict] = []
    overview_res: list[dict] = []
    dep_res: list[dict] = []

    # # # # # # # # # # # # # # # # # # # # #
    # Retrieve per graph metrics (1 Table and 1 Plot)
    # # # # # # # # # # # # # # # # # # # # #

    # it is important that all queries return under the name "res"
    statistics_def: list[tuple[str,str]] = [                                                            # In the paper:
        (r"$\mu_1$: NodeCount","MATCH (n) RETURN COUNT(n) as res"),                                       #  µ1
        (r"$\mu_2$: EdgeCount", "MATCH ()-[e]->() RETURN COUNT(e) as res"),                               #  µ2
        (r"$\mu_3$: AvgNodePropCount", "MATCH (n) RETURN avg(size(keys(properties(n)))) AS res"),         #  µ3
        (r"$\mu_4$: AvgEdgePropCount", "MATCH ()-[e]->() RETURN avg(size(keys(properties(e)))) AS res"),  #  µ4
   #     ("NodePropCount", "MATCH (n) RETURN size(keys(properties(n))) AS res"),
   #     ("EdgePropCount", "MATCH ()-[e]->() RETURN size(keys(properties(e))) AS res"),
    ]



    match database:
        case "memgraph":
            URI = MEMGRAPH_URI
            DATABASE = MEMGRAPH_DATABASE
        case _:
            URI = NEO4J_URI
            DATABASE = NEO4J_DATABASE

    with driver.session() as session:
        for statistic_def in statistics_def:
            query = Query(statistic_def[1])
            result = session.run(query)
            record = result.single()
            if record is not None:
                statistics_res.append({GRAPH_COL: graph_name,
                                       METHOD_COL: method,
                                       METRIC_COL: statistic_def[0],
                                       VALUE_COL: record["res"],
                                       DATABASE_COL: database,
                                       RUN_ID_COL: RUN_ID
                                       })

    statistics_df = pd.DataFrame(statistics_res)

    if method == "denormalized":
        timestamp = time.time_ns()

    statistics_df[TIMESTAMP_COL] = pd.to_datetime(timestamp)

    # # # # # # # # # # # # # # # # # # # # #
    # Retrieve overview on Graphs based on setup.yaml (--> Table 2 in Paper)
    # # # # # # # # # # # # # # # # # # # # #
    if not measured_denormalized and database == "neo4j":
        with driver.session() as session:
            result = session.run("CALL apoc.meta.stats()")
            record = result.single()
            if record is not None:
                graph_setup = next(filter(lambda x: x["name"] == graph_name , setup["graphs"]))
                dependencies = slpgd.DependencySet.from_string_list(graph_setup["dependencies"])
                inter_deps_count = sum(map(lambda dep: dep.is_inter_graph_object, dependencies))
                intra_deps_count = sum(map(lambda dep: dep.is_intra_graph_object, dependencies))
                overview_res.append({GRAPH_COL: graph_name,
                                     GRAPH_SOURCE_COL: graph_setup["source"] if "source" in graph_setup.keys() is not None else "unknwon",
                                     NO_INTER_GRAPH_DEPS_COL: inter_deps_count,
                                     NO_INTRA_GRAPH_DEPS_COL: intra_deps_count,
                                     ORIGIN_OF_DEPS_COL: graph_setup["dependency_origin"] if "dependency_origin" in graph_setup.keys() is not None else "unknwon",
                                     ORIGINAL_NF_COL: dependencies.get_normal_form(session),
                                     LP_POSSIBLE_COL: "$\\checkmark$" if dependencies.lp_suitable else "$\\times$",
                                     })
        overview_df = pd.DataFrame(overview_res)
        global graph_overview_df
        graph_overview_df = pd.concat([graph_overview_df, overview_df], ignore_index=True)



    # # # # # # # # # # # # # # # # # # # # #
    # Retrieve per dependency metrics(1 Table and 1 Plot)
    # # # # # # # # # # # # # # # # # # # # #

    for dep in dependencies:
        with driver.session() as session:
            c = 0
            e = 0

            m5 = 0
            m6 = 0
            m8 = 0


            # µ5
            result = session.run(f"""
            MATCH {str(dep.pattern).replace("&", ":")} WITH  
            {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))}, 
            count(*) AS red
            RETURN max(red) AS res
                                            """)
            record = result.single()
            if record is not None:
                m5 = record["res"]


            # µ6
            result = session.run(f"""
            MATCH {str(dep.pattern).replace("&", ":")} WITH  
            {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))}, 
            count(*) AS red
            RETURN avg(red) AS res
                                            """)
            record = result.single()
            if record is not None:
                m6 = record["res"]


            # µ7 == minimality
            µ7c = f"""
            MATCH {str(dep.pattern).replace("&", ":")} WITH DISTINCT 
            {",".join(map(lambda left: str(left.to_query_string(database))+" AS x"+pascalcase(str(left)), dep.left))},
            {dep.right.to_query_string(database)+" AS x"+pascalcase(str(dep.right))}
            RETURN COUNT(*) AS res
            """
            #print(f"µ7 clusters\n=========={µ7c}")
            result = session.run(µ7c)
            record = result.single()
            if record is not None:
                c = record["res"]


            result = session.run(f"""
            MATCH {str(dep.pattern).replace("&", ":")} WITH DISTINCT 
            {",".join(map(lambda left: f"toString(id({left.get_graph_object().symbol}))+toStringOrNull({str(left.to_query_string(database))}) AS x{pascalcase(str(left))}", dep.left))},
            toString(id({dep.right.get_graph_object().symbol}))+toStringOrNull({dep.right.to_query_string(database)}) AS x{pascalcase(str(dep.right))}
            RETURN COUNT(*) AS res
                            """)
            record = result.single()
            if record is not None:
                e = record["res"]

           # print("µ7c: ", µ7c)

            minimality = 1 if e == 1 else (c - 1) / (e - 1)

            # µ8
            result = session.run(f"""
            MATCH {str(dep.pattern).replace("&", ":")} WITH  
            
            {dep.right.to_query_string(database) + " AS x" + pascalcase(str(dep.right))}, count(*) AS red
            RETURN max(red) AS res
                            """)
            record = result.single()
            if record is not None:
                m8 = record["res"]

        dep_res.append({GRAPH_COL: graph_name,
                        DATABASE_COL: "Neo4J" if database == "neo4j" else "Memgraph",
                        DEPENDENCY_COL: dep.to_latex(),
                        METHOD_COL: method,
                        MAX_RED_COUNT_COL: m5,
                        AVG_RED_COUNT_COL: m6,
                        MINIMALITY_COL: minimality,
                        MAX_INC_COUNT_COL: m8,
                        })
            
    dep_df = pd.DataFrame(dep_res)
    global per_dep_metrics_df
    per_dep_metrics_df = pd.concat([per_dep_metrics_df, dep_df], ignore_index=True)


    # Add timestamp to dataframe
    statistics_df = pd.DataFrame(statistics_res)

    if method == "denormalized":
        timestamp = time.time_ns()

    statistics_df[TIMESTAMP_COL] = pd.to_datetime(timestamp)

    global per_graph_metrics_df
    per_graph_metrics_df = pd.concat([per_graph_metrics_df, statistics_df], ignore_index=True)






def test_connection_to_neo4j(uri: str, username: str = "neo4j", password: str = None):
    """Tests whether a connection to the Neo4j database is successful.

    :param uri: URI of the Neo4j database
    :param username: Username
    :param password: Password"""
    with GraphDatabase.driver(uri, auth=(username,password)) as driver:
        driver.verify_connectivity()

def test_connection_to_memgraph(uri):
    with GraphDatabase.driver(uri) as driver:
        driver.verify_connectivity()

def test_docker_container_creation():
    """Tests whether the `testcontainers` package is able to create Docker containers.
    If the creation files the evaluation is exited as no experiments can be run."""
    logging.info("Testing Docker container creation by creating a simple container that logs \"Hello World!\".")
    with DockerContainer("alpine").with_command("echo 'Hello world!' && tail -f /dev/null") as container:
        try:
            container.waiting_for(LogMessageWaitStrategy("Hello world!"))
        except Exception:
            logging.error(f"Running the \"Hello World!\" Docker container failed.")
            exit()
    logging.info(f"The \"Hello World!\" Docker container was run successfully.")


if __name__ == "__main__":
    main()