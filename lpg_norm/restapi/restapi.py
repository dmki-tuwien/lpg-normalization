import asyncio
import logging
import os
import sys
import time
from typing import Literal

import yaml
from caseconverter import pascalcase
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from neo4j import Driver, GraphDatabase, Query
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from lpg_norm.gofd import GOFD

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lpg_norm import gofd
from lpg_norm.logger import QueryLogger
from lpg_norm.normalize import (
    perform_graph_native_normalization, perform_structural_normalization,  # perform_structural_normalization
)

class WebSocketLogHandler(logging.Handler):
    """Custom logging handler that distributes logs to active asyncio queues."""

    def __init__(self):
        super().__init__()
        self.queues: set[asyncio.Queue] = set()

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        # put_nowait ensures the log call is non-blocking
        for queue in list(self.queues):
            try:
                queue.put_nowait(msg)
            except asyncio.QueueFull:
                pass



ws_handler = WebSocketLogHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
ws_handler.setFormatter(formatter)



ROOT_PATH = (
    ""
    if os.getenv("URL_PREFIX") is None
    else os.getenv("URL_PREFIX")
)
app: FastAPI
if ROOT_PATH == "":
    app = FastAPI()
else:
    app = FastAPI(root_path=ROOT_PATH)


ORIGINS = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows Content-Type, Authorization, etc.
)

logging.setLoggerClass(QueryLogger)
logger = logging.getLogger("lpg-norm-rest")
logger.addHandler(ws_handler)
logger.setLevel(logging.INFO)



setup: dict
"""The configuration of the demo scenarios."""
with open("setup.yaml", "r") as file:
    setup = yaml.safe_load(file)

load_dotenv()  # Required to get content of .env when not using Docker

GRAPHS_PATH = "./graphs" if os.getenv("GRAPHS_PATH") is None else os.getenv("GRAPHS_PATH")

# Memgraph Connection
MEMGRAPH_DATABASE = (
    "memgraph"
    if os.getenv("MEMGRAPH_DATABASE") is None
    else os.getenv("MEMGRAPH_DATABASE")
)
MEMGRAPH_URI = (
    "bolt://memgraph:7687"
    if os.getenv("MEMGRAPH_URI") is None
    else os.getenv("MEMGRAPH_URI")
)

# Neo4J Connection
NEO4J_URI = (
    "bolt://neo4j:7687" if os.getenv("NEO4J_URI") is None else os.getenv("NEO4J_URI")
)
NEO4J_DATABASE = (
    "neo4j" if os.getenv("NEO4J_DATABASE") is None else os.getenv("NEO4J_DATABASE")
)
USERNAME = (
        "neo4j" if os.getenv("USERNAME") is None else os.getenv("USERNAME")
)
PASSWORD = (
        "password" if os.getenv("PASSWORD") is None else os.getenv("PASSWORD")
)

def get_driver(database: Literal["neo4j", "memgraph"]) -> Driver:
    if database == "neo4j":
        return GraphDatabase.driver(NEO4J_URI, auth=(USERNAME, PASSWORD))
    elif database == "memgraph":
        return GraphDatabase.driver(MEMGRAPH_URI, auth=(None, None))


class ScenarioDef(BaseModel):
    id: str
    name: str
    category: str

@app.get("/health")
def get_health() -> bool:
    """Returns `true` when the API is healthy, i.e., connections to both, Neo4j and Memgraph can be established."""
    try:
        return get_database_health("neo4j") and get_database_health("memgraph")
    except Exception:
        return False

@app.post("/reset")
def total_reset():
    return reset("neo4j") and reset("memgraph")

@app.get("/{database}/health")
def get_database_health(database: Literal["neo4j", "memgraph"]):
    """Returns `true` when a connection to the supplied database can be established."""

    res = False
    with get_driver(database) as driver:
        driver.verify_connectivity()
        # The following is only executed if the connection was successful:
        res = True

    return res

@app.post("/{database}/reset")
def reset(database:  Literal["neo4j", "memgraph"]):
    """Resets the database system, i.e., removes all nodes and edges."""
    try:
        with get_driver(database).session(database=database) as session:
            query = "MATCH (n) DETACH DELETE n"
            session.run(query)
            logger.info(f"Reset \"{database}\".")
            logger.query(query)
    except Exception as e:
        logger.error(f"Failed to reset \"{database}\": {e}")

    return True


@app.get("/{database}/scenarios")
def get_scenarios(database: Literal["neo4j", "memgraph"]) -> list[ScenarioDef]:
    """Retrieves the names and IDs of available scenarios as a `list`"""

    res: list[ScenarioDef] = [{"id": map_entry["id"], "name": map_entry["name_html"], "category": map_entry["category"]} for map_entry in
           filter(
               lambda filter_entry: ("neo4j" in filter_entry and "from_file" in filter_entry["neo4j"]) or ("from_file" in filter_entry),
                setup["graphs"]
           )
           ]


    return res


