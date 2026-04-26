import sys
import time

from caseconverter import pascalcase
from dotenv import load_dotenv
from fastapi import FastAPI, status
from neo4j import GraphDatabase, Driver, Query
from pydantic import BaseModel
from typing import Literal

import os
import yaml
from starlette.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gnfd
from normalize import perform_graph_native_normalization

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


origins = [
    "http://localhost:3000"
]

# 2. Add the middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows Content-Type, Authorization, etc.
)

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
    """Returns `true` when the API is healthy."""
    try:
        return get_database_health("neo4j") and get_database_health("memgraph")
    except Exception:
        return False

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
    with get_driver(database).session(database=database) as session:
        session.run("MATCH (n) DETACH DELETE n")

    return True

@app.post("/reset")
def total_reset():
    return reset("neo4j") and reset("memgraph")

@app.get("/{database}/scenarios")
def get_scenarios(database: Literal["neo4j", "memgraph"]) -> list[ScenarioDef]:
    """Retrieves the names and IDs of available scenarios as a `list`"""

    res: list[ScenarioDef] = list(
        map(lambda map_entry: {"id": map_entry["id"], "name": map_entry["name_html"], "category": map_entry["category"]},
           filter(
               lambda filter_entry: ("neo4j" in filter_entry.keys() and "from_file" in filter_entry["neo4j"].keys()) or ("from_file" in filter_entry.keys()),
                setup["graphs"]
           )
           )
    )

    return res


@app.post("/{database}/scenarios/load")
def load_scenario(database: Literal["neo4j", "memgraph"], id: str) -> bool:
    """Loads a scenario into the supplied database. Returns `True` when successful and `False` otherwise."""
    reset(database)

    driver = get_driver(database)
    graph = next(filter(lambda filter_entry:
                       (
                           ("neo4j" in filter_entry.keys() and "from_file" in filter_entry["neo4j"].keys()) or
                           ("from_file" in filter_entry.keys())
                       ) and id == filter_entry["id"],
        setup["graphs"]))
    match database:
        case "memgraph":
            if "from_file" in graph.keys():
                file = graph["from_file"]
            elif "memgraph" in graph.keys():
                file = graph["memgraph"]["from_file"]
            else:
                neo_driver = get_driver("neo4j")

                with neo_driver.session(database="neo4j") as session:
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
                        session.run(query)
        case _:
            with driver.session(database=database) as session:
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
    return True

@app.get("/{database}/scenarios/{id}/dependencies")
def get_dependencies(database: Literal["neo4j", "memgraph"], id: str) -> list[str]:
    res: list[str] = next(map(lambda map_entry: map_entry["dependencies"], filter(
            lambda filter_entry: filter_entry["id"] == id and (("neo4j" in filter_entry.keys() and "from_file" in filter_entry["neo4j"].keys()) or (
                        "from_file" in filter_entry.keys())),
            setup["graphs"])))

    return res


@app.get("/{database}/scenarios/{id}/minimal_cover")
def get_minimal_cover(database: Literal["neo4j", "memgraph"], id: str) -> list[str]:
    res: list[str] = next(map(lambda map_entry: map_entry["minimal_cover"], filter(
            lambda filter_entry: filter_entry["id"] == id and (("neo4j" in filter_entry.keys() and "from_file" in filter_entry["neo4j"].keys()) or (
                        "from_file" in filter_entry.keys())),
            setup["graphs"])))
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

    res = dict()

    with get_driver(database).session() as session:
        for statistics_def_key in statistics_def.keys():
            query = Query(statistics_def[statistics_def_key])
            result = session.run(query)
            record = result.single()
            if record is not None:
                res[statistics_def_key] = 0 if record["res"] is None else record["res"]

    return res

@app.post("/{database}/statistics/dependencies")
def get_per_dep_statistics(database: Literal["neo4j", "memgraph"], dependencies: list[str]) -> dict[str, dict[str, float]]:
    res = dict()

    for dep_str in dependencies:
        res[dep_str] = dict()
        dep = gnfd.GOFD.from_string(dep_str)

        with get_driver(database).session() as session:
            result = session.run(f"""
                    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH  
                    {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))}, 
                    count(*) AS red
                    RETURN max(red) AS res
                                                    """)
            record = result.single()
            if record is not None:
                res[dep_str]["MaxRedPot"] = record["res"]


        with get_driver(database).session() as session:
            result = session.run(f"""
                    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]} WITH
                    {",".join(map(lambda left: str(left.to_query_string(database)) + " AS x" + pascalcase(str(left)), dep.left))},
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
                    {", ".join(map(lambda left: f"x{pascalcase(str(left))}: {left}", dep.left))},
                    {", ".join(map(lambda right: f"x{pascalcase(str(right))}: {right}", dep.right))}
                    }}) AS res""")
            record = result.single()
            if record is not None:
                clusters = record["res"]

        with get_driver(database).session() as session:
            result = session.run(f"""
                    {dep.pattern.to_gql_match_where_string().split("WHERE")[0]}
                    RETURN count({{
                    {", ".join(map(lambda left: f"x{pascalcase(str(left))}: {left}", dep.left))},
                    {", ".join(map(lambda right: f"x{pascalcase(str(right))}: {right}", dep.right))}
                    }}) AS res""")
            record = result.single()
            if record is not None:
                elements = record["res"]

        res[dep_str]["Minimality"] = 1 if elements == 1 else (clusters - 1) / (elements - 1)

    return res

