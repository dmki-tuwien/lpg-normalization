from __future__ import annotations

import abc
import copy
import operator
from functools import reduce

import clingo
import uuid
from abc import abstractmethod

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from gnfd.gnfdLexer import gnfdLexer
from gnfd.gnfdListener import gnfdListener
from gnfd.gnfdParser import gnfdParser

CLINGO_FACT_NODE = "node"
CLINGO_FACT_LEFT_EDGE = "ledge"
CLINGO_FACT_RIGHT_EDGE = "redge"
CLINGO_FACT_PROPERTY = "prop"
CLINGO_FACT_LABEL = "lab"


class GraphObject(abc.ABC):
    """Abstract class representing an LPG graph object, i.e., a :any:`Edge` or a :any:`Node`.

    :param symbol: The symbol of the variable of the graph object.
    :type symbol: str
    :param labels: The labels of the graph object.
    :type labels: set[str] | None
    :param properties: The properties of the graph object.
    :type properties: set[str] | None"""

    def __init__(
        self,
        symbol: str = "",
        labels: set[str] | None = None,
        properties: set[str] | None = None,
    ):
        self.unique = uuid.uuid4().hex[:7]
        self.symbol: str = symbol

        if labels is None:
            self.labels: set[str] = set()
        else:
            self.labels: set[str] = labels

        if properties is None:
            self.properties: set[str] = set()
        else:
            self.properties: set[str] = properties

    def clingo_symbol(self) -> str:
        """Returns a symbol for use with clingo."""


        clingo_symbol = f"{self.symbol}_{self.unique}"
        return clingo_symbol

    def is_anonymous(self):
        """A graph object is anonymous if it has no symbol.
        Anonymous graph objects cannot be used in the descriptor, i.e., the left and right side, of a :any:`GNFD`.
        """
        return self.symbol == ""

    @abstractmethod
    def go_equals(self, other: GraphObject):
        """:returns: Whether 2 graph objects are equivalent"""

    def __str__(self):
        if len(self.labels) < 1:
            return self.symbol
        else:
            return f"{self.symbol}:{",".join(self.labels)}::{",".join(self.properties)}"
        # TODO: should I use ampersand instead of comma?


class Pattern(abc.ABC):
    """Represents a pattern used for matching in an LPG."""

    def __init__(self, string: str):
        self.string: str = string

    @abstractmethod
    def to_clingo_tableau(self, lhs: set[Reference], constants: bool = True) -> str:
        """:returns: The pattern represented as clingo facts containing constants or variables."""
        pass

    @abstractmethod
    def to_gql_match_where_tuple(self) -> tuple[str, str]:
        """:returns: A tuple where the first value denotes a GQL match and the second denotes a GQL where"""
        pass

    def to_gql_match_where_string(self) -> str:
        tup = self.to_gql_match_where_tuple()
        return f"MATCH {tup[0]} WHERE {tup[1]}"

    @abstractmethod
    def contains_var(self, symbol: str) -> bool:
        """Checks whether the pattern contains a graph object whose variable symbol is :paramref:`symbol`.

        :param symbol: The symbol which should be looked for in the pattern.
        :type symbol: str
        :returns: Whether there is a :any:`GraphObject` having :paramref:`symbol` as its symbol.
        """
        pass

    @abstractmethod
    def contains_property(self, symbol: str, key: str):
        """Checks whether the pattern contains a graph object whose variable symbol is :paramref:`symbol` and which has a property :paramref:`key`.

        :param symbol: The symbol which should be looked for in the pattern.
        :type symbol: str
        :param key: The key of the property whose existence should be checked.
        :type key: str
        :returns: Whether there is a :any:`GraphObject` having :paramref:`symbol` as its symbol.
        """
        pass

    @abstractmethod
    def get_graph_object_with_symbol(self, symbol: str) -> GraphObject | None:
        """:returns: a graph object with the given symbol"""
        pass

    @property
    @abc.abstractmethod
    def leftmost_node(self):
        """:returns: the left most node of the pattern, i.e., the leaf of always choosing pattern 1"""
        pass

    @property
    @abc.abstractmethod
    def rightmost_node(self):
        """:returns: the right most node of the pattern, i.e., the leaf of always choosing pattern 2"""
        pass

    def equals(self, other: Pattern) -> bool:
        """Computes whether the structure of this and the :paramref:`other` pattern and their labels and properties are equal.

        :returns: whether the :paramref:`other` is equal to this pattern."""
        for go1 in self.get_graph_objects():
            if not reduce(operator.or_, map(lambda go2: go1.go_equals(go2), other.get_graph_objects())):
                return False
        return True

    @abstractmethod
    def minimal_pattern_intersections(
        self, other: Pattern
    ) -> list[tuple[Pattern, set[tuple[str, str]]]]:
        """Computes the minimal pattern intersection between this and the :paramref:`other` pattern.

        :returns: a list of tuples consisting of (1) the pattern that is the minimal intersection between this and the :paramref:`other` pattern and of (2) tuples denote variable correspondences between the patterns.
        """

    @abstractmethod
    def get_graph_objects(self) -> set[GraphObject]:
        """:returns: all graph objects, i.e., :any:`Node`s and :any:`Edge`s."""
        pass

    def __str__(self):
        return self.string


