import logging
import os
import time
import uuid
from typing import Literal

import neo4j.exceptions
import yaml
import pandas as pd
import duckdb

from caseconverter import pascalcase
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.neo4j import Neo4jContainer

from neo4j import GraphDatabase, Query, Driver
from dotenv import load_dotenv
from tqdm_loggable.auto import tqdm

import gofd

from constants import *
from normalize import perform_graph_native_normalization
from gofd import DependencySet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
neo4j_log = logging.getLogger("neo4j")
"""The logger used by the Neo4J Python driver. Not to confuse with actual Neo4J instances!"""
neo4j_log.setLevel(logging.INFO)

load_dotenv()  # Required to get content of .env when not using Docker

GRAPHS_PATH = "./graphs" if os.getenv("GRAPHS_PATH") is None else os.getenv("GRAPHS_PATH")


# Memgraph Connection
MEMGRAPH_DATABASE = (
    "memgraph"
    if os.getenv("MEMGRAPH_DATABASE") is None
    else os.getenv("MEMGRAPH_DATABASE")
)
MEMGRAPH_URI = (
    "bolt://localhost:7688"
    if os.getenv("MEMGRAPH_URI") is None
    else os.getenv("MEMGRAPH_URI")
)

# Neo4J Connection
NEO4J_URI = (
    "neo4j://localhost" if os.getenv("NEO4J_URI") is None else os.getenv("NEO4J_URI")
)
NEO4J_DATABASE = (
    "neo4j" if os.getenv("NEO4J_DATABASE") is None else os.getenv("NEO4J_DATABASE")
)
NEO4J_HEAP_SIZE: str = "1" if os.getenv("NEO4J_HEAP_SIZE") is None else os.getenv("NEO4J_HEAP_SIZE")
NEO4J_PAGECACHE_SIZE: str = "5" if os.getenv("NEO4J_PAGECACHE_SIZE") is None else os.getenv("NEO4J_PAGECACHE_SIZE")
NEO4J_PLUGINS_PATH: str = "plugins" if os.getenv("NEO4J_PLUGINS_PATH") is None else os.getenv("NEO4J_PLUGINS_PATH")

NUMBER_OF_RUNS = 1 if os.getenv("RUNS") is None else int(os.getenv("RUNS"))
"""Number of evaluation runs."""

# Database authentication
USERNAME = (
        "neo4j" if os.getenv("USERNAME") is None else os.getenv("USERNAME")
)
PASSWORD = (
        "password" if os.getenv("PASSWORD") is None else os.getenv("PASSWORD")
)

RUN_ID = None
"""The unique ID of one evaluation run. One evaluation session can consist of multiple runs."""

SESSION_ID = uuid.uuid4()
"""The unique ID of one evaluation session. One evaluation session can consist of multiple runs."""

SETUP_FILE: str = (
        "setup.yaml" if os.getenv("SETUP_FILE") is None else os.getenv("SETUP_FILE")
)
"""Path to the YAML file containing the evaluation setup."""

STOP = my_env = os.getenv("STOP", 'False').lower() in ('true', '1', 't', 'yes')
if STOP:
    NUMBER_OF_RUNS = 1

DUCKDB_CON = duckdb.connect("out/eval_results.duckdb")


# Statistics and Metrics Export configuration
per_graph_metrics_df = pd.DataFrame(
    columns=[
        GRAPH_COL,
        METHOD_COL,
        METRIC_COL,
        VALUE_COL,
        TIMESTAMP_COL,
        DATABASE_COL,
        SUBSET_COL,
        MINIMUM_COVER_COL,
        RUN_ID_COL,
    ]
)
per_dep_metrics_df = pd.DataFrame(
    columns=[
        GRAPH_COL,
        DATABASE_COL,
        DEPENDENCY_COL,
        METHOD_COL,
        MAX_INC_COUNT_COL,
        AVG_INC_COUNT_COL,
        MINIMALITY_COL,
        MINIMALITY_CLUSTER_COL,
        MINIMALITY_MATCHES_COL,
    ]
)


# Keeps track if graph overview has been computed for a graph
_created_graph_overview: list = []

setup: dict
"""The configuration of the evaluation. Defines the used datasets and dependencies."""
with open(SETUP_FILE, "r") as file:
    setup = yaml.safe_load(file)


