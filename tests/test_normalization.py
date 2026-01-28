import pytest
from testcontainers.neo4j import Neo4jContainer

from gnfd import DependencySet
from normalize import perform_graph_native_normalization

# Define the container as a session-level fixture
@pytest.fixture(scope="session")
def neo4j_container():
    # 1. Initialize and start the container
    with Neo4jContainer("neo4j:2025.10") as neo4j:
        yield neo4j  # Yields the running container object


@pytest.fixture(scope="function")
def graph_db(neo4j_container):
    driver = neo4j_container.get_driver()

    # Clean up the database before running the next test (i.e., and a new copy of a graph will be inserted)
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    yield driver
    driver.close()

@pytest.fixture(scope="function")
def graph_simple(graph_db):
    """The simple graph used for the tests can be visualized as:
     _________                            _______
    /   A     \  B  y1="y1", y2="y2"   \ /   C   \
    | x1="x1" |------------------------>|        |
    | x2="x2" |                       / \_______/
    \________/
    """
    with graph_db.session() as session:
        session.run("CREATE (:A {x1: \"x1\", x2: \"x2\"})-[:B {y1: \"y1\", y2: \"y2\"}]->(:C)")
    yield graph_db

@pytest.fixture(scope="function")
def graph_merge(graph_db):
    """The merge graph used for the tests can be visualized as:
     _________                            _______
    /  A id1  \ B id2 y1="y1", y2="y2" \ / C id3 \
    | x1="x1" |------------------------>|        |
    | x2="x2" |                       / \_______/
    \________/

     _________                            _______
    /  A id4  \ B id5 y1="y1", y2="y2" \ / C id6 \
    | x1="x1" |------------------------>|        |
    | x2="x2" |                       / \_______/
    \________/
    """
    with graph_db.session() as session:
        session.run("CREATE (:A {x1: \"x1\", x2: \"x2\"})-[:B {y1: \"y1\", y2: \"y2\"}]->(:C)")
        session.run("CREATE (:A {x1: \"x1\", x2: \"x2\"})-[:B {y1: \"y1\", y2: \"y2\"}]->(:C)")
    yield graph_db

