from __future__ import annotations

import abc
from enum import Enum
from functools import reduce

from antlr4 import *

from slpgd.parser.spgdsParser import spgdsParser
from slpgd.parser.spgdsLexer import spgdsLexer
from slpgd.parser.spgdsListener import spgdsListener

"""This file contains the classes for representing the SLPGDs in Python."""


class GraphObject(abc.ABC):
    """Abstract class representing an LPG graph object, i.e., a :any:`Edge` or a :any:`Node`.

    :param symbol: The symbol of the variable of the graph object.
    :param labels: The labels of the graph object."""

    def __init__(self, symbol: str, labels: str):
        self.symbol: str = symbol
        self.labels: set[str] = set()

    def __repr__(self):
        if len(self.labels) < 1:
            return self.symbol
        else:
            return f"{self.symbol}:{",".join(self.labels)}"


class Node(GraphObject):
    """Represents an LPG node.

    :param symbol: The symbol of the variable of the node.
    :param labels: The labels of the node."""

    def __repr__(self):
        return f"{super().__repr__()}"


class Edge(GraphObject):
    """Represents an LPG edge.

    :param symbol: The symbol of the variable of the node.
    :type symbol: str
    :param labels: The labels of the node.
    :type labels: str
    :param src: The source :any:`Node` of the edge.
    :type src: Node | None
    :param tgt: The target :any:`Node` of the edge.
    :type tgt: Node | None
    """

    def __init__(self, symbol: str, labels: str, src: Node | None, tgt: Node | None):
        self.src: Node | None = src
        self.tgt: Node | None = tgt
        super().__init__(symbol, labels)

    def __repr__(self):
        return f"{super().__repr__()}"


class Property:
    def __init__(self, key: str, graph_object: GraphObject):
        self.key: str = key
        self.graphObject: GraphObject = graph_object

    def __repr__(self):
        return f"{str(self.graphObject)}.{self.key}"


class Pattern:
    """Represents the matching pattern of an SLPGD :any:`Dependency`."""

    def __init__(self, pattern: str, graph_objects: set[GraphObject]):
        self._pattern: str = pattern
        """The string representation of the pattern."""
        self.graph_objects: set[GraphObject] = graph_objects
        """The graph objects contained in the pattern represented as :any:`GraphObject`."""

    def get_graph_object_by_symbol(self, symbol: str) -> GraphObject:
        for graph_object in self.graph_objects:
            if graph_object.symbol == symbol:
                return graph_object

    def __repr__(self):
        return self._pattern

    def __hash__(self):
        return hash(str(self._pattern))


class Reference:
    """Represents a reference to a property key contained in a graph object or to the graph object itself."""

    def __init__(self, reference: GraphObject | Property):
        self.reference: GraphObject | Property = reference

    def __repr__(self):
        return f"{str(self.reference)}"

    def __hash__(self):
        return hash(str(self.reference))

    def get_graph_object(self) -> GraphObject:
        """:return: The graph object of the reference."""
        if isinstance(self.reference, GraphObject):
            return self.reference
        else:
            assert isinstance(self.reference, Property)
            return self.reference.graphObject


class Dependency:
    """Python implementation of an SLPGD.

    :param pattern: The pattern of the dependency.
    :param left: The left side of the dependency.
    :param right: The right side of the dependency, i.e, the references that depend on the :paramref:`left` side of the dependency.
    """

    def __init__(self, pattern, left: set[Reference], right: Reference):
        self.pattern: Pattern = pattern
        self.left: set[Reference] = left
        self.right: Reference = right

    def __repr__(self):
        return f"{self.pattern}:{", ".join(map(lambda x: str(x), self.left))} → {str(self.right)}"

    @property
    def is_trivial(self) -> bool:
        """:returns: whether the dependency is trivial, i.e., the reference on :paramref:`right` side is part of the set of references on the :paramref:`left` side of the dependency."""
        return reduce(
            lambda x, y: x or y, map(lambda elem: self.right == elem, self.left)
        )

    @property
    def is_inter_graph_object(self) -> bool:
        """:returns: whether the dependency is an inter-graph object dependency, i.e., it references more than one graph object."""
        graph_objects: set[GraphObject] = set()
        for reference in self.left:
            graph_objects.add(reference.get_graph_object())
        graph_objects.add(self.right.get_graph_object())

        return len(graph_objects) > 1

    @property
    def is_intra_graph_object(self) -> bool:
        """:returns: whether the dependency is an intra-graph object dependency, i.e., it references exactly one graph object."""
        return not self.is_inter_graph_object

    @classmethod
    def from_string(cls, string: str) -> Dependency:
        """Parse a SLPGD dependency from a string.

        :param string: The string representation of the SLPGD to create. Relies on this `syntax`.
        """
        # TODO: Insert proper link
        # TODO: put command for Antlr Generation into Docker!!
        # antlr4 -Dlanguage=Python3 -lib assets/gql-grammar/ -o slpgd/parser spgds.g4
        input_stream = InputStream(string)
        lexer = spgdsLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = spgdsParser(stream)
        tree = parser.dependency()
        listener = _MySLPGDListener()

        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.dependency