class Node(GraphObject, Pattern):
    """Represents an LPG node."""

    def get_graph_objects(self) -> set[GraphObject]:
        res = set()
        res.add(self)
        return res

    def get_graph_object_with_symbol(self, symbol: str) -> GraphObject | None:
        if self.symbol == symbol and symbol != "":
            return self
        else:
            return None

    def to_gql_match_where_tuple(self) -> tuple[str, str]:
        label_delim: str = ""
        if len(self.labels) > 0:
            label_delim = ":"
        return f"({self.symbol}{label_delim}{":".join(self.labels)})", f"{" AND ".join(map(lambda key: f"{self.symbol}.{key} IS NOT NULL", self.properties))}"

    def to_clingo_tableau(self, lhs, constants = True) -> str:
        res = ""
        node_symbol = self.clingo_symbol()

        def get_symbol(prop_symbol, suffix="") -> str:
            if f"{self.symbol}.{prop_symbol}" in map(str, lhs):
                return f"{self.symbol}_{prop_symbol}"
            else:
                return f"{self.symbol}_{prop_symbol}_{suffix}"

        for i in ["1","2"]:
            if self not in map(lambda ref: ref.reference, lhs):
                node_symbol += i  # the symbol of the node occurs not on the left side of a dep, so it must be different
            if constants:
                res += "".join(
                    map(
                        lambda lab: f"enc({node_symbol.lower()},lab__,str__{lab}, {uuid.uuid4().hex[:7].lower()}).\n",
                        self.labels,
                    )
                )
                res += "".join(
                    map(
                        lambda prop: f"enc({node_symbol.lower()},{get_symbol(prop)}__,str__{get_symbol(prop,i)}, {uuid.uuid4().hex[:7].lower()}).\n",
                        self.properties,
                    )
                )
            else:
                if constants:
                    res += "".join(
                        map(
                            lambda lab: f"enc({node_symbol.upper()},lab__,Str__{lab}, {uuid.uuid4().hex[:7].upper()}).\n",
                            self.labels,
                        )
                    )
                    res += "".join(
                        map(
                            lambda
                                prop: f"enc({node_symbol.upper()},{get_symbol(prop)}__,Str__{get_symbol(prop,i)}, {uuid.uuid4().hex[:7].upper()}).\n",
                            self.properties,
                        )
                    )
        return res

    def contains_var(self, symbol: str) -> bool:
        return symbol == self.symbol

    def contains_property(self, symbol: str, key: str):
        return self.contains_var(symbol) and key in self.properties

    def minimal_pattern_intersections(self, other: Pattern):
        res: list[tuple[Pattern, set[tuple[str, str]]]] = []

        if isinstance(other, Node): # case 1
            rep = set()
            rep.add((self.symbol, other.symbol))
            tup = (Node(self.symbol,
                        labels=self.labels.union(other.labels),
                        properties=self.properties.union(other.properties)), rep)
            res.append(tup)

        if isinstance(other, Edge): # case 2
            for mpi in self.minimal_pattern_intersections(other.src_pattern): # case 2.1
                other_clone = copy.deepcopy(other)
                other_clone.src_pattern = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)
            for mpi in self.minimal_pattern_intersections(other.tgt_pattern): # case 2.1
                other_clone = copy.deepcopy(other)
                other_clone.tgt_pattern = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)

        if isinstance(other, PatternConcat): # case 3
            for mpi in self.minimal_pattern_intersections(other.left): # case 3.1
                other_clone = copy.deepcopy(other)
                other_clone.left = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)
            for mpi in self.minimal_pattern_intersections(other.right): # case 3.2
                other_clone = copy.deepcopy(other)
                other_clone.right = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)
        return res

    def go_equals(self, other):
        return (
                isinstance(other, Node)
                and self.labels == other.labels
                and self.properties == other.properties
        )

    def equals(self, other: Pattern) -> bool:
        return (
            isinstance(other, Node)
            and self.labels == other.labels
            and self.properties == other.properties
        )




    @property
    def leftmost_node(self):
        return self

    @property
    def rightmost_node(self):
        return self

    def __str__(self):
        return f"({self.symbol}:{"&".join(self.labels)}:{"&".join(self.properties)})"