@app.post("/{database}/scenarios/load")
def load_scenario(database: Literal["neo4j", "memgraph"], id: str) -> bool:
    """Loads a scenario into the supplied database. Returns `True` when successful and `False` otherwise."""
    reset(database)

    driver = get_driver(database)
    graph = next(filter(lambda filter_entry:
                       (
                           ("neo4j" in filter_entry and "from_file" in filter_entry["neo4j"]) or
                           ("from_file" in filter_entry)
                       ) and id == filter_entry["id"],
        setup["graphs"]))

    logger.info(f"Load scenario \"{id}\" into \"{database}\".")
    match database:
        case "memgraph":
            if "from_file" in graph:
                file = graph["from_file"]
            elif "memgraph" in graph:
                file = graph["memgraph"]["from_file"]
            else:
                neo_driver = get_driver("neo4j")

                with neo_driver.session(database="neo4j") as session:
                    if "from_file" in graph:
                        query = f"CALL apoc.cypher.runFile(\"{graph['from_file']}\");"
                        session.run(query)
                        logger.query(query)
                    elif (
                            "neo4j" in graph
                            and "from_file" in graph["neo4j"]
                    ):
                        session.run(
                            f"CALL apoc.cypher.runFile(\"{graph['neo4j']['from_file']}\");"
                        )
                with driver.session(database="memgraph") as session:
                    session.run("CREATE INDEX ON :__MigrationNode__;")

                    session.run("CREATE INDEX ON :__MigrationNode__(__elementId__);")

                    neo4j_uri = NEO4J_URI[7:-5]
                    if "localhost" in neo4j_uri or "127.0.0.1" in neo4j_uri:
                        neo4j_uri = "host.docker.internal"

                    session.run(f"""
CALL migrate.neo4j("MATCH (n) RETURN labels(n) AS src_labels, elementId(n) AS src_id, properties(n) AS src_props", {{host: "{neo4j_uri}", port: 7687, username: "neo4j", password: "password"}})
YIELD row
MERGE (n:__MigrationNode__ {{__elementId__: row.src_id}})
SET n:row.src_labels
SET n += row.src_props; """)

                    session.run(f"""
CALL migrate.neo4j(
  "MATCH (n)-[r]->(m) RETURN type(r) as rel_type, elementId(n) AS src_id, elementId(m) AS dest_id, properties(r) AS edge_props",
  {{host: "{neo4j_uri}", port: 7687, username: "neo4j", password: "password"}})
YIELD row
MATCH (n:__MigrationNode__ {{__elementId__: row.src_id}})
MATCH (m:__MigrationNode__ {{__elementId__: row.dest_id}})
CREATE (n)-[r:row.rel_type]->(m)
SET r += row.edge_props;""")

                    session.run("""
MATCH (n:__MigrationNode__)
REMOVE n:__MigrationNode__
REMOVE n.__elementId__;""")
                    session.run("DROP INDEX ON :__MigrationNode__;")
                    session.run("DROP INDEX ON :__MigrationNode__(__elementId__);")

                    return True


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
                        logger.query(query)
                        session.run(query)
        case _:
            with driver.session(database=database) as session:
                if "from_file" in graph:
                    session.run(
                        f"CALL apoc.cypher.runFile(\"{graph['from_file']}\");"
                    )
                elif (
                        "neo4j" in graph
                        and "from_file" in graph["neo4j"]
                ):
                    session.run(
                        f"CALL apoc.cypher.runFile(\"{graph['neo4j']['from_file']}\");"
                    )
    return True

@app.get("/{database}/scenarios/{id}/dependencies")
def get_dependencies(database: Literal["neo4j", "memgraph"], id: str) -> list[str]:
    res: list[str] = next(map_entry["dependencies"] for map_entry in filter(
            lambda filter_entry: filter_entry["id"] == id and (("neo4j" in filter_entry and "from_file" in filter_entry["neo4j"]) or (
                        "from_file" in filter_entry)),
            setup["graphs"]))

    return res


@app.get("/{database}/scenarios/{id}/minimal_cover")
def get_minimal_cover(database: Literal["neo4j", "memgraph"], id: str) -> list[str]:
    res: list[str] = next(map_entry["minimal_cover"] for map_entry in filter(
            lambda filter_entry: filter_entry["id"] == id and (("neo4j" in filter_entry and "from_file" in filter_entry["neo4j"]) or (
                        "from_file" in filter_entry)),
            setup["graphs"]))
    return res

