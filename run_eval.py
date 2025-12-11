import logging
import os
import time
import uuid

import neo4j.exceptions
import yaml
import pandas as pd

from neo4j import GraphDatabase, RoutingControl, Result, Query
from plotnine import *

from slpgd import DependencySet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: change to environment variables!!
URI = "neo4j://localhost" if os.getenv("URI") is None else os.getenv("URI")
USERNAME = "neo4j" if os.getenv("USERNAME") is None else os.getenv("USERNAME")
PASSWORD = "neo4j" if os.getenv("PASSWORD") is None else os.getenv("PASSWORD")
AUTH = (USERNAME, PASSWORD)
DATABASE = "neo4j" if os.getenv("DATABASE") is None else os.getenv("DATABASE")


GRAPH_COL = "graph"
METHOD_COL = "method"
METRIC_COL = "metric"
VALUE_COL = "value"
TIMESTAMP_COL = "timestamp"
RUN_ID_COL = "run_id"
RUN_ID = str(uuid.uuid4())

metrics_df = pd.DataFrame(columns=[GRAPH_COL, METHOD_COL, METRIC_COL, VALUE_COL, TIMESTAMP_COL, RUN_ID_COL])



def main():
    try:
        test_connection_to_neo4j()
    except neo4j.exceptions.ServiceUnavailable:
        logger.error("Could not connect to Neo4j")
        exit(1)

    logger.info("Start experiments")

    setup = ""
    with open("setup.yaml", 'r') as file:
        setup = yaml.safe_load(file)

    if len(setup["graphs"]) < 1:
        logger.error("No graphs found in setup.yaml")
        exit(1)

    for graph in setup["graphs"]:
        perform_experiment_for_graph(graph)


    logger.info("Finished experiments")

    logger.info("Create plot and export CSV results.")
    plot_height = 2 * len(setup["graphs"])
    plot_metrics = (ggplot(metrics_df, aes(x=METHOD_COL, y=VALUE_COL))
                    + geom_col(fill="darkblue", position="dodge")
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

    pdf_metadata = {
        #'Title': '',
        'Author': 'The Orb of Evaluation',
        #'Subject': '',
        #'Keywords': 'plotnine, python',
        'Creator': 'The Dominion'  # Optional, usually set by matplotlib
    }

    try:
        os.mkdir("out")
    except FileExistsError:
        pass

    plot_metrics.save("out/plot.pdf", metadata=pdf_metadata, verbose=False)
    metrics_df.to_csv("out/metrics.csv", index=False)


def perform_experiment_for_graph(graph: dict):
    logger.info(f"\tPerform experiment with graph \"{graph['name']}\"")

    for method in ["relational"]: #, "semantics1", "semantics2"]: # TODO: Enum?
        # 1. Clean up the database, as it may contain old data
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.execute_query("MATCH (n) DETACH DELETE n")
        # 2. Insert denormalized graph
        with open(graph["from_file"], 'r') as filename:
            create_graph_queries_str = filename.read()
            create_graph_queries = [s.strip() for s in (create_graph_queries_str.split(';')) if s.strip()]

            with GraphDatabase.driver(URI, auth=AUTH).session(database=DATABASE) as session:
                for query in create_graph_queries:
                    print(query)
                    session.run(query)

        # 3. Get initial statistics
        get_graph_statistics(graph["name"], "denormalized") # None = no normalization performed yet --> TODO: Enum?

        # 4. Perform normalization
        provided_dependencies = DependencySet.from_string_list(graph["dependencies"])
        match method:
            case "relational":
                provided_dependants = provided_dependencies.dependants
                with GraphDatabase.driver(URI, auth=AUTH) as driver:
                    dependencies = DependencySet.from_string_list(graph["dependencies"]).infer_structural_deps(driver, except_dependants=provided_dependants)
                    # print(dependencies)
                    transformations: list[str]
                    new_pattern: str
                    transformations, new_pattern = dependencies.get_transformations_rel_synthesize(driver)
                    with driver.session(database=DATABASE) as session:
                        for transformation in transformations:
                        #    print(transformation)
                        #    print(new_pattern)
                            session.run(transformation)

                pass
            case _:
                pass

        # 5. Get statistics after normalization
        get_graph_statistics(graph["name"], method)

        #input("Press any key to continue...")

    logger.info(f"\tFinished experiment with graph \"{graph['name']}\"")


def get_graph_statistics(graph_name: str, method: str | None):
    timestamp: int = 0
    if method != "denormalized":
        timestamp = time.time_ns()
    statistics_res: list[dict] = []

    # it is important that all queries return under the name "res"
    statistics_def: list[tuple[str,str]] = [
        ("NodeCount","MATCH (n) RETURN COUNT(n) as res"),
        ("EdgeCount", "MATCH ()-[e]->() RETURN COUNT(e) as res"),
        ("AvgNodePropCount", "MATCH (n) RETURN avg(size(keys(properties(n)))) AS res"),
        ("AvgEdgePropCount", "MATCH ()-[e]->() RETURN avg(size(keys(properties(e)))) AS res"),
   #     ("NodePropCount", "MATCH (n) RETURN size(keys(properties(n))) AS res"),
   #     ("EdgePropCount", "MATCH ()-[e]->() RETURN size(keys(properties(e))) AS res"),
    ]


    with GraphDatabase.driver(URI, auth=AUTH).session() as session:
        for statistic_def in statistics_def:
            query = Query(statistic_def[1])
            result = session.run(query)
            record = result.single()
            if record is not None:
                statistics_res.append({GRAPH_COL: graph_name, METHOD_COL: method, METRIC_COL: statistic_def[0], VALUE_COL: record["res"], RUN_ID_COL: RUN_ID})

    statistics_df = pd.DataFrame(statistics_res)

    if method == "denormalized":
        timestamp = time.time_ns()

    statistics_df[TIMESTAMP_COL] = pd.to_datetime(timestamp)

    global metrics_df
    metrics_df = pd.concat([metrics_df, statistics_df], ignore_index=True)





def test_connection_to_neo4j():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

if __name__ == "__main__":
    main()