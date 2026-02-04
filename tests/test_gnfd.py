import pytest
from pandas.core.groupby import GroupBy

from gnfd import *

def test_node_pattern():
    a_dep_0 = GNFD.from_string("(a)::a=>a")
    a_dep_1 = GNFD.from_string("(a:Test_0a)::a=>a")
    a_dep_2 = GNFD.from_string("(a::p)::a=>a")
    a_dep_3 = GNFD.from_string("(a:Test_2c:q)::a.q=>a,a.q")

    assert a_dep_0.pattern.contains_var("a")
    assert not a_dep_0.pattern.contains_var("b")

    assert not a_dep_0.pattern.contains_property("a", "o")
    assert not a_dep_1.pattern.contains_property("a", "o")
    assert not a_dep_2.pattern.contains_property("a", "o")
    assert a_dep_2.pattern.contains_property("a", "p")
    assert not a_dep_2.pattern.contains_property("b", "p")
    assert a_dep_3.pattern.contains_property("a", "q")
    assert not a_dep_3.pattern.contains_property("z", "y")

def test_concat_pattern():
    ab_dep_0 = GNFD.from_string("(a),(b)::a=>b")
    ab_dep_1 = GNFD.from_string("(a),()::a=>a")
    ab_dep_2 = GNFD.from_string("(a:Test1:p)<-[c]-(d:Hallo:t),(b:Test2:q)-[]->()::a.p=>b.q")

    assert ab_dep_0.pattern.contains_var("a")
    assert ab_dep_0.pattern.contains_var("b")
    assert not ab_dep_0.pattern.contains_var("c")

    assert ab_dep_1.pattern.contains_var("a")
    assert not ab_dep_1.pattern.contains_var("b")

    assert ab_dep_2.pattern.contains_property("a","p")
    assert not ab_dep_2.pattern.contains_property("a","q")
    assert ab_dep_2.pattern.contains_property("b", "q")
    assert not ab_dep_2.pattern.contains_property("b", "p")

def test_edge_pattern():
    abc_dep_0 = GNFD.from_string("(a)-[b]->(c)::a=>b")

    assert abc_dep_0.pattern.contains_var("a")
    assert abc_dep_0.pattern.contains_var("b")
    assert abc_dep_0.pattern.contains_var("c")
    assert not abc_dep_0.pattern.contains_var("d")

    abc_dep_1 = GNFD.from_string("(a)<-[b]-(c)::a=>b")

    assert abc_dep_1.pattern.contains_var("a")
    assert abc_dep_1.pattern.contains_var("b")
    assert abc_dep_1.pattern.contains_var("c")
    assert not abc_dep_1.pattern.contains_var("d")

    abc_dep_2 = GNFD.from_string("(a::p)-[b::hi]->(c)::a=>b")

    assert abc_dep_2.pattern.contains_var("a")
    assert abc_dep_2.pattern.contains_property("a","p")
    assert abc_dep_2.pattern.contains_var("b")
    assert abc_dep_2.pattern.contains_property("b","hi")
    assert abc_dep_2.pattern.contains_var("c")
    assert not abc_dep_2.pattern.contains_property("b", "o")
    assert not abc_dep_2.pattern.contains_property("c", "d")
    assert not abc_dep_2.pattern.contains_property("d", "e")

    abc_dep_3 = GNFD.from_string("(a::p)<-[b::hi]-(c)::a=>b")

    assert abc_dep_3.pattern.contains_var("a")
    assert abc_dep_3.pattern.contains_property("a", "p")
    assert abc_dep_3.pattern.contains_var("b")
    assert abc_dep_3.pattern.contains_property("b", "hi")
    assert abc_dep_3.pattern.contains_var("c")
    assert not abc_dep_3.pattern.contains_property("b", "o")
    assert not abc_dep_3.pattern.contains_property("c", "d")
    assert not abc_dep_3.pattern.contains_property("d", "e")

    abc_dep_4 = GNFD.from_string("(a::p)<-[]-(c)::a.p=>c")

    assert abc_dep_4.pattern.contains_var("a")
    assert abc_dep_4.pattern.contains_property("a", "p")
    assert abc_dep_4.pattern.contains_var("c")
    assert not abc_dep_4.pattern.contains_property("c", "d")
    assert not abc_dep_4.pattern.contains_property("d", "e")

    abc_dep_5 = GNFD.from_string("(a::p)<-[:My_Label]-(c)::a.p=>c")

    assert abc_dep_5.pattern.contains_var("a")
    assert abc_dep_5.pattern.contains_property("a", "p")
    assert abc_dep_5.pattern.contains_var("c")
    assert not abc_dep_5.pattern.contains_property("c", "d")
    assert not abc_dep_5.pattern.contains_property("d", "e")

    abc_dep_6 = GNFD.from_string("(a::p)<-[b:My_Label]-(c)::a.p=>b")

    assert abc_dep_6.pattern.contains_var("a")
    assert abc_dep_6.pattern.contains_property("a", "p")
    assert abc_dep_6.pattern.contains_var("b")
    assert abc_dep_6.pattern.contains_var("c")
    assert not abc_dep_6.pattern.contains_property("c", "d")
    assert not abc_dep_6.pattern.contains_property("d", "e")

    abc_dep_7 = GNFD.from_string("(a::p)<-[b:My_Label:Prop]-(c)::a.p=>b.Prop")

    assert abc_dep_7.pattern.contains_var("a")
    assert abc_dep_7.pattern.contains_property("a", "p")
    assert abc_dep_7.pattern.contains_var("b")
    assert abc_dep_7.pattern.contains_property("b", "Prop")
    assert abc_dep_7.pattern.contains_var("c")
    assert not abc_dep_7.pattern.contains_property("c", "d")
    assert not abc_dep_7.pattern.contains_property("d", "e")