class Edge(GraphObject, Pattern, abc.ABC):
    """Represents an abstract LPG edge without a direction.

    :param symbol: The symbol of the variable of the edge.
    :param labels: The labels of the edge.
    :param properties: The properties of the edge.
    :param src_pattern: The source :any:`Node` of the edge.
    :param tgt_pattern: The target :any:`Node` of the edge.
    """

    def __init__(
        self,
        symbol: str = "",
        labels: set[str] | None = None,
        properties: set[str] | None = None,
        src_pattern: Pattern | None = None,
        tgt_pattern: Pattern | None = None,
    ):
        self.src_pattern: Pattern | None = src_pattern
        self.tgt_pattern: Pattern | None = tgt_pattern
        super().__init__(symbol, labels, properties)

    def contains_var(self, symbol: str) -> bool:
        return (
            symbol == self.symbol
            or self.src_pattern.contains_var(symbol)
            or self.tgt_pattern.contains_var(symbol)
        )

    def contains_property(self, symbol: str, key: str):
        return (
            (self.contains_var(symbol) and key in self.properties)
            or self.src_pattern.contains_property(symbol, key)
            or self.tgt_pattern.contains_property(symbol, key)
        )

    def to_clingo_tableau(self, lhs, constants: bool = True) -> str:
        res = ""
        edge_symbol = self.clingo_symbol()

        def get_symbol(prop_symbol, suffix="") -> str:
            if f"{self.symbol}.{prop_symbol}" in map(str, lhs):
                return f"{self.symbol}_{prop_symbol}"
            else:
                return f"{self.symbol}_{prop_symbol}_{suffix}"

        for i in ["1", "2"]:
            if self not in map(lambda ref: ref.reference, lhs):
                edge_symbol += i  # the symbol of the node occurs not on the left side of a dep, so it must be different
            if constants:
                res += f"enc({self.src.clingo_symbol(lhs,i).lower()},edge__,{self.tgt.clingo_symbol(lhs,i).lower()},{self.clingo_symbol(lhs,i).lower()}).\n"
                res += "".join(
                    map(
                        lambda
                            lab: f"enc({self.clingo_symbol(lhs,i).lower()},lab__,str__{lab}, {uuid.uuid4().hex[:7].lower()}).\n",
                        self.labels,
                    )
                )
                res += "".join(
                    map(
                        lambda
                            prop: f"enc({self.clingo_symbol(lhs,i).lower()},{prop}__,str__{prop}, {uuid.uuid4().hex[:7].lower()}).\n",
                        self.properties,
                    )
                )
            else:
                res += f"enc({self.src.clingo_symbol(lhs,i).upper()},Edge__,{self.tgt.clingo_symbol(lhs,i).upper()},{self.clingo_symbol(lhs,i).upper()}).\n"
                res += "".join(
                    map(
                        lambda
                            lab: f"enc({self.clingo_symbol(lhs,i).upper()},lab__,Str__{lab}, {uuid.uuid4().hex[:7].upper()}).\n",
                        self.labels,
                    )
                )
                res += "".join(
                    map(
                        lambda
                            prop: f"enc({self.clingo_symbol(lhs,i).upper()},{prop}__,Str__{prop}, {uuid.uuid4().hex[:7].upper()}).\n",
                        self.properties,
                    )
                )
     #   res += self.src_pattern.to_clingo()
     #   res += self.tgt_pattern.to_clingo()
        return res

    def to_gql_match_where_tuple(self) -> tuple[str, str]:
        tup_src_pattern = self.src_pattern.to_gql_match_where_tuple()
        tup_tgt_pattern = self.tgt_pattern.to_gql_match_where_tuple()

        where = f"{" AND ".join(map(lambda key: f"{self.symbol}.{key} IS NOT NULL", self.properties))}"
        if len(where) > 0 and len(tup_src_pattern[1]) > 0:
            where += " AND "
        where += tup_src_pattern[1]
        if len(where) > 0 and len(tup_tgt_pattern[1]) > 0:
            where += " AND "
        where += tup_tgt_pattern[1]

        label_delim: str = ""
        if len(self.labels) > 0:
            label_delim = ":"

        return f"{tup_src_pattern[0]},({self.src.symbol})-[{self.symbol}{label_delim}{":".join(self.labels)}]->({self.tgt.symbol}),{tup_tgt_pattern[0]}", where

    def get_graph_object_with_symbol(self, symbol: str) -> GraphObject | None:
        if self.symbol == symbol and symbol != "":
            return self
        else:
            sgo = self.src_pattern.get_graph_object_with_symbol(symbol)
            tgo = self.tgt_pattern.get_graph_object_with_symbol(symbol)
            if sgo is not None:
                return sgo
            else:
                return tgo

    def get_graph_objects(self) -> set[GraphObject]:
        res = set()
        res.add(self)
        res = res.union(self.src_pattern.get_graph_objects())
        res = (
            res.union(self.tgt_pattern.get_graph_objects()))
        return res


    @property
    @abstractmethod
    def src(self):
        """:returns the source :any:`Node` of the edge"""
        pass

    @property
    @abstractmethod
    def tgt(self):
        """:returns the target :any:`Node` of the edge"""
        pass

    def go_equals(self, other: GraphObject) -> bool:
        return (
            isinstance(other, Edge)
            and self.src.go_equals(other.src)
            and self.tgt.go_equals(other.tgt)
            and self.labels == other.labels
            and self.properties == other.properties
        )

    def minimal_pattern_intersections(
        self, other: Pattern
    ) -> list[tuple[Pattern, set[tuple[str, str]]]]:
        res: list[tuple[Pattern, set[tuple[str, str]]]] = []

        if isinstance(other, Node): # case 2
            return other.minimal_pattern_intersections(self)

        elif isinstance(other, Edge): # case 4
            for mpi in self.minimal_pattern_intersections(other.src_pattern): # case 4.1
                clone = copy.deepcopy(self)
                clone.src_pattern = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (clone, rep)
                res.append(tup)
            for mpi in self.minimal_pattern_intersections(other.tgt_pattern): # case 4.2
                clone = copy.deepcopy(self)
                clone.tgt_pattern = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (clone, rep)
                res.append(tup)
            for mpi1 in self.minimal_pattern_intersections(other.src_pattern): # case 4.3
                for mpi2 in self.minimal_pattern_intersections(other.tgt_pattern):
                    clone = copy.deepcopy(self)
                    clone.src_pattern = mpi1[0]
                    clone.tgt_pattern = mpi2[0]
                    clone.labels = clone.labels.union(other.labels)
                    clone.properties = clone.properties.union(other.properties)
                    rep = set()
                    rep = rep.union(mpi1[1])
                    rep = rep.union(mpi2[1])
                    rep.add((self.symbol, other.symbol))
                    tup = (clone, rep)
                    res.append(tup)

        elif isinstance(other, PatternConcat):
            for mpi in self.minimal_pattern_intersections(other.left): # case 5.1
                other_clone = copy.deepcopy(other)
                other_clone.left = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)
            for mpi in self.minimal_pattern_intersections(other.right): # case 5.2
                other_clone = copy.deepcopy(other)
                other_clone.right = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)

        return res