def main():
    test_docker_container_creation()
    setup_duckdb(DUCKDB_CON)

    logger.info(f"🚀 Start evaluation. Session ID: {SESSION_ID}")

    if len(setup["graphs"]) < 1:
        logger.error('🔥 "setup.yaml" does not contain any graph. No evaluation is performed.')
        exit(1)

    for _ in tqdm(range(NUMBER_OF_RUNS), desc="Run"):
        global RUN_ID
        RUN_ID = uuid.uuid4()

        for database in tqdm(["memgraph", "neo4j"], desc="System"):
            for graph in tqdm(setup["graphs"], desc="Graphs"):
                if STOP:
                    subsets = ["all"]
                else:
                    subsets = ["all",
                               "within-node",
                               "within-edge",
                               "within-graph-object",
                               "between-graph-object",
                               "with-reification"]
                for subset in tqdm(
                    subsets, desc="Dep. subset"
                ):
                    for algorithm in ["graph-native"]:
                        for ignore_min_cov in [False]: #tqdm([True, False], desc="Min. cov."):
                            perform_evaluation(
                                graph, database, subset, algorithm, ignore_min_cov
                            )

    logger.info("✅ Finished evaluation")





def perform_evaluation(
    graph: dict, database: Literal["neo4j", "memgraph"], subset: str, algorithm: str, ignore_min_cov: bool
):
    logger.info(
        f"\tPerform experiment with graph \"{graph['name']}\", database \"{database}\", subset \"{subset}\", algorithm \"{algorithm}\", and minimal cover ignored \"{ignore_min_cov}\"."
    )
    if subset not in [
        "all",
        "within-node",
        "within-edge",
        "within-graph-object",
        "between-graph-object",
        "with-reification"
    ] or algorithm not in ["graph-native", "lp", "structural"] or database not in ["neo4j", "memgraph"]:
        raise ValueError('Illegal argument used for calling "perform_evaluation"')

    container: DockerContainer | Neo4jContainer
    """A testcontainer Container of Neo4j or an empty container if Memgraph is used. 
    By using it in a \"with\" clause, testcontainers automatically cleans used containers up."""

    driver: Driver
    """A Neo4J driver connected to the database running in :any:`container`."""

    is_based_on_neo4j_dump: bool = "memgraph" not in graph.keys() and "from_file" not in graph.keys()
    """Whether the currently considered graph is based on a Neo4j dump."""

    # 1. Get a fresh database container
    if database == "memgraph" and not is_based_on_neo4j_dump:
        container = DockerContainer("alpine")
    else:
        assert database == "neo4j" or (database == "memgraph" and is_based_on_neo4j_dump)
        container = Neo4jContainer("neo4j:2026.06-enterprise")
        container.with_volume_mapping(
            GRAPHS_PATH, "/tmp/graphs"
        )  # "/var/lib/neo4j/import/graphs")
        container.with_volume_mapping(NEO4J_PLUGINS_PATH,"/plugins","rw")
        container.with_bind_ports(7687, 7687)
        container.with_env("NEO4J_ACCEPT_LICENSE_AGREEMENT", "eval")
        container.with_env("NEO4J_PLUGINS", '["apoc","apoc-extended"]')
        container.with_env("NEO4J_dbms_security_procedures_unrestricted", "apoc.*")
        container.with_env("NEO4J_apoc_export_file_enabled", "true")
        container.with_env("NEO4J_apoc_import_file_enabled", "true")
        container.with_env("NEO4J_AUTH", "neo4j/password")
        container.with_env("NEO4J_server_memory_heap_initial__size", f"{NEO4J_HEAP_SIZE}G")
        container.with_env("NEO4J_server_memory_heap_max__size", f"{NEO4J_HEAP_SIZE}G")
        container.with_env("NEO4J_server_memory_pagecache_size", f"{NEO4J_PAGECACHE_SIZE}G")
        container.with_kwargs(nano_cpus=int(4 * 1e9))  # 1 CPU = 1e9 nanocpus

        start_sh: str = (
            "cp -R /tmp/graphs /var/lib/neo4j/import &&"
        )
        start_sh += f"chown -R 7474:7474 /var/lib/neo4j/import && "
        if "neo4j" in graph.keys() and "from_dump" in graph["neo4j"].keys():
            start_sh += f"{{ cat /var/lib/neo4j/import/{graph["neo4j"]['from_dump']} | neo4j-admin database load --from-stdin neo4j --overwrite-destination=true ; }} && "
        start_sh += "exec /startup/docker-entrypoint.sh neo4j"

        container.with_command(f'bash -c "{start_sh}"')

    # 2. Wait for the container to become responsive
    with container:
        if database == "memgraph":
            uri = MEMGRAPH_URI
            if is_based_on_neo4j_dump:
                logger.info("Start Neo4J for data import to Memgraph.")
        if database == "neo4j" or is_based_on_neo4j_dump:
            logger.info("⏳ Wait for Neo4J to clean query caches.")
            # Neo4J Enterprise is not immediately coming online (although logs say different things)
            container.waiting_for(LogMessageWaitStrategy("db.clearQueryCaches():"))
            # and even after this additional intermediate log message it takes further ~15 seconds

            i = 0
            with tqdm(desc="⏳ Wait for Neo4j to become responsive", initial=i) as t:
                responsive = False
                while not responsive:
                    responsive = True

                    try:
                        with container.get_driver() as d:
                            with d.session(database="neo4j") as session:
                                session.run("MATCH (n) RETURN n LIMIT 1")
                    except neo4j.exceptions.DatabaseUnavailable:
                        # Neo4j is not responsible je
                        responsive = False
                        time.sleep(1)
                        i += 1
                        t.update(i)
                t.postfix = "✅ Neo4j is now responsive"


        with (
            container.get_driver()
            if database == "neo4j"
            else GraphDatabase.driver(uri, auth=None)
        ) as driver:
            # connects to

        # 2. Insert denormalized graph if its loaded from a file
            match database:
                case "memgraph":
                    # We do'n't have a fresh database for memgraph --> delete everything first!
                    with driver.session(database=database) as session:

                        responsive = False
                        i = 0
                        with tqdm(desc="Memgraph cleanup", initial=i) as t:
                         #   for s in (["MATCH (n) DETACH DELETE n", "DROP ALL INDEXES", "DROP ALL CONSTRAINTS"]):
                            for s in (["STORAGE MODE IN_MEMORY_ANALYTICAL", "DROP GRAPH", "STORAGE MODE IN_MEMORY_TRANSACTIONAL"]):
                                session.run(s)

                                while not responsive:
                                    responsive = True

                                    try:
                                        session.run("MATCH (n) RETURN n LIMIT 1")
                                    except neo4j.exceptions.TransientError:
                                        responsive = False
                                        time.sleep(1)
                                        i += 1
                                        t.update(i)
                    if "from_file" in graph.keys():
                        file = graph["from_file"]
                    elif "memgraph" in graph.keys():
                        file = graph["memgraph"]["from_file"]
                    else:
                        logger.info("Stream data from Neo4J into Memgraph")
                        if (
                            "neo4j" in graph.keys()
                            and "from_file" in graph["neo4j"].keys()
                        ):
                            with container.get_driver() as neo4j_driver:
                                with neo4j_driver.session() as session:
                                    session.run(
                                        f"CALL apoc.cypher.runFile(\"{graph['neo4j']['from_file']}\");"
                                    )
                        with driver.session(database=database) as session:
                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run("CREATE INDEX ON :__MigrationNode__;")
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run("CREATE INDEX ON :__MigrationNode__(__elementId__);")
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run(f"""
                            CALL migrate.neo4j("MATCH (n) RETURN labels(n) AS src_labels, elementId(n) AS src_id, properties(n) AS src_props", {{host: "{container.get_container_host_ip()}", port: {container.get_exposed_port(7687)}, username: "neo4j", password: "password"}})
                            YIELD row
                            MERGE (n:__MigrationNode__ {{__elementId__: row.src_id}})
                            SET n:row.src_labels
                            SET n += row.src_props; """)
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run(f"""
                            CALL migrate.neo4j(
                              "MATCH (n)-[r]->(m) RETURN type(r) as rel_type, elementId(n) AS src_id, elementId(m) AS dest_id, properties(r) AS edge_props",
                              {{host: "{container.get_container_host_ip()}", port: {container.get_exposed_port(7687)}, username: "neo4j", password: "password"}})
                            YIELD row
                            MATCH (n:__MigrationNode__ {{__elementId__: row.src_id}})
                            MATCH (m:__MigrationNode__ {{__elementId__: row.dest_id}})
                            CREATE (n)-[r:row.rel_type]->(m)
                            SET r += row.edge_props;""")
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run("""
                            MATCH (n:__MigrationNode__)
                            REMOVE n:__MigrationNode__
                            REMOVE n.__elementId__;""")
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run("DROP INDEX ON :__MigrationNode__;")
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run("DROP INDEX ON :__MigrationNode__(__elementId__);")
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            responsive = False

                            while not responsive:
                                responsive = True

                                try:
                                    session.run("MATCH (n) RETURN n LIMIT 1")
                                except neo4j.exceptions.TransientError:
                                    responsive = False
                                    time.sleep(2)

                            logger.info("Importing data from Neo4J to Memgraph finished.")

                    if not is_based_on_neo4j_dump:
                        with open(file, "r") as filename:
                            create_graph_queries_str = filename.read()
                            create_graph_queries = [
                                s.strip()
                                for s in (create_graph_queries_str.split(";"))
                                if s.strip()
                            ]

                            with driver.session(database=database) as session:
                                for query in create_graph_queries:
                                    #   print(query)
                                    session.run(query)
                case _:
                    assert database == "neo4j"
                    with driver.session(database=database) as session:
                        res = session.run(
                            """CALL dbms.listConfig() YIELD name, value 
WHERE name CONTAINS 'memory.pagecache.size' 
RETURN value"""
                        )
                        record = res.single()
                        if record is not None:
                            logger.info(
                                f"Available Pagecache Memory: {record['value']}"
                            )

                        if "from_file" in graph.keys():
                            session.run(
                                f"CALL apoc.cypher.runFile(\"{graph['from_file']}\");"
                            )
                        elif (
                            "neo4j" in graph.keys()
                            and "from_file" in graph["neo4j"].keys()
                        ):
                            session.run(
                                f"CALL apoc.cypher.runFile(\"{graph['neo4j']['from_file']}\");"
                            )
                            pass
                        else:
                            pass  # the data has been loaded from the dump!

            provided_dependencies = DependencySet.from_string_list(
                graph["dependencies"]
            )

            if "minimal_cover" in graph.keys():
                minimal_cover = DependencySet.from_string_list(graph["minimal_cover"])
            else:
                minimal_cover = None

            measured_denormalized = False

        # 4. Get initial statistics
            logger.info("Get statistics")
            calculate_metrics(
                driver,
                graph["name"],
                "denormalized",
                database,
                provided_dependencies,
                measured_denormalized,
                subset,
                ignore_min_cov,
            )  # None = no normalization performed yet
            measured_denormalized = True  # Measurements for denormalized graphs have been taken and are not performed again

            if STOP:
                input(f"Loaded graph {graph["name"]}. Press enter to continue ... ")

            logger.info(f"Start normalization; method: {algorithm}")
            normalized_deps, transformations = perform_graph_native_normalization(
                driver,
                database,
                (
                    provided_dependencies
                    if ignore_min_cov or minimal_cover is None
                    else minimal_cover
                ),  # a minimal cover is used if it is present and not to be ignored
                dep_filter=subset,
            )

            # 5. Get statistics after normalization
            calculate_metrics(
                driver,
                graph["name"],
                algorithm,
                database,
                normalized_deps,
                measured_denormalized,
                subset,
                ignore_min_cov,
            )

            if STOP:
                input(f"Normalized graph {graph["name"]}. Press enter to continue ... ")

    logger.info(f"✅ Finished experiment with graph \"{graph['name']}\" and method \"{algorithm}\"")