class _MySLPGDListener(spgdsListener):
    """`ANTLR listener <https://github.com/antlr/antlr4/blob/4.13.2/doc/listeners.md>`__ for the SLPGDs."""

    GraphObjectType = Enum(
        "GraphObjectType", [("Node", 0), ("EdgeLeft", 1), ("EdgeRight", 2)]
    )

    def __init__(self):
        self.dependency: Dependency | None = None
        self._variables: list = []
        self._graph_object_types: list[self.GraphObjectType] = []
        self.stack: list = []

    def exitElementPatternFiller(self, ctx: spgdsParser.ElementPatternFillerContext):
        #  print(ctx.getText())

        graph_object_type = self._graph_object_types[
            -1
        ]  # get the last entered graph object
        if len(self._graph_object_types) > 1:
            prior_graph_object_type = self._graph_object_types[-2]
        else:
            prior_graph_object_type = None

        if ctx.getChildCount() == 2:
            var_name_str = ctx.getChild(
                0
            ).getText()  # The first child is the variable declaration
            labels_str = (
                ctx.getChild(1).getChild(1).getText()
            )  # The second child of the second child is the string rep. of the graph object's labels
        elif ctx.getChildCount() == 1:
            if not ctx.getChild(0).getText().startswith(":"):
                var_name_str = ctx.getChild(
                    0
                ).getText()  # It is the variable declaration
                labels_str = None
            else:
                var_name_str = None
                labels_str = (
                    ctx.getChild(0).getChild(1).getText()
                )  # The second child of the child is the string rep. of the graph object's labels
        else:
            var_name_str, labels_str = None, None

        match graph_object_type:
            case self.GraphObjectType.Node:
                self._variables.append(Node(symbol=var_name_str, labels=labels_str))
                if len(self._variables) > 1:
                    match prior_graph_object_type:
                        case self.GraphObjectType.EdgeLeft:
                            self._variables[-2].src = self._variables[-1]
                        case self.GraphObjectType.EdgeRight:
                            self._variables[-2].tgt = self._variables[-1]
            case self.GraphObjectType.EdgeLeft:
                if len(self._variables) > 0:
                    assert isinstance(self._variables[-1], Node)
                    self._variables.append(
                        Edge(
                            symbol=var_name_str,
                            labels=labels_str,
                            src=None,
                            tgt=self._variables[-1],
                        )
                    )
            case self.GraphObjectType.EdgeRight:
                if len(self._variables) > 0:
                    assert isinstance(self._variables[-1], Node)
                    self._variables.append(
                        Edge(
                            symbol=var_name_str,
                            labels=labels_str,
                            src=self._variables[-1],
                            tgt=None,
                        )
                    )
        # print(self._variables)

    def exitPathPatternList(self, ctx: spgdsParser.PathPatternListContext):
        pattern = Pattern(
            ctx.getText(), set(self._variables)
        )  # set(filter(lambda x: x is None, map(lambda go: go.symbol, self._variables))))
        self.stack.append(pattern)

    def enterNodePattern(self, ctx: spgdsParser.NodePatternContext):
        self._graph_object_types.append(self.GraphObjectType.Node)

    # def enterEdgePattern(self, ctx:spgdsParser.EdgePatternContext):
    #     self._latest_graph_object = Edge

    def enterFullEdgePointingLeft(self, ctx: spgdsParser.FullEdgePointingLeftContext):
        self._graph_object_types.append(self.GraphObjectType.EdgeLeft)

    def enterFullEdgePointingRight(self, ctx: spgdsParser.FullEdgePointingRightContext):
        self._graph_object_types.append(self.GraphObjectType.EdgeRight)

    def exitReference(self, ctx: spgdsParser.ReferenceContext):
        graph_object_var = ctx.getChild(0).getText()
        if graph_object_var not in map(lambda x: x.symbol, self._variables):
            raise ValueError(
                f'The used variable "{graph_object_var}" has not been matched!'
            )
        graph_object = next(
            filter(lambda x: x.symbol == graph_object_var, self._variables)
        )
        reference: Reference
        if len(ctx.children) == 3:
            reference = Reference(Property(ctx.getChild(2).getText(), graph_object))
        else:
            assert len(ctx.children) == 1
            reference = Reference(graph_object)
        self.stack.append(reference)

    def exitLeft(self, ctx: spgdsParser.LeftContext):
        left: set[Reference] = set()

        for i in range(
            (len(ctx.children) // 2) + 1
        ):  # Division by 2 plus 1, as this is the actual number of references in the left side of the dependency (the children also include the commas between them i.e., a,b has a length of 3 but only 2 references
            left.add(self.stack.pop())

        self.stack.append(left)

    def exitDependency(self, ctx: spgdsParser.DependencyContext):
        right = self.stack.pop()
        left = self.stack.pop()
        pattern = self.stack.pop()
        self.dependency = Dependency(pattern, left, right)

    #  print(self.dependency)