def __str__(self):
    return f"-[{self.symbol}]-"


class LeftEdge(Edge):
    """Represents an LPG edge directed to the left."""

    @property
    def leftmost_node(self):
        return self.tgt_pattern.leftmost_node

    @property
    def rightmost_node(self):
        return self.src_pattern.rightmost_node

    @property
    def src(self):
        return self.src_pattern.leftmost_node

    @property
    def tgt(self):
        return self.tgt_pattern.rightmost_node

    def minimal_pattern_intersections(self, other: Pattern):
        pass

    def __str__(self):
        return f"{str(self.tgt_pattern)}<-[{self.symbol}:{"&".join(self.labels)}:{"&".join(self.properties)}]-{str(self.src_pattern)}"


class RightEdge(Edge):
    """Represents an LPG edge directed to the right."""

    @property
    def leftmost_node(self):
        return self.src_pattern.leftmost_node

    @property
    def rightmost_node(self):
        return self.tgt_pattern.rightmost_node

    @property
    def src(self):
        return self.src_pattern.rightmost_node

    @property
    def tgt(self):
        return self.tgt_pattern.leftmost_node

    def minimal_pattern_intersections(self, other: Pattern):
        pass

    def __str__(self):
        return f"{str(self.src_pattern)}-[{self.symbol}]->{str(self.tgt_pattern)}"


