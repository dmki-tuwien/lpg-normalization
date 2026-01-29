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
from tqdm_loggable.auto import tqdm

import gnfd

from constants import *
from normalize import perform_graph_native_normalization
from gnfd import DependencySet

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
                                             SUBSET_COL,
                                             MINIMUM_COVER_COL,
                                             RUN_ID_COL])
per_dep_metrics_df = pd.DataFrame(columns=[GRAPH_COL,
                                           DATABASE_COL,
                                           DEPENDENCY_COL,
                                           METHOD_COL,
                                           MAX_INC_COUNT_COL,
                                           AVG_INC_COUNT_COL,
                                           MINIMALITY_COL,
MINIMALITY_CLUSTER_COL,
MINIMALITY_MATCHES_COL,
                                           RED_COUNT_COL])
graph_overview_df = pd.DataFrame(columns=[GRAPH_COL,
                                          GRAPH_SOURCE_COL,
NODE_COUNT_COL,
EDGE_COUNT_COL,
LABEL_COUNT_COL,
TYPES_COUNT_COL,
                                          NO_INTER_GRAPH_DEPS_COL,
                                          NO_INTRA_GRAPH_DEPS_COL,
                                          ORIGIN_OF_DEPS_COL,
                                          ORIGINAL_NF_COL,
                                          LP_POSSIBLE_COL])

# Keeps track if graph overview has been assessed
_created_graph_overview: list = []

setup: dict
"""The configuration of the evaluation. Defines the used datasets and dependencies."""
with open("setup.yaml", 'r') as file:
    setup = yaml.safe_load(file)

def main():
    test_docker_container_creation()

    logger.info("🚀 Start evaluation")

    if len(setup["graphs"]) < 1:
        logger.error("🔥 \"setup.yaml\" does not contain any graph.")
        exit(1)

    for database in tqdm(["neo4j", "memgraph"], desc="System"):
        for graph in tqdm(setup["graphs"], desc="Graphs"):
            for subset in  tqdm(["all", "within-node", "within-go", "inter-go"], desc="Dep. subset"):
                for algorithm in ["synthesis"]: #,"decomposition"]:
                    for ignore_min_cov in tqdm([True, False], desc="Min. cov."):
                        perform_evaluation(graph, database, subset, algorithm, ignore_min_cov)

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


