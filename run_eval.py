import logging
import os
import time
import uuid

from caseconverter import pascalcase
import neo4j.exceptions
import yaml
import pandas as pd

from neo4j import GraphDatabase, Query
from plotnine import *
from dotenv import load_dotenv

import slpgd
from slpgd import DependencySet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
neo4j_log = logging.getLogger("neo4j")
neo4j_log.setLevel(logging.WARNING)

load_dotenv() # Required to get content of .env when not using Docker

# Neo4J Authentication
USERNAME = "neo4j" if os.getenv("USERNAME") is None else os.getenv("USERNAME")
PASSWORD = "neo4j" if os.getenv("PASSWORD") is None else os.getenv("PASSWORD")
AUTH = (USERNAME, PASSWORD)

# Memgraph Connection
MEMGRAPH_DATABASE = "memgraph" if os.getenv("MEMGRAPH_DATABASE") is None else os.getenv("MEMGRAPH_DATABASE")
MEMGRAPH_URI = "bolt://localhost:7688" if os.getenv("MEMGRAPH_URI") is None else os.getenv("MEMGRAPH_URI")

# Neo4J Connection
NEO4J_URI = "neo4j://localhost" if os.getenv("NEO4J_URI") is None else os.getenv("NEO4J_URI")
NEO4J_DATABASE = "neo4j" if os.getenv("NEO4J_DATABASE") is None else os.getenv("NEO4J_DATABASE")

# Statistics and Metrics Export configuration
AVG_RED_COUNT_COL = "m6_avg_red_count"
DATABASE_COL = "database"
DEPENDENCY_COL = "dependency"
GRAPH_COL = "graph"
GRAPH_SOURCE_COL = "graph_source"
LP_POSSIBLE_COL = "lp_possible"
MAX_RED_COUNT_COL = "m5_max_red_count"
MAX_INC_COUNT_COL = "m8_max_inc_count"
METHOD_COL = "method"
METRIC_COL = "metric"
MINIMALITY_COL = "m7_minimality"
NO_INTER_GRAPH_DEPS_COL = "no_inter_deps"
NO_INTRA_GRAPH_DEPS_COL = "no_intra_deps"
ORIGIN_OF_DEPS_COL = "dep_origin"
ORIGINAL_NF_COL = "original_nf"
PDF_METADATA = {
    # 'Title': '',
    'Author': 'The Orb of Evaluation',
    # 'Subject': '',
    # 'Keywords': 'plotnine, python',
    'Creator': 'The Dominion'  # Optional, usually set by matplotlib
}
RUN_ID_COL = "run_id"
RUN_ID = str(uuid.uuid4())
TIMESTAMP_COL = "timestamp"
VALUE_COL = "value"
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
with open("setup.yaml", 'r') as file:
    setup = yaml.safe_load(file)

def main():


    try:
        test_connection_to_neo4j()
    except neo4j.exceptions.ServiceUnavailable:
        logger.error("Could not connect to Neo4j")
        exit(1)
    try:
        test_connection_to_memgraph()
    except neo4j.exceptions.ServiceUnavailable:
        logger.error("Could not connect to Memgraph")
        exit(1)

    logger.info("Start experiments")

    if len(setup["graphs"]) < 1:
        logger.error("No graphs found in setup.yaml")
        exit(1)

    for database in ["neo4j", "memgraph"]:
        for graph in setup["graphs"]:
            perform_experiment_for_graph(graph, database)

    logger.info("Finished experiments")

    logger.info("Create plot and export CSV results.")
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
        pass

    plot_metrics.save("out/plot.pdf", metadata=PDF_METADATA, verbose=False)

    graph_overview_df.to_csv("out/graph_overview.csv", index=False)
    graph_overview_df.to_latex("out/graph_overview.tex", index=False)

    per_graph_metrics_df.to_csv("out/metrics.csv", index=False)

    global per_dep_metrics_df
    per_dep_metrics_df = per_dep_metrics_df.set_index([GRAPH_COL, DATABASE_COL, METHOD_COL, DEPENDENCY_COL])
    per_dep_metrics_df.to_csv("out/per_dep_metrics.csv")
    per_dep_metrics_df.style.format(precision=3).to_latex("out/per_dep_metrics.latex")