def test_vars_in_scope():
    with pytest.raises(ValueError):
        GNFD.from_string("(a)-[b]->(c)::a.x=>b.y")

    with pytest.raises(ValueError):
        GNFD.from_string("(a)-[b]->(c)::a=>by")

def test_pattern_equality():
    # Nodes
    abc_dep_0 = GNFD.from_string("(a)-[b]->(c)::a=>b")

    assert abc_dep_0.pattern.leftmost_node.contains_var("a")
    assert abc_dep_0.pattern.rightmost_node.contains_var("c")
    assert abc_dep_0.pattern.rightmost_node.equals(abc_dep_0.pattern.leftmost_node)

    abc_dep_1 = GNFD.from_string("(a)<-[b]-(c:Hi)::a=>b")

    assert abc_dep_1.pattern.leftmost_node.contains_var("a")
    assert abc_dep_1.pattern.rightmost_node.contains_var("c")
    assert not abc_dep_1.pattern.rightmost_node.equals(abc_dep_1.pattern.leftmost_node)

    abc_dep_2 = GNFD.from_string("(a::D)<-[b]-(c)::a=>b")

    assert abc_dep_2.pattern.leftmost_node.contains_var("a")
    assert abc_dep_2.pattern.rightmost_node.contains_var("c")
    assert not abc_dep_2.pattern.rightmost_node.equals(abc_dep_2.pattern.leftmost_node)
    # Nodes do not equal edges?
    assert not abc_dep_2.pattern.equals(abc_dep_2.pattern.rightmost_node)

    # Edges vs. concat
    abcde_dep_1 = GNFD.from_string("(a::D)<-[b]-(c)-[d]->(e:Hello:World)::a=>b")
    abcde_dep_2 = GNFD.from_string("(a::D)<-[b]-(c),(c)-[d]->(f:Hello:World)::c=>f.World")

    assert abcde_dep_1.pattern.equals(abcde_dep_2.pattern)

    abcde_dep_3 = GNFD.from_string("(a::D)<-[b]-(c)-[d]->(e:Hello:World)::a=>b")
    abcde_dep_4 = GNFD.from_string("(a::D)<-[b]-(c),(c:No_longer_equal)-[d]->(f:Hello:World)::c=>f.World")
    abcde_dep_5 = GNFD.from_string("(a::D)<-[b]-(t),(t:No_longer_equal)-[d]->(f:Hello:World)::t=>f.World")

    assert not abcde_dep_3.pattern.equals(abcde_dep_4.pattern)
    assert abcde_dep_5.pattern.equals(abcde_dep_4.pattern)

    # Nodes vs. concat
    ab_dep_0 = GNFD.from_string("(a),(b::Hi)::a=>b.Hi")
    ab_dep_1 = GNFD.from_string("(b::Hi)::b=>b.Hi")

    assert not ab_dep_0.pattern.equals(ab_dep_1.pattern)

def test_minimal_pattern_intersections():
    # Case 1
    a_dep_0 = GNFD.from_string("(a)::a=>a")
    a_dep_1 = GNFD.from_string("(a:Test_0a)::a=>a")
    a_dep_2 = GNFD.from_string("(a:Ole:p)::a=>a")
    a_dep_3 = GNFD.from_string("(b:Test_2c:q)::b.q=>b,b.q")
    a_dep_23 = GNFD.from_string("(c:Test_2c&Ole:p&q)::c.q=>c,c.q")

    mpi_01 = a_dep_0.pattern.minimal_pattern_intersections(a_dep_1.pattern)
    assert len(mpi_01) == 1
    assert isinstance(mpi_01[0][0], Node)
    assert mpi_01[0][0].equals(a_dep_1.pattern)
    assert len(mpi_01[0][1]) == 1
    assert ("a","a") in mpi_01[0][1]

    mpi_23 = a_dep_2.pattern.minimal_pattern_intersections(a_dep_3.pattern)
    assert len(mpi_23) == 1
    assert isinstance(mpi_23[0][0], Node)
    assert mpi_23[0][0].equals(a_dep_23.pattern)
    assert len(mpi_23[0][1]) == 1
    assert ("a", "b") in mpi_23[0][1]


# def test_entailment():
#     deps: list[str] = ["(x::k2)-[y::k3]->(:L2)::x.k2=>y.k3", "(x::k1&k2)-[:L1]->()::x.k1=>x.k2"]
#
#     deps: DependencySet = DependencySet.from_string_list(deps)
#     target = GNFD.from_string("(x::k1&k2)-[y:L1:k3]->(:L2)::x.k1=>y.k3")
#
#     deps.entail(target)
#
#     pass