def perform_evaluation(graph: dict, database: str, subset: str, algorithm: str, ignore_min_cov: bool):
    logger.info(f"\tPerform experiment with graph \"{graph['name']}\", database \"{database}\", subset \"{subset}\", algorithm \"{algorithm}\", and minimal cover ignored \"{ignore_min_cov}\".")
    if subset not in ["within-node", "within-go", "inter-go", "all"] or algorithm not in ["synthesis", "decomposition"]:
        raise ValueError("Illegal argument used for calling \"perform_evaluation\"")
    DATABASE = database
    container: DockerContainer | Neo4jContainer
    """A testcontainer Container of Neo4j or an empty container if Memgraph is used. 
    By using it in a \"with\" clause, testcontainers automatically cleans used containers up."""
    driver: Driver
    """A Neo4J driver connected to the database running in :any:`container`."""

    # 1. Get a fresh database container
    if database == "memgraph":
        container = DockerContainer("alpine")
    else:
        assert database == "neo4j"
        container = Neo4jContainer("neo4j:2025.12-enterprise")
        container.with_volume_mapping(GRAPHS_PATH, "/tmp/graphs") #"/var/lib/neo4j/import/graphs")
        container.with_env("NEO4J_ACCEPT_LICENSE_AGREEMENT", "eval")
        container.with_env("NEO4J_PLUGINS",'["apoc","apoc-extended"]')
        container.with_env("NEO4J_dbms_security_procedures_unrestricted", "apoc.*")
        container.with_env("NEO4J_apoc_export_file_enabled", "true")
        container.with_env("NEO4J_apoc_import_file_enabled", "true")
        container.with_env("NEO4J_AUTH", "neo4j/password")
        container.with_env("NEO4J_server_memory_heap_initial__size", "200G")
        container.with_env("NEO4J_server_memory_heap_max__size", "200G")
        container.with_env("NEO4J_server_memory_pagecache_size", "100G")
        container.with_env("NEO4J_server_thread__pool_global_size","40")
        container.with_env("NEO4J_cypher_parallel__runtime_workers","40")
        container.with_kwargs(nano_cpus=int(40 * 1e9))  # 1 CPU = 1e9 nanocpus

        start_sh: str = "ls -la /var/lib/neo4j/import && cp -R /tmp/graphs /var/lib/neo4j/import &&"
        start_sh += f"chown -R 7474:7474 /var/lib/neo4j/import && ls -la /var/lib/neo4j/import && "
        if "neo4j" in graph.keys() and "from_dump" in graph["neo4j"].keys():
            start_sh += f"{{ cat /var/lib/neo4j/import/{graph["neo4j"]['from_dump']} | neo4j-admin database load --from-stdin neo4j --overwrite-destination=true ; }} && "
        start_sh += "exec /startup/docker-entrypoint.sh neo4j"

        container.with_command(f'bash -c "{start_sh}"')

    with container:
        if database == "memgraph":
            uri = f"bolt://memgraph:7687"
        if database == "neo4j":
            logger.info("Wait for Neo4J to clean query caches.")
            # Neo4J Enterprise is not immediately coming online (although logs say different things)
            container.waiting_for(LogMessageWaitStrategy("db.clearQueryCaches():"))
            # and even after this additional intermediate log message it takes further ~15 seconds
            if "from_dump" in graph["neo4j"].keys():
                logger.info("Wait 30 seconds for Neo4J to become responsive")
                time.sleep(30)
            else:
                time.sleep(1)

        with container.get_driver() if database == "neo4j" else GraphDatabase.driver(uri, auth=None) as driver:
            # connects to


            # 2. Insert denormalized graph if its loaded from a file
            match database:
                case "memgraph":
                    # We do'n't have a fresh database for memgraph --> delete everything first!
                    with driver.session(database=DATABASE) as session:
                        session.run("MATCH (n) DETACH DELETE n")
                    if "from_file" in graph.keys():
                        file = graph['from_file']
                    elif "memgraph" in graph.keys():
                        file = graph['memgraph']['from_file']
                    else:
                        return
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
                            session.run(f"CALL apoc.cypher.runFile(\"{file}\");")
                        elif "neo4j" in graph.keys() and "from_file" in graph["neo4j"].keys():
                            file = graph['neo4j']['from_file']
                            res = session.run(f"CALL apoc.cypher.runFile(\"{file}\");")
                            pass
                        else:
                            pass # the data has been loaded from the dump!

            provided_dependencies = DependencySet.from_string_list(graph["dependencies"])

            if "minimal_cover" in graph.keys():
                minimal_cover = DependencySet.from_string_list(graph["minimal_cover"])
            else:
                minimal_cover = None

            measured_denormalized = False

            # 3. Get initial statistics
            logger.info("Get statistics")
            get_graph_statistics(driver, graph["name"], "denormalized", database, provided_dependencies, measured_denormalized, subset, algorithm, ignore_min_cov) # None = no normalization performed yet --> TODO: Enum?
            measured_denormalized = True # Measurements for denormalized graphs have been taken and are not performed again

            logger.info("Start normalization")
            normalized_deps, transformations = perform_graph_native_normalization(driver,
                                                                       DATABASE,
                                                                       provided_dependencies if ignore_min_cov or minimal_cover is None else minimal_cover, # a minimal cover is used if it is present and not to be ignored
                                                                       dep_filter=subset)



            # 5. Get statistics after normalization
            get_graph_statistics(driver, graph["name"], f"{subset} {algorithm} ignoreMinCov{ignore_min_cov}", database, normalized_deps, measured_denormalized, subset, algorithm, ignore_min_cov)
            # TODO replace with transformed dependencies

            #input("Press any key to continue...")

    logger.info(f"\tFinished experiment with graph \"{graph['name']}\"")