@app.get("/{database}/statistics/graph")
def get_per_graph_statistics(database: Literal["neo4j", "memgraph"]) -> dict[str, float]:
    statistics_def: dict[str, str]
    if database=="neo4j":
        statistics_def = {
        "NodeCount": "MATCH (n) RETURN COUNT(n) as res",
        "EdgeCount": "MATCH ()-[e]->() RETURN COUNT(e) as res",
        "AvgNodePropCount": "MATCH (n) RETURN avg(size(keys(properties(n)))) AS res",
        "AvgEdgePropCount": "MATCH ()-[e]->() RETURN avg(size(keys(properties(e)))) AS res",
        "DisconnectedSubgraphCount": """MATCH (n)
OPTIONAL MATCH (n)-[*0..]-(m)
WITH n, collect(DISTINCT elementId(m)) AS component
WITH DISTINCT apoc.coll.sort(component) AS uniqueComponents
RETURN count(uniqueComponents) AS res"""
        }
    else:
        assert database=="memgraph"
        statistics_def = {
            "NodeCount": "MATCH (n) RETURN COUNT(n) as res",
            "EdgeCount": "MATCH ()-[e]->() RETURN COUNT(e) as res",
            "AvgNodePropCount": "MATCH (n) RETURN avg(size(keys(properties(n)))) AS res",
            "AvgEdgePropCount": "MATCH ()-[e]->() RETURN avg(size(keys(properties(e)))) AS res",
            "DisconnectedSubgraphCount": """CALL weakly_connected_components.get() YIELD node, component_id
RETURN count(DISTINCT component_id) AS res"""
        }

    res: dict = {}

    with get_driver(database).session() as session:
        for statistics_def_key in statistics_def:
            query = Query(statistics_def[statistics_def_key])
            result = session.run(query)
            record = result.single()
            if record is not None:
                res[statistics_def_key] = 0 if record["res"] is None else record["res"]

    return res

@app.post("/{database}/statistics/dependencies")
def get_per_dep_statistics(database: Literal["neo4j", "memgraph"], dependencies: list[str]) -> dict[str, dict[str, float]]:
    res = {}

    for dep_str in filter(lambda dep: not GOFD.from_string(dep).is_trivial, dependencies):
        res[dep_str] = {}
        dep = gofd.GOFD.from_string(dep_str)

        with get_driver(database).session() as session:
            result = session.run(f"""
                    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH  
                    {",".join(f"{left.to_query_string(database)!s} AS x{pascalcase(str(left))}" for left in dep.left)}, 
                    count(*) AS red
                    RETURN max(red) AS res
                                                    """)
            record = result.single()
            if record is not None:
                res[dep_str]["MaxRedPot"] = record["res"]


        with get_driver(database).session() as session:
            result = session.run(f"""
                    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH
                    {",".join(f"{left.to_query_string(database)!s} AS x{pascalcase(str(left))}" for left in dep.left)},
                    count(*) AS red
                    RETURN avg(red) AS res
                                                    """)
            record = result.single()
            if record is not None:
                res[dep_str]["AvgRedPot"] = record["res"]

        clusters = 0
        elements = 0
        with get_driver(database).session() as session:
            result = session.run(f"""
                    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]}
                    RETURN count(DISTINCT {{
                    {", ".join(f"x{pascalcase(str(left))}: {left}" for left in dep.left)},
                    {", ".join(f"x{pascalcase(str(right))}: {right}" for right in dep.right)}
                    }}) AS res""")
            record = result.single()
            if record is not None:
                clusters = record["res"]

        with get_driver(database).session() as session:
            result = session.run(f"""
                    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]}
                    RETURN count({{
                    {", ".join(f"x{pascalcase(str(left))}: {left}" for left in dep.left)},
                    {", ".join(f"x{pascalcase(str(right))}: {right}" for right in dep.right)}
                    }}) AS res""")
            record = result.single()
            if record is not None:
                elements = record["res"]

        res[dep_str]["Minimality"] = 1 if elements == 1 else (clusters - 1) / (elements - 1)

    return res

@app.post("/{database}/normalize")
def normalize(database: Literal["neo4j", "memgraph"],
              dependencies: list[str],
              method: Literal["graph-native", "lp", "structural"] = "graph-native",
              useLlm: bool = False,
              llmUrl: str | None = None,
              llmKey: str | None = None,
              llmModel: str | None = None) -> tuple[list[str], list[str], float]:
    dependencies_str_list = dependencies
    dependencies_obj_list = gofd.DependencySet.from_string_list(dependencies_str_list)

    with get_driver(database) as driver:
        before = time.time_ns()
        norm_res = None
        if method == "graph-native":
            norm_res = perform_graph_native_normalization(driver, database, dependencies_obj_list, logger=logger, useLlm=useLlm, llmUrl=llmUrl, llmKey=llmKey, llmModel=llmModel)
        elif method == "lp":
            norm_res = perform_graph_native_normalization(driver, database, dependencies_obj_list, dep_filter="within-node", logger=logger)
        elif method == "structural":
            norm_res = perform_structural_normalization(driver, database, logger=logger)
            pass
        after = time.time_ns()

    duration = after - before
    duration = duration/(10**9)
    res = (list(map(str, norm_res[0])), norm_res[1], duration)

    return res