def perform_experiment_for_graph(graph: dict, database: str):
    match database:
        case "memgraph":
            URI = MEMGRAPH_URI
            DATABASE = MEMGRAPH_DATABASE
        case _:
            URI = NEO4J_URI
            DATABASE = NEO4J_DATABASE
    logger.info(f"\tPerform experiment with graph \"{graph['name']}\"")

    measured_denormalized = False

    for method in ["relational"]: #,"slpgd1","slpgd2"]: #, "semantics1", "semantics2"]: # TODO: Enum?
        # 1. Clean up the database, as it may contain old data
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.execute_query("MATCH (n) DETACH DELETE n")

        # 2. Insert denormalized graph
        match database:
            case "memgraph":
                if "from_file" in graph.keys():
                    file = graph['from_file']
                elif "memgraph" in graph.keys():
                    file = graph['memgraph']['from_file']
                else:
                    break
                with open(file, 'r') as filename:
                    create_graph_queries_str = filename.read()
                    create_graph_queries = [s.strip() for s in (create_graph_queries_str.split(';')) if s.strip()]

                    with GraphDatabase.driver(URI).session(database=DATABASE) as session:
                        for query in create_graph_queries:
                            print(query)
                            session.run(query)
            case _:
                with GraphDatabase.driver(NEO4J_URI, auth=AUTH).session(database=DATABASE) as session:
                    if "from_file" in graph.keys():
                        file = graph['from_file']
                    elif "neo4j" in graph.keys():
                        file = graph['neo4j']['from_file']
                    else:
                        break
                    session.run(f"CALL apoc.cypher.runFile(\"{file}\");")

        provided_dependencies = DependencySet.from_string_list(graph["dependencies"])


        # 3. Get initial statistics
        get_graph_statistics(graph["name"], "denormalized", database, provided_dependencies, measured_denormalized) # None = no normalization performed yet --> TODO: Enum?
        measured_denormalized = True # Measurements for denomalized graphs have been taken and are not performed again


        # 4. Perform normalization
        match method:
            case "relational":
                provided_dependants = provided_dependencies.dependants
                with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
                    dependencies = DependencySet.from_string_list(graph["dependencies"]).infer_structural_deps(driver, except_dependants=provided_dependants)
                    # print(dependencies)
                    transformations: list[str]
                    new_pattern: str
                    transformations, new_pattern = dependencies.get_transformations_rel_synthesize(driver)
                    with driver.session(database=NEO4J_DATABASE) as session:
                        for transformation in transformations:
                        #    print(transformation)
                        #    print(new_pattern)
                            session.run(transformation)

                pass
            case _:
                pass

        # 5. Get statistics after normalization
        get_graph_statistics(graph["name"], method, database, provided_dependencies, measured_denormalized)
        # TODO replace with transformed dependencies

        #input("Press any key to continue...")

    logger.info(f"\tFinished experiment with graph \"{graph['name']}\"")


def get_graph_statistics(graph_name: str, method: str | None, database: str, dependencies: DependencySet, measured_denormalized) -> None:
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

    with GraphDatabase.driver(URI, auth=AUTH if database == "neo4j" else None).session() as session:
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
        with GraphDatabase.driver(URI, auth=AUTH if database == "neo4j" else None).session() as session:
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

    with GraphDatabase.driver(URI, auth=AUTH if database == "neo4j" else None).session() as session:
        for dep in dependencies:
            with GraphDatabase.driver(URI, auth=AUTH if database == "neo4j" else None).session() as session:
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
                result = session.run(f"""
MATCH {str(dep.pattern).replace("&", ":")} WITH DISTINCT 
{",".join(map(lambda left: str(left.to_query_string(database))+" AS x"+pascalcase(str(left)), dep.left))},
{dep.right.to_query_string(database)+" AS x"+pascalcase(str(dep.right))}
RETURN COUNT(*) AS res
""")
                record = result.single()
                if record is not None:
                    c = record["res"]

                result = session.run(f"""
MATCH {str(dep.pattern).replace("&", ":")} WITH  
{",".join(map(lambda left: str(left.to_query_string(database))+" AS x"+pascalcase(str(left)), dep.left))},
{dep.right.to_query_string(database)+" AS x"+pascalcase(str(dep.right))}
RETURN COUNT(*) AS res
                """)
                record = result.single()
                if record is not None:
                    e = record["res"]

                minimality = 1 if e == 1 else (c - 1) / (e - 1)

                # µ8
                result = session.run(f"""
MATCH {str(dep.pattern).replace("&", ":")} WITH  
{",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))},
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






def test_connection_to_neo4j():
    with GraphDatabase.driver(NEO4J_URI, auth=AUTH) as driver:
        driver.verify_connectivity()

def test_connection_to_memgraph():
    with GraphDatabase.driver(MEMGRAPH_URI) as driver:
        driver.verify_connectivity()

if __name__ == "__main__":
    main()