class PatternConcat(Pattern):
    """Represents a concatenation of two patterns."""

    def get_graph_objects(self) -> set[GraphObject]:
        res = set()
        res = res.union(self.left.get_graph_objects())
        res = res.union(self.right.get_graph_objects())
        return res

    def to_clingo_tableau(self) -> str:
        return f"{self.left.to_clingo_tableau()}\n{self.right.to_clingo_tableau()}"

    def __init__(self, left: Pattern, right: Pattern, string: str):
        super().__init__(string)
        self.left: Pattern = left
        self.right: Pattern = right

    def to_gql_match_where_tuple(self) -> tuple[str, str]:
        tup_left_pattern = self.left.to_gql_match_where_tuple()
        tup_right_pattern = self.right.to_gql_match_where_tuple()


        where = tup_left_pattern[1]
        if len(where) > 0 and len(tup_right_pattern[1]) > 0:
            where += " AND "
        where += tup_right_pattern[1]

        return f"{tup_left_pattern[0]},{tup_right_pattern[0]}", where

    def contains_var(self, symbol: str) -> bool:
        return self.left.contains_var(symbol) or self.right.contains_var(symbol)

    def contains_property(self, symbol: str, key: str):
        return self.left.contains_property(symbol, key) or self.right.contains_property(
            symbol, key
        )

    def get_graph_object_with_symbol(self, symbol: str) -> GraphObject | None:
        lgo = self.left.get_graph_object_with_symbol(symbol)
        rgo = self.right.get_graph_object_with_symbol(symbol)
        if lgo is not None:
            return lgo
        else:
            return rgo

    @property
    def leftmost_node(self):
        return self.left.leftmost_node

    @property
    def rightmost_node(self):
        return self.right.rightmost_node

    def minimal_pattern_intersections(self, other: Pattern):
        if isinstance(other, Node) or isinstance(other, Edge):
            return other.minimal_pattern_intersections(self)

        else: # case 6
            assert isinstance(other, PatternConcat)

            res: list[tuple[Pattern, set[tuple[str, str]]]] = []

            for mpi in self.minimal_pattern_intersections(other.left): # case 6.1
                other_clone = copy.deepcopy(other)
                other_clone.left = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)
            for mpi in self.minimal_pattern_intersections(other.right): # case 6.2
                other_clone = copy.deepcopy(other)
                other_clone.left = mpi[0]
                rep = set()
                rep = rep.union(mpi[1])
                tup = (other_clone, rep)
                res.append(tup)
            for mpi1 in self.minimal_pattern_intersections(other.left): # case 6.3
                for mpi2 in self.minimal_pattern_intersections(other.right):
                    other_clone = copy.deepcopy(other)
                    other_clone.left = mpi1[0]
                    other_clone.right = mpi2[0]
                    rep = set()
                    rep = rep.union(mpi1[1])
                    rep = rep.union(mpi2[1])

                    tup = (other_clone, rep)
                    res.append(tup)

            return res

    def __str__(self):
        return f"{str(self.left)}, {str(self.right)}"