@app.get("/{database}/visualize/nodes")
def visualize_nodes(database: Literal["neo4j", "memgraph"]) -> list[dict]:
    with get_driver(database).session() as session:
        if database == "neo4j":
            result = session.run("""MATCH (n) return elementId(n) as id, labels(n) as labels, properties(n) as properties""")
            return [record for record in result]
        elif database == "memgraph":
            result = session.run("""MATCH (n) return id(n) as id, labels(n) as labels, properties(n) as properties""")
            return [record for record in result]

@app.get("/{database}/visualize/edges")
def visualize_edges(database: Literal["neo4j", "memgraph"]) -> list[dict]:
    with get_driver(database).session() as session:
        if database == "neo4j":
            result = session.run("""MATCH (n)-[m]->(o) return elementId(n) as src, elementId(m) as id, elementId(o) as tgt, [type(m)] as labels,  properties(m) as properties""")
            return [record for record in result]
        if database == "memgraph":
            result = session.run("""MATCH (n)-[m]->(o) return id(n) as src, id(m) as id, id(o) as tgt, [type(m)] as labels, properties(m) as properties""")
            return [record for record in result]

@app.post("/{database}/visualize/dependencies")
def visualize_deps(database: Literal["neo4j", "memgraph"], dependencies: list[str]) -> list:
    res_list = []
    for dep_str in dependencies:
        dep = gofd.GOFD.from_string(dep_str)
        for left in dep.left:
            left_prefix = "n" if isinstance(left.get_graph_object(), gofd.Node) else "re"
            for right in dep.right:
                right_prefix = "n" if isinstance(right.get_graph_object(), gofd.Node) else "re"
                with get_driver(database).session() as session:
                    if left.is_graph_object_variable and right.is_graph_object_variable:
                        result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                    "{left_prefix}"+{left.to_query_string(database)!s} AS left,
                                    "{right_prefix}"+{right.to_query_string(database)!s} AS right
                                    RETURN left, right""")
                    elif left.is_graph_object_variable and right.is_property_variable:
                        if database == "neo4j":
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+{left.to_query_string(database)!s} AS left,
                                                                "{right_prefix}"+elementId({right.get_graph_object().symbol!s})+"_{right.reference.key!s}" AS right
                                                                RETURN left, right""")
                        else:
                            assert database == "memgraph"
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+{left.to_query_string(database)!s} AS left,
                                                                "{right_prefix}"+id({right.get_graph_object().symbol!s})+"_{right.reference.key!s}" AS right
                                                                RETURN left, right""")
                    elif left.is_property_variable and right.is_graph_object_variable:
                        if database == "neo4j":
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+elementId({left.get_graph_object().symbol!s})+"_{left.reference.key!s}" AS left,
                                                                "{right_prefix}"+{right.to_query_string(database)!s} AS right
                                                                RETURN left, right""")
                        else:
                            assert database == "memgraph"
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+id({left.get_graph_object().symbol!s})+"_{left.reference.key!s}" AS left,
                                                                "{right_prefix}"+{right.to_query_string(database)!s} AS right
                                                                RETURN left, right""")
                    else:
                        assert left.is_property_variable
                        assert right.is_property_variable
                        if database == "neo4j":
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+elementId({left.get_graph_object().symbol!s})+"_{left.reference.key!s}" AS left,
                                                                "{right_prefix}"+elementId({right.get_graph_object().symbol!s})+"_{right.reference.key!s}" AS right
                                                                RETURN left, right""")
                        else:
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+id({left.get_graph_object().symbol!s})+"_{left.reference.key!s}" AS left,
                                                                "{right_prefix}"+id({right.get_graph_object().symbol!s})+"_{right.reference.key!s}" AS right
                                                                RETURN left, right""")

                    res_list = res_list + [record for record in result]

    return res_list





@app.websocket("/ws/log")
async def ws_log(websocket: WebSocket):
    await websocket.accept()
    log_queue = asyncio.Queue(maxsize=100)
    ws_handler.queues.add(log_queue)

    try:
        while True:
            # Awaits until a new log record is available in the queue
            log_entry = await log_queue.get()
            await websocket.send_text(log_entry)
            log_queue.task_done()
    except (WebSocketDisconnect, asyncio.CancelledError):
        pass
    finally:
        # Clean up queue reference when client disconnects
        ws_handler.queues.discard(log_queue)