@app.post("/{database}/normalize")
def normalize(database: Literal["neo4j", "memgraph"], dependencies: list[str]) -> tuple[list[str], list[str], float]:
    dependencies_str_list = dependencies
    dependencies_obj_list = gnfd.DependencySet.from_string_list(dependencies_str_list)

    with get_driver(database) as driver:
        before = time.time_ns()
        norm_res = perform_graph_native_normalization(driver, database, dependencies_obj_list)
        after = time.time_ns()

    duration = after - before
    duration = duration/(10**9)
    res = (list(map(str, norm_res[0])), norm_res[1], duration)


    return res

@app.get("/{database}/visualize/nodes")
def visualize_nodes(database: Literal["neo4j", "memgraph"]) -> list[dict]:
    with get_driver(database).session() as session:
        if database == "neo4j":
            result = session.run(f"""MATCH (n) return elementId(n) as id, labels(n) as labels, properties(n) as properties""")
            return [record for record in result]
        if database == "memgraph":
            result = session.run(f"""MATCH (n) return id(n) as id, labels(n) as labels, properties(n) as properties""")
            return [record for record in result]

@app.get("/{database}/visualize/edges")
def visualize_edges(database: Literal["neo4j", "memgraph"]) -> list[dict]:
    with get_driver(database).session() as session:
        if database == "neo4j":
            result = session.run(f"""MATCH (n)-[m]->(o) return elementId(n) as src, elementId(m) as id, elementId(o) as tgt, [type(m)] as labels,  properties(m) as properties""")
            return [record for record in result]
        if database == "memgraph":
            result = session.run(f"""MATCH (n)-[m]->(o) return id(n) as src, id(m) as id, id(o) as tgt, [type(m)] as labels, properties(m) as properties""")
            return [record for record in result]

@app.post("/{database}/visualize/dependencies")
def visualize_deps(database: Literal["neo4j", "memgraph"], dependencies: list[str]) -> list:
    res_list = []
    for dep_str in dependencies:
        dep = gnfd.GOFD.from_string(dep_str)
        for left in dep.left:
            left_prefix = "n" if isinstance(left.get_graph_object(), gnfd.Node) else "re"
            for right in dep.right:
                right_prefix = "n" if isinstance(right.get_graph_object(), gnfd.Node) else "re"
                with get_driver(database).session() as session:
                    if left.is_graph_object_variable and right.is_graph_object_variable:
                        result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                    "{left_prefix}"+{str(left.to_query_string(database))} AS left,
                                    "{right_prefix}"+{str(right.to_query_string(database))} AS right
                                    RETURN left, right""")
                    elif left.is_graph_object_variable and right.is_property_variable:
                        if database == "neo4j":
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+{str(left.to_query_string(database))} AS left,
                                                                "{right_prefix}"+elementId({str(right.get_graph_object().symbol)})+"_{str(right.reference.key)}" AS right
                                                                RETURN left, right""")
                        else:
                            assert database == "memgraph"
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+{str(left.to_query_string(database))} AS left,
                                                                "{right_prefix}"+id({str(right.get_graph_object().symbol)})+"_{str(right.reference.key)}" AS right
                                                                RETURN left, right""")
                    elif left.is_property_variable and right.is_graph_object_variable:
                        if database == "neo4j":
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+elementId({str(left.get_graph_object().symbol)})+"_{str(left.reference.key)}" AS left,
                                                                "{right_prefix}"+{str(right.to_query_string(database))} AS right
                                                                RETURN left, right""")
                        else:
                            assert database == "memgraph"
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+id({str(left.get_graph_object().symbol)})+"_{str(left.reference.key)}" AS left,
                                                                "{right_prefix}"+{str(right.to_query_string(database))} AS right
                                                                RETURN left, right""")
                    else:
                        assert left.is_property_variable
                        assert right.is_property_variable
                        if database == "neo4j":
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+elementId({str(left.get_graph_object().symbol)})+"_{str(left.reference.key)}" AS left,
                                                                "{right_prefix}"+elementId({str(right.get_graph_object().symbol)})+"_{str(right.reference.key)}" AS right
                                                                RETURN left, right""")
                        else:
                            result = session.run(f"""{dep.pattern.to_gql_match_where_string()} WITH
                                                                "{left_prefix}"+id({str(left.get_graph_object().symbol)})+"_{str(left.reference.key)}" AS left,
                                                                "{right_prefix}"+id({str(right.get_graph_object().symbol)})+"_{str(right.reference.key)}" AS right
                                                                RETURN left, right""")

                    res_list = res_list + [record for record in result]

    return res_list