class Property:
    """Represents an LPG property, i.e., a combination of property key and graph object variable."""

    def __init__(self, key: str, graph_object: GraphObject):
        self.key: str = key
        self.graphObject: GraphObject = graph_object

    def equals(self, other: Property) -> bool:
        return self.graphObject.go_equals(other.graphObject) and self.key == other.key

    def __str__(self):
        return f"{str(self.graphObject.symbol)}.{self.key}"


class Reference:
    """Represents a reference to a property key contained in a graph object or to the graph object itself."""

    def __init__(self, reference: GraphObject | Property):
        self.reference: GraphObject | Property = reference

    def __str__(self):
        return f"{str(self.reference)}"

    def get_graph_object(self) -> GraphObject:
        """:return: The graph object of the reference."""
        if isinstance(self.reference, GraphObject):
            return self.reference
        else:
            assert isinstance(self.reference, Property)
            return self.reference.graphObject

    def equals(self, other: Reference) -> bool:
        if isinstance(self.reference, GraphObject) and isinstance(other.reference, GraphObject):
            return self.reference.go_equals(other.reference)
        elif isinstance(self.reference, Property) and isinstance(self.reference, Property):
            return self.reference.equals(other.reference)
        else:
            return False # A graph object reference and a property reference can never be equal

    def to_query_string(self, database: str) -> str:
        """:return: The string representation of the reference that can be used to query the provided database."""
        if database == "memgraph" and isinstance(self.reference, GraphObject):
            return f"id({str(self.reference.symbol)})"
        elif isinstance(self.reference, GraphObject):
            return f"elementId({self.reference.symbol})"
        else:
            return str(self)


class GNFD:
    """Denotes a GN-FD that consists of a :any:`Pattern` and sets of :any:`Reference` that denote the right and left side of the descriptor of the GN-FD."""

    def __init__(
        self,
        pattern: Pattern,
        left: set[Reference],
        right: set[Reference],
    ):
        self.pattern: Pattern = pattern
        self.left: set[Reference] = left
        self.right: set[Reference] = right

    def __str__(self):
        return f"{str(self.pattern)}::{",".join(map(str, self.left))}=>{",".join(map(str, self.right))}"

    @staticmethod
    def from_string(string: str):
        """Parse a GN-FD from a string.

        :param string: The string representation of the GN-FD to create. Relies on the grammar shown in `gnfd.g4`.
        """

        # ANTLR has been run in this folder using the command `antlr4 -Dlanguage=Python3 -visitor gnfd.g4`.
        input_stream = InputStream(string)
        lexer = gnfdLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = gnfdParser(stream)
        tree = parser.dependency()
        listener = _GNFDListener()

        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.dependency

    @property
    def is_within_graph_object(self):
        return self.is_within_node or self.is_within_edge

    @property
    def is_within_node(self):
        gos = set(map(lambda ref: ref.get_graph_object(), self.left.union(self.right)))
        if len(gos) == 1:
            return isinstance(gos.pop(), Node)
        else:
            return False

    @property
    def is_within_edge(self):
        gos = set(map(lambda ref: ref.get_graph_object(), self.left.union(self.right)))
        if len(gos) == 1:
            return isinstance(gos.pop(), Edge)
        else:
            return False

    @property
    def is_inter_graph_object(self):
        return not self.is_within_graph_object

    def to_latex(self):
        return f"{str(self.pattern)}::{",".join(map(str, self.left))}\\determ {",".join(map(str, self.right))}"


