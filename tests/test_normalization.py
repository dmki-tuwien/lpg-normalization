import pytest
from sympy.parsing.sympy_parser import transformations
from testcontainers.neo4j import Neo4jContainer

from slpgd import DependencySet


# Define the container as a session-level fixture
@pytest.fixture(scope="session")
def neo4j_container():
    # 1. Initialize and start the container
    with Neo4jContainer("neo4j:2025.10") as neo4j:
        yield neo4j  # Yields the running container object


@pytest.fixture(scope="function")
def graph_db(neo4j_container):
    driver = neo4j_container.get_driver()

    # Clean up the database before running the next test
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    yield driver
    driver.close()

@pytest.fixture(scope="function")
def graph_simple(graph_db):
    """The simple graph used for the tests can be visualized as:
     _______                 _______
    /   A   \  B  y="y"   \ /   C   \
    | x="x" |-------------->| z="z" |
    \_______/             / \_______/
    """
    with graph_db.session() as session:
        session.run("CREATE (:A {x: \"x\"})-[:B {y: \"y\"}]->(:C {z: \"z\"})")
    yield graph_db


def test_graph_simple_exists(graph_simple):
    # Use the driver provided by the fixture to run your library's functions
    # and assert results against the clean test database.
    # ...
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

@pytest.mark.parametrize("dependency_strings,result_query", [
    (["(a:A)-[b:B]->(c:C):a->b.y"],
         "MATCH (a:A)-[b:B]->(c:C) WHERE a.BY IS NOT NULL AND b.Y IS NULL RETURN count(*) as count"),
    (["(a:A)-[b:B]->(c:C):a.x->b.y"],
         "MATCH (x1:AXBY)-[:AXBY]-(a:A)-[b:B]->(c:C) WHERE x1.AX IS NOT NULL AND x1.BY IS NOT NULL AND a.X IS NULL AND b.Y IS NULL RETURN count(*) as count"),
    (["(a:A)-[b:B]->(c:C):b.y->a.x"],
         "MATCH (x1:AXBY)-[:AXBY]-(a:A)-[b:B]->(c:C) WHERE x1.AX IS NOT NULL AND x1.BY IS NOT NULL AND a.X IS NULL AND b.Y IS NULL RETURN count(*) as count"),
    (["(a:A)-[b:B]->(c:C):b->a"],
         "MATCH (a:A)-[b:B]->(c:C) WHERE a.x IS NOT NULL AND b.y IS NOT NULL AND c.z IS NOT NULL RETURN count(*) as count"),
    (["(a:A)-[b:B]->(c:C):a.x->b"], # TODO: Adjust to be a.x->b
         "MATCH (x1:AXBY)-[:AXBY]-(a:A)-[b:B]->(c:C) WHERE x1.AX IS NOT NULL AND x1.BY IS NOT NULL AND a.X IS NULL AND b.Y IS NULL RETURN count(*) as count"),
    (["(a:A)-[b:B]->(c:C):b.y->a"],
         "MATCH (a:A)-[b:B]->(c:C) WHERE a.x IS NOT NULL AND b.y IS NOT NULL AND c.z IS NOT NULL RETURN count(*) as count"),
])
def test_graph_simple_global_one_dep(graph_simple, dependency_strings, result_query):
    provided_dependencies = DependencySet.from_string_list(dependency_strings)
    provided_dependants = provided_dependencies.dependants
    dependencies = DependencySet.from_string_list(dependency_strings).infer_structural_deps(graph_simple, except_dependants=provided_dependants)

    transformations, _ = dependencies.get_transformations_rel_synthesize(graph_simple)
    with graph_simple.session() as session:
        for transformation in transformations:
            session.run(transformation)

        result = session.run(result_query)
        record = result.single()
        assert record is not None
        assert record["count"] == 1