def get_graph_statistics(driver, graph_name: str, method: str | None, database: str, dependencies: DependencySet, measured_denormalized, subset: str, algorithm: str, ignore_min_cov: bool) -> None:
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
                                       SUBSET_COL: subset,
                                       MINIMUM_COVER_COL: ignore_min_cov,
                                       RUN_ID_COL: RUN_ID
                                       })

    statistics_df = pd.DataFrame(statistics_res)

    if method == "denormalized":
        timestamp = time.time_ns()

    statistics_df[TIMESTAMP_COL] = pd.to_datetime(timestamp)

    # # # # # # # # # # # # # # # # # # # # #
    # Retrieve overview on Graphs based on setup.yaml (--> Table 2 in Paper)
    # # # # # # # # # # # # # # # # # # # # #
    global _created_graph_overview
    if not measured_denormalized and database == "neo4j" and graph_name not in _created_graph_overview:
        logger.info("    Get graph overview")
        _created_graph_overview.append(graph_name)
        with driver.session() as session:
            result = session.run("CALL apoc.meta.stats()")
            record = result.single()
            if record is not None:
                graph_setup = next(filter(lambda x: x["name"] == graph_name , setup["graphs"]))
                dependencies = gnfd.DependencySet.from_string_list(graph_setup["dependencies"])
                inter_deps_count = sum(map(lambda dep: dep.is_inter_graph_object, dependencies))
                within_deps_count = sum(map(lambda dep: dep.is_within_graph_object, dependencies))
                overview_res.append({GRAPH_COL: graph_name,
                                     GRAPH_SOURCE_COL: graph_setup["source"] if "source" in graph_setup.keys() is not None else "unknown",
                                     NODE_COUNT_COL: record["nodeCount"] if "nodeCount" in record.keys() else "unknown",
                                         EDGE_COUNT_COL: record["relCount"] if "relCount" in record.keys() else "unknown",
                                     LABEL_COUNT_COL: record["labelCount"] if "labelCount" in record.keys() else "unknown",
                                         TYPES_COUNT_COL: record["relTypeCount"] if "relTypeCount" in record.keys() else "unknown",
                                     NO_INTER_GRAPH_DEPS_COL: inter_deps_count,
                                     NO_INTRA_GRAPH_DEPS_COL: within_deps_count,
                                     ORIGIN_OF_DEPS_COL: graph_setup["dependency_origin"] if "dependency_origin" in graph_setup.keys() is not None else "unknown",
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
        logger.info(f"    Get per dep. metrics for {str(dep)}")
        with driver.session() as session:
            c = 0
            e = 0

            m5 = 0
            m6 = 0
            m8 = 0


            # µ5
            logger.info("        µ5")
            mu5 = f"""
            {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH  
            {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))}, 
            count(*) AS red
            RETURN max(red) AS res
                                            """
            result = session.run(mu5)
            record = result.single()
            if record is not None:
                m5 = record["res"]


            # µ6
            logger.info("        µ6")
            result = session.run(f"""
            {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH  
            {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))}, 
            count(*) AS red
            RETURN avg(red) AS res
                                            """)
            record = result.single()
            if record is not None:
                m6 = record["res"]


            # µ7 == minimality; as defined in "Lisa Ehrlinger and Wolfram Wöß. “A Novel Data Quality Metric for Minimality.” In Data Quality and Trust in Big Data, vol. 11235, Springer, 2019. https://doi.org/10.1007/978-3-030-19143-6_1."
            logger.info("        µ7 Clusters")
            mu7c = f"""
            {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH DISTINCT 
            {",".join(map(lambda left: str(left.to_query_string(database))+" AS x"+pascalcase(str(left)), dep.left))},
            {",".join(map(lambda right: str(right.to_query_string(database))+" AS x"+pascalcase(str(right)), dep.right))}
            RETURN COUNT(*) AS res
            """
            #print(f"µ7 clusters\n=========={µ7c}")
            result = session.run(mu7c)
            record = result.single()
            if record is not None:
                c = record["res"]

            id_func = "elementId" if database == "neo4j" else "id"

            logger.info("        µ7 Elements")
            result = session.run(f"""
            {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH DISTINCT 
            {",".join(map(lambda left: f"toString({id_func}({left.get_graph_object().symbol}))+toStringOrNull({str(left.to_query_string(database))}) AS x{pascalcase(str(left))}", dep.left))},
            {",".join(map(lambda right: f"toString({id_func}({right.get_graph_object().symbol}))+toStringOrNull({str(right.to_query_string(database))}) AS x{pascalcase(str(right))}", dep.right))}
            RETURN COUNT(*) AS res
                            """)
            record = result.single()
            if record is not None:
                e = record["res"]

           # print("µ7c: ", µ7c)

            minimality = 1 if e == 1 else (c - 1) / (e - 1)

            # µ8
            logger.info("        µ8")
            query8 = f"""
            {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH  
            {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left.union(dep.right)))}, 
            count(*) AS red WHERE red > 1
            RETURN sum(red-1) AS res
                            """
            result = session.run(query8)
            record = result.single()
            if record is not None:
                m8 = record["res"]
            else:
                0

        dep_res.append({GRAPH_COL: graph_name,
                        DATABASE_COL: "Neo4J" if database == "neo4j" else "Memgraph",
                        DEPENDENCY_COL: dep.to_latex(),
                        METHOD_COL: method,
                        MAX_INC_COUNT_COL: m5,
                        AVG_INC_COUNT_COL: m6,
                        MINIMALITY_COL: minimality,
                        MINIMALITY_CLUSTER_COL: c,
                            MINIMALITY_MATCHES_COL: e,
                        RED_COUNT_COL: m8,
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