class _GNFDListener(gnfdListener):
    def __init__(self):
        self.dependency: GNFD
        self.stack: list = []

    def exitDependency(self, ctx: gnfdParser.DependencyContext):
        right = self.stack.pop()
        left = self.stack.pop()
        pattern = self.stack.pop()

        self.dependency = GNFD(pattern, left, right)

    def exitReference(self, ctx: gnfdParser.ReferenceContext):
        ref = ctx.getText().split(".")
        pattern: Pattern = self.stack[0]

        go: GraphObject
        reference: Reference
        if not pattern.contains_var(ref[0]):
            raise ValueError(
                f'The descriptor of the dependency references a variable "{ref[0]}" that is not part of the pattern.'
            )
        else:
            go = pattern.get_graph_object_with_symbol(ref[0])
        if len(ref) > 1:
            if not pattern.contains_property(ref[0], ref[1]):
                raise ValueError(
                    f'The descriptor of the dependency references a property "{ref[0]}.{ref[1]}" that is not required to be present.'
                )
            else:
                reference = Reference(Property(ref[1], go))
        else:
            reference = Reference(go)

        self.stack.append(reference)

    def exitReferenceList(self, ctx):
        refs = ctx.getText().split(",")
        ref_objects = set()
        for _ in refs:
            ref_objects.add(self.stack.pop())
            self.stack.pop() # Second pop needed, as for each mentioned variable name a string is pushed to the stack
        self.stack.append(ref_objects)

    def exitLeft(self, ctx: gnfdParser.LeftContext):
        self.exitReferenceList(ctx)

    def exitRight(self, ctx: gnfdParser.RightContext):
        self.exitReferenceList(ctx)

    def exitPattern(self, ctx: gnfdParser.PatternContext):
        if ctx.getChildCount() == 3:
            right = self.stack.pop()
            left = self.stack.pop()
            assert isinstance(left, Pattern) and isinstance(right, Pattern)
            self.stack.append(PatternConcat(left, right, ctx.getText()))
        elif ctx.getChildCount() > 3:  # This is for sure an edge!
            if ctx.getChild(1).getText() == "<":  # it's a left edge
                match ctx.getChildCount():
                    case 7:  # Edge is "empty"
                        right = self.stack.pop()
                        left = self.stack.pop()
                        self.stack.append(LeftEdge(src_pattern=right, tgt_pattern=left))
                    case 8:
                        right = self.stack.pop()
                        if (
                            not ctx.getChild(4).getText().startswith(":")
                        ):  # Edge has a symbol
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                LeftEdge(name, src_pattern=right, tgt_pattern=left)
                            )
                        else:  # Edge has no symbol but labels
                            labels = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                LeftEdge("", labels, src_pattern=right, tgt_pattern=left)
                            )
                    case 9:
                        if (
                            not ctx.getChild(4).getText().startswith(":")
                        ):  # Edge has a symbol
                            right = self.stack.pop()
                            labels = self.stack.pop()
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                LeftEdge(
                                    name, labels, src_pattern=right, tgt_pattern=left
                                )
                            )
                        else:
                            right = self.stack.pop()
                            props = self.stack.pop()
                            labs = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                LeftEdge(
                                    labels=labs,
                                    properties=props,
                                    src_pattern=right,
                                    tgt_pattern=left,
                                )
                            )
                    case _:
                        if ctx.getChild(5).getText() == ":":  # No labels are present
                            right = self.stack.pop()
                            props = self.stack.pop()
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                LeftEdge(
                                    name,
                                    properties=props,
                                    src_pattern=right,
                                    tgt_pattern=left,
                                )
                            )
                        else:  # everything is present
                            right = self.stack.pop()
                            props = self.stack.pop()
                            labs = self.stack.pop()
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                LeftEdge(
                                    name,
                                    labels=labs,
                                    properties=props,
                                    src_pattern=right,
                                    tgt_pattern=left,
                                )
                            )
            else:  # it's an right edge
                match ctx.getChildCount():
                    case 7:  # Edge is "empty"
                        right = self.stack.pop()
                        left = self.stack.pop()
                        self.stack.append(
                            RightEdge(src_pattern=left, tgt_pattern=right)
                        )
                    case 8:
                        right = self.stack.pop()
                        if (
                            not ctx.getChild(3).getText().startswith(":")
                        ):  # Edge has a symbol
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                RightEdge(name, src_pattern=left, tgt_pattern=right)
                            )
                        else:  # Edge has no symbol but labels
                            labels = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                RightEdge("", labels, src_pattern=left, tgt_pattern=right)
                            )
                    case 9:
                        if (
                            not ctx.getChild(3).getText().startswith(":")
                        ):  # Edge has a symbol
                            right = self.stack.pop()
                            labels = self.stack.pop()
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                RightEdge(
                                    name, labels, src_pattern=left, tgt_pattern=right
                                )
                            )
                        else:
                            right = self.stack.pop()
                            props = self.stack.pop()
                            labs = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                RightEdge(
                                    labels=labs,
                                    properties=props,
                                    src_pattern=left,
                                    tgt_pattern=right,
                                )
                            )
                    case _:
                        if ctx.getChild(4).getText() == ":":  # No labels are present
                            right = self.stack.pop()
                            props = self.stack.pop()
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                RightEdge(
                                    name,
                                    properties=props,
                                    src_pattern=left,
                                    tgt_pattern=right,
                                )
                            )
                        else:  # everything is present
                            right = self.stack.pop()
                            props = self.stack.pop()
                            labs = self.stack.pop()
                            name = self.stack.pop()
                            left = self.stack.pop()
                            self.stack.append(
                                RightEdge(
                                    name,
                                    labels=labs,
                                    properties=props,
                                    src_pattern=left,
                                    tgt_pattern=right,
                                )
                            )

    def exitNodePattern(self, ctx: gnfdParser.NodePatternContext):
        node: Node = Node()
        name = ""
        props = set()
        labs = set()
        match ctx.getChildCount():
            case 2:  # Node is "empty"
                pass
            case 3:
                if not ctx.getChild(1).getText().startswith(":"):  # Node has a symbol
                    node = Node(self.stack.pop())
                else:  # Node has no symbol but labels
                    node = Node(labels=self.stack.pop())
            case 4:
                if not ctx.getChild(1).getText().startswith(":"):  # Node has a symbol
                    labs = self.stack.pop()
                    name = self.stack.pop()
                    node = Node(name, labs)
                else:
                    props = self.stack.pop()
                    labs = self.stack.pop()
                    node = Node(labels=labs, properties=props)
            case _:
                if ctx.getChild(2).getText() == ":":  # No labels are present
                    props = self.stack.pop()
                    name = self.stack.pop()
                    node = Node(name, properties=props)
                else:  # everything is present
                    props = self.stack.pop()
                    labs = self.stack.pop()
                    name = self.stack.pop()
                    node = Node(name, labs, props)

        if len(self.stack) > 0:
            p: Pattern = self.stack[0]
            res = p.get_graph_object_with_symbol(node.symbol)
            if res is not None:
                node = res
                node.labels = node.labels.union(labs)
                node.properties = node.properties.union(props)

        self.stack.append(node)

    def enterLabelList(self, ctx: gnfdParser.LabelListContext):
        self.stack.append(
            set(map(str.strip, ctx.getText().replace(":", "").split("&")))
        )  # [1:] removes the leading colon of the list

    def enterPropertyList(self, ctx: gnfdParser.PropertyListContext):
        self.stack.append(
            set(map(str.strip, ctx.getText().replace(":", "").split("&")))
        )  # [1:] removes the leading colon of the list

    def exitVarName(self, ctx: gnfdParser.VarNameContext):
        self.stack.append(ctx.getText())
