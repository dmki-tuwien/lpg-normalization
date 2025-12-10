import pytest

from slpgd import *

def test_graph_object():
    go1 = Node("a")
    go2 = Edge("b")

    assert not go1 is go2
    assert go1 is go1

    assert str(go1) == "a"
    assert str(go2) == "b"


def test_property():
    go1 = Node("a")
    go2 = Edge("b")
    p1 = Property("a", go1)
    p2 = Property("a", go2)

    assert not p1 is p2
    assert p1 is p1

    assert str(p1) == "a.a"
    assert str(p2) == "b.a"


def test_reference():
    go1 = Node("a")
    go2 = Edge("b")
    p1 = Property("a", go1)
    p2 = Property("a", go2)
    r1 = Reference(go1)
    r2 = Reference(p1)
    r3 = Reference(go1)
    r4 = Reference(p2)

    assert not r1 is r2
    assert r1 is r1
    assert r1 is not r3
    assert r1.reference is r3.reference
    assert r2 is not r3
    assert r2.reference is not r3.reference

    assert str(r1) == "a"
    assert str(r2) == "a.a"
    assert str(r3) == "a"

    assert r1.get_graph_object() is go1
    assert r2.get_graph_object() is go1
    assert r1.get_graph_object() is r3.get_graph_object()
    assert r2.get_graph_object() is r3.get_graph_object()
    assert r2.get_graph_object() is not r4.get_graph_object()

def test_dependency():
    d: Dependency = Dependency(Node("a"),)