def calculate_metrics(
    driver,
    graph_name: str,
    method: str | None,
    database: Literal["neo4j", "memgraph"],
    dependencies: DependencySet,
    measured_denormalized,
    subset: str,
    ignore_min_cov: bool,
) -> None:
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
        # Take the timestamp asap after normalization
        timestamp = time.time_ns()
    statistics_res: list[dict] = []
    dep_res: list[dict] = []

    # # # # # # # # # # # # # # # #
    # Retrieve per graph metrics  #
    # # # # # # # # # # # # # # # #

    # it is important that all queries return under the name "res"
    statistics_def: list[tuple[str, str]] = [  # In the paper:
        (r"NodeCount", "MATCH (n) RETURN COUNT(n) as res"),  #  µ1
        (r"EdgeCount", "MATCH ()-[e]->() RETURN COUNT(e) as res"),  #  µ2
        (
            r"AvgNodePropCount",
            "MATCH (n) RETURN avg(size(keys(properties(n)))) AS res",
        ),  #  µ3
        (
            r"AvgEdgePropCount",
            "MATCH ()-[e]->() RETURN avg(size(keys(properties(e)))) AS res",
        ),  #  µ4
        #     ("NodePropCount", "MATCH (n) RETURN size(keys(properties(n))) AS res"),
        #     ("EdgePropCount", "MATCH ()-[e]->() RETURN size(keys(properties(e))) AS res"),
    ]

    with driver.session() as session:
        for statistic_def in statistics_def:
            query = Query(statistic_def[1])
            result = session.run(query)
            record = result.single()
            if record is not None:
                DUCKDB_CON.execute(f"""INSERT INTO per_graph_metric 
    ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {METRIC_COL}, {VALUE_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL}) VALUES (?,?,?,?,?,?,?,?,?)""",
                               [SESSION_ID, RUN_ID, graph_name, method, statistic_def[0], record["res"], database, subset, ignore_min_cov])


    # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Retrieve overview on Graphs based on setup.yaml #
    # # # # # # # # # # # # # # # # # # # # # # # # # #
    global _created_graph_overview
    if (
        not measured_denormalized
        and database == "neo4j"
        and graph_name not in _created_graph_overview
    ):
        logger.info("    Get graph overview")
        _created_graph_overview.append(graph_name)
        with driver.session() as session:
            result = session.run("CALL apoc.meta.stats()")
            record = result.single()
            if record is not None:
                graph_setup = next(
                    filter(lambda x: x["name"] == graph_name, setup["graphs"])
                )
                dependencies = gofd.DependencySet.from_string_list(
                    graph_setup["dependencies"]
                )
                between_deps_count = sum(
                    map(lambda dep: dep.is_between_graph_object, dependencies)
                )
                within_deps_count = sum(
                    map(lambda dep: dep.is_within_graph_object, dependencies)
                )
                DUCKDB_CON.execute(f"""INSERT INTO graph_overview 
                ( {SESSION_ID_COL},
                {GRAPH_COL},
                {NODE_COUNT_COL},
                {EDGE_COUNT_COL},
                {LABEL_COUNT_COL},
                {TYPES_COUNT_COL},
                {NO_BETWEEN_GRAPH_DEPS_COL},
                {NO_WITHIN_GRAPH_DEPS_COL},
                {LP_POSSIBLE_COL}) VALUES (?,?,?,?,?,?,?,?,?)""",
                                   [SESSION_ID, graph_name, record["nodeCount"], record["relCount"], record["labelCount"], record["relTypeCount"], between_deps_count, within_deps_count, dependencies.lp_suitable])


    # # # # # # # # # # # # # # # # # # # # #
    # Retrieve per dependency metrics(1 Table and 1 Plot)
    # # # # # # # # # # # # # # # # # # # # #

    i = 0
    with tqdm(desc="Per dependency metric calculation:", initial=0, total=len(dependencies)*3) as t:
        for dep in dependencies:
            logger.info(f"    Get per dep. metrics for {str(dep)}")
            with driver.session() as session:
                c = 0
                e = 0

                # µ5
                t.postfix = "Maximum redundancy potential"
                mu5 = f"""
                {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH  
                {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))}, 
                count(*) AS red
                RETURN max(red) AS res
                                                """
                result = session.run(mu5)
                record = result.single()
                if record is not None:
                    DUCKDB_CON.execute(f"""INSERT INTO per_dep_metric 
                        ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {DEPENDENCY_COL}, {METRIC_COL}, {VALUE_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL}) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                       [SESSION_ID, RUN_ID, graph_name, method, dep.to_latex(), MAX_INC_COUNT_COL, record["res"],
                                        database, subset, ignore_min_cov])
                i += 1
                t.update(i)

                # µ6
                t.postfix = "Average redundancy potential"
                result = session.run(
                    f"""
                {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH  
                {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))}, 
                count(*) AS red
                RETURN avg(red) AS res
                                                """
                )
                record = result.single()
                if record is not None:
                    DUCKDB_CON.execute(f"""INSERT INTO per_dep_metric 
                                            ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {DEPENDENCY_COL}, {METRIC_COL}, {VALUE_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL}) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                       [SESSION_ID, RUN_ID, graph_name, method, dep.to_latex(), AVG_INC_COUNT_COL,
                                        record["res"],
                                        database, subset, ignore_min_cov])
                i += 1
                t.update(i)


                # µ7 == minimality; as defined in "Lisa Ehrlinger and Wolfram Wöß. “A Novel Data Quality Metric for Minimality.” In Data Quality and Trust in Big Data, vol. 11235, Springer, 2019. https://doi.org/10.1007/978-3-030-19143-6_1."
                t.postfix = "Minimality"

                mu7c = f"""
    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} 
    WITH
    DISTINCT 
    {", ".join(map(lambda left: f"{left} as x{pascalcase(str(left))}", dep.left))}, 
    {", ".join(map(lambda right: f"{right} as x{pascalcase(str(right))}", dep.right))}
    RETURN count(*) AS res"""
                print(f"µ7 clusters\n=========={mu7c}")
                result = session.run(mu7c)
                record = result.single()
                if record is not None:
                    c = record["res"]
                    DUCKDB_CON.execute(f"""INSERT INTO per_dep_metric 
                                            ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {DEPENDENCY_COL}, {METRIC_COL}, {VALUE_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL}) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                       [SESSION_ID, RUN_ID, graph_name, method, dep.to_latex(), MINIMALITY_CLUSTER_COL,
                                        record["res"],
                                        database, subset, ignore_min_cov])
                i += 0.5
                t.update(i)

                result = session.run(
                    f"""
    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} 
    WITH
    {", ".join(map(lambda left: f"{left} as x{pascalcase(str(left))}", dep.left))}, 
    {", ".join(map(lambda right: f"{right} as x{pascalcase(str(right))}", dep.right))}
    RETURN count(*) AS res"""
                )
                record = result.single()
                if record is not None:
                    e = record["res"]
                    DUCKDB_CON.execute(f"""INSERT INTO per_dep_metric 
                                                                ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {DEPENDENCY_COL}, {METRIC_COL}, {VALUE_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL}) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                       [SESSION_ID, RUN_ID, graph_name, method, dep.to_latex(), MINIMALITY_MATCHES_COL,
                                        record["res"],
                                        database, subset, ignore_min_cov])

                minimality = 1 if e == 1 else (c - 1) / (e - 1)
                DUCKDB_CON.execute(f"""INSERT INTO per_dep_metric 
                                                            ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {DEPENDENCY_COL}, {METRIC_COL}, {VALUE_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL}) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                   [SESSION_ID, RUN_ID, graph_name, method, dep.to_latex(), MINIMALITY_COL,
                                    minimality,
                                    database, subset, ignore_min_cov])
                i += 0.5
                t.update(i)

            t.postfix = "Finished"



    dep_df = pd.DataFrame(dep_res)
    global per_dep_metrics_df
    per_dep_metrics_df = pd.concat([per_dep_metrics_df, dep_df], ignore_index=True)

    # Add timestamp to dataframe
    statistics_df = pd.DataFrame(statistics_res)


    global per_graph_metrics_df
    per_graph_metrics_df = pd.concat(
        [per_graph_metrics_df, statistics_df], ignore_index=True
    )

    if method == "denormalized":
        timestamp = time.time_ns()

    ts_str = str(pd.Timestamp(timestamp))

    DUCKDB_CON.execute(f"""UPDATE per_graph_metric 
     SET {TIMESTAMP_COL} = (?) WHERE {RUN_ID_COL} = '{RUN_ID}' AND {SESSION_ID_COL} = '{SESSION_ID}' AND {GRAPH_COL} = '{graph_name}' AND {METHOD_COL} = '{method}' AND {SUBSET_COL} = '{subset}'""", [ts_str])
    statistics_df[TIMESTAMP_COL] = pd.to_datetime(timestamp)
    DUCKDB_CON.execute(f"""UPDATE per_dep_metric 
         SET {TIMESTAMP_COL} = (?) WHERE {RUN_ID_COL} = '{RUN_ID}' AND {SESSION_ID_COL} = '{SESSION_ID}' AND {GRAPH_COL} = '{graph_name}' AND {METHOD_COL} = '{method}' AND {SUBSET_COL} = '{subset}'""",
                       [ts_str])
    statistics_df[TIMESTAMP_COL] = pd.to_datetime(timestamp)

def setup_duckdb(con: duckdb.DuckDBPyConnection):
    """Opens the DuckDB and creates the tables if they do not exist yet."""
    con.sql(f"""
    CREATE TABLE IF NOT EXISTS per_graph_metric (
    {SESSION_ID_COL} UUID,
    {RUN_ID_COL} UUID,
    {GRAPH_COL} TEXT,
    {METHOD_COL} TEXT,
    {METRIC_COL} TEXT,
    {VALUE_COL} DOUBLE,
    {TIMESTAMP_COL} TIMESTAMP_NS,
    {DATABASE_COL} TEXT, 
    {SUBSET_COL} TEXT,
    {MINIMUM_COVER_COL} BOOLEAN,
    PRIMARY KEY ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {METRIC_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL})
);""")

    con.sql(f"""
        CREATE TABLE IF NOT EXISTS graph_overview (
        {SESSION_ID_COL} UUID,
        {GRAPH_COL} TEXT,
        {NODE_COUNT_COL} INT,
        {EDGE_COUNT_COL} INT,
        {LABEL_COUNT_COL} INT,
        {TYPES_COUNT_COL} INT,
        {NO_BETWEEN_GRAPH_DEPS_COL} INT,
        {NO_WITHIN_GRAPH_DEPS_COL} INT, 
        {LP_POSSIBLE_COL} BOOLEAN,
        PRIMARY KEY ({SESSION_ID_COL}, {GRAPH_COL})
    );""")

    con.sql(f"""
        CREATE TABLE IF NOT EXISTS per_dep_metric (
        {SESSION_ID_COL} UUID,
        {RUN_ID_COL} UUID,
        {GRAPH_COL} TEXT,
        {METHOD_COL} TEXT,
        {DEPENDENCY_COL} TEXT,
        {METRIC_COL} TEXT,
        {VALUE_COL} DOUBLE,
        {TIMESTAMP_COL} TIMESTAMP_NS,
        {DATABASE_COL} TEXT, 
        {SUBSET_COL} TEXT,
        {MINIMUM_COVER_COL} BOOLEAN,
        PRIMARY KEY ({SESSION_ID_COL}, {RUN_ID_COL}, {GRAPH_COL}, {METHOD_COL}, {DEPENDENCY_COL}, {METRIC_COL}, {DATABASE_COL}, {SUBSET_COL}, {MINIMUM_COVER_COL})
    );""")
def test_connection_to_neo4j(uri: str, username: str = "neo4j", password: str = None):
    """Tests whether a connection to the Neo4j database is successful.

    :param uri: URI of the Neo4j database
    :param username: Username
    :param password: Password"""
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        driver.verify_connectivity()


def test_connection_to_memgraph(uri: str):
    """Tests whether a connection to the Memgraph database is successful.

    :param uri: URI of the Memgraph database"""
    with GraphDatabase.driver(uri) as driver:
        driver.verify_connectivity()


def test_docker_container_creation():
    """Tests whether the `testcontainers` package is able to create Docker containers.
    If the creation failes, the evaluation is exited as no experiments can be run."""
    with tqdm(desc="Startup testing", initial=0, total=1) as t:
        t.postfix = 'Testing Docker container creation'

        with DockerContainer("alpine").with_command(
                "echo 'Hello world!' && tail -f /dev/null"
        ) as container:
            try:
                container.waiting_for(LogMessageWaitStrategy("Hello world!"))
            except Exception:
                logging.error('Running the "Hello World!" Docker container failed; cannot start the evaluation.')
                exit()
        t.update(1)
        t.postfix = 'The "Hello World!" Docker container was run successfully.'


if __name__ == "__main__":
    main()