def test_graph_simple_exists(graph_simple):
    with graph_simple.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 2

        result = session.run("MATCH (a:A) RETURN count(a) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 1

        result = session.run("MATCH (c:C) RETURN count(c) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 1

        result = session.run("MATCH ()-[b:B]->() RETURN count(b) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 1

        result = session.run("MATCH (a:A)-[b:B]->(c:C) RETURN count(*) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 1

def test_graph_merge_exists(graph_merge):
    with graph_merge.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 4

        result = session.run("MATCH (a:A) RETURN count(a) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 2

        result = session.run("MATCH (c:C) RETURN count(c) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 2

        result = session.run("MATCH ()-[b:B]->() RETURN count(b) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 2

        result = session.run("MATCH (a:A)-[b:B]->(c:C) RETURN count(*) as count")
        record = result.single()
        assert record is not None
        assert record["count"] == 2

@pytest.mark.parametrize("dependency_strings,result_query", [
    ## Test within nodes
    (["(a:A)-[b:B]->(c:C)::a=>a"],
         "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Trivial --> nothing happens
    (["(a:A:x1)-[b:B]->(c:C)::a.x1=>a"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Denotes a key --> nothing happens
    (["(a:A:x1)-[b:B]->(c:C)::a=>a.x1"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Structurally implied --> nothing happens
    (["(a:A:x1&x2)-[b:B]->(c:C)::a.x1=>a.x2"],
     "MATCH (a:A)-[b:B]->(c:C) MATCH (a)-[:AX1AX2]-(d:Ax1ax2) WHERE a.x1 IS NULL AND a.x2 IS NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL AND d.Ax1=\"x1\" AND d.Ax2=\"x2\" RETURN count(*) as count"), # Nodes of dep. are transformed to a new node

    ## Test within edges
    (["(a:A)-[b:B]->(c:C)::b=>b"],
         "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Trivial --> nothing happens
    (["(a:A)-[b:B:y1]->(c:C)::b.y1=>b"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Denotes a key --> nothing happens
    (["(a:A)-[b:B:y1]->(c:C)::b=>b.y1"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Structurally implied --> nothing happens
    (["(a:A)-[b:B:y1&y2]->(c:C)::b.y1=>b.y2"],
     "MATCH (a:A)-[:SRC_B]->(b:B)-[:TGT_B]->(c:C) MATCH (b)-[:BY1BY2]->(d:By1by2) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NULL AND d.By1=\"y1\" AND d.By2=\"y2\" RETURN count(*) as count"), # Reification + move to new node

    ## Test edge --> node
    (["(a:A)-[b:B]->(c:C)::b=>a"],
         "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Structurally implied --> nothing happens
    (["(a:A:x1)-[b:B]->(c:C)::b=>a.x1"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Structurally implied --> nothing happens
    (["(a:A)-[b:B:y1]->(c:C)::b.y1=>a"],
     "MATCH (a:A)-[:SRC_B]->(b:B)-[:TGT_B]->(c:C) MATCH (b)-[:BY1]->(d:By1) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND d.By1=\"y1\" RETURN count(*) as count"), 
    (["(a:A:x1)-[b:B:y1]->(c:C)::b.y1=>a.x1"],
     "MATCH (a:A)-[:SRC_B]->(b:B)-[:TGT_B]->(c:C) MATCH (b)-[:AX1BY1]->(d:Ax1by1) WHERE a.x1 IS NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND d.By1=\"y1\" AND d.Ax1=\"x1\" RETURN count(*) as count"),

    ## Test node --> edge
    (["(a:A)-[b:B]->(c:C)::a=>b"],
         "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Limits the number of incoming/outgoing edges to 1
    (["(a:A:x1)-[b:B]->(c:C)::a.x1=>b"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL RETURN count(*) as count"), # Limits the number of incoming/outgoing edges to 1
    (["(a:A)-[b:B:y1]->(c:C)::a=>b.y1"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND a.By1=\"y1\" RETURN count(*) as count"),
    (["(a:A:x1)-[b:B:y1]->(c:C)::a.x1=>b.y1"],
     "MATCH (a:A)-[b:B]->(c:C) MATCH (a)-[:AX1BY1]->(d:Ax1by1) WHERE a.x1 IS NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND d.By1=\"y1\" AND d.Ax1=\"x1\" RETURN count(*) as count")
])
def test_graph_simple(graph_simple, dependency_strings, result_query):
    provided_dependencies = DependencySet.from_string_list(dependency_strings)

    perform_graph_native_normalization(graph_simple, "neo4j", provided_dependencies)

    with graph_simple.session() as session:
        result = session.run(result_query)
        record = result.single()
        assert record is not None
        assert record["count"] == 1


@pytest.mark.parametrize("dependency_strings,result_query", [
    ## Test within nodes
    (["(a:A:x1&x2)-[b:B]->(c:C)::a.x1=>a.x2"],
     "MATCH (a:A)-[b:B]->(c:C) MATCH (a)-[:AX1AX2]-(d:Ax1ax2) WHERE a.x1 IS NULL AND a.x2 IS NULL AND b.y1 IS NOT NULL AND b.y2 IS NOT NULL AND d.Ax1=\"x1\" AND d.Ax2=\"x2\" RETURN count(DISTINCT d) as count"), # Nodes of dep. are transformed to exactly 1 new node

    ## Test within edges
    (["(a:A)-[b:B:y1&y2]->(c:C)::b.y1=>b.y2"],
     "MATCH (a:A)-[:SRC_B]->(b:B)-[:TGT_B]->(c:C) MATCH (b)-[:BY1BY2]->(d:By1by2) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NULL AND d.By1=\"y1\" AND d.By2=\"y2\" RETURN count(DISTINCT d) as count"), # Reification + move to new node

    ## Test edge --> node
    (["(a:A)-[b:B:y1]->(c:C)::b.y1=>a"],
     "MATCH (a:A)-[:SRC_B]->(b:B)-[:TGT_B]->(c:C) MATCH (b)-[:BY1]->(d:By1) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND d.By1=\"y1\" RETURN count(DISTINCT d) as count"), # Only limits the endpoint of edges --> nothing happens
    (["(a:A:x1)-[b:B:y1]->(c:C)::b.y1=>a.x1"],
     "MATCH (a:A)-[:SRC_B]->(b:B)-[:TGT_B]->(c:C) MATCH (b)-[:AX1BY1]->(d:Ax1by1) WHERE a.x1 IS NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND d.By1=\"y1\" AND d.Ax1=\"x1\" RETURN count(DISTINCT d) as count"),

    ## Test node --> edge
    (["(a:A)-[b:B:y1]->(c:C)::a=>b.y1"],
     "MATCH (a:A)-[b:B]->(c:C) WHERE a.x1 IS NOT NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND a.By1=\"y1\" RETURN count(DISTINCT [a, a.By1])-1 as count"), # For this query 2 is expected, but since the expectation in this test is always 1, we do -1
    (["(a:A:x1)-[b:B:y1]->(c:C)::a.x1=>b.y1"],
     "MATCH (a:A)-[b:B]->(c:C) MATCH (a)-[:AX1BY1]->(d:Ax1by1) WHERE a.x1 IS NULL AND a.x2 IS NOT NULL AND b.y1 IS NULL AND b.y2 IS NOT NULL AND d.By1=\"y1\" AND d.Ax1=\"x1\" RETURN count(DISTINCT d) as count") # TODO!
])
def test_graph_merge(graph_merge, dependency_strings, result_query):
    provided_dependencies = DependencySet.from_string_list(dependency_strings)

    perform_graph_native_normalization(graph_merge, "neo4j", provided_dependencies)

    with graph_merge.session() as session:
        result = session.run(result_query)
        record = result.single()
        assert record is not None
        assert record["count"] == 1
