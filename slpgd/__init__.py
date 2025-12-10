"""Python implementation of the SLPGDs for Labelled Property Grpahs (LPGs)"""
from __future__ import annotations

import abc
import io
import operator
from collections import namedtuple
from collections.abc import MutableSet
from itertools import accumulate, pairwise, count
from typing import Iterable, FrozenSet, NamedTuple, Callable

import neo4j
from functional_dependencies import FDSet, RelSchema, FD

from .dependency import *

OrderAndSchema = NamedTuple("OrderAndSchema", [("order", int), ("schema", FrozenSet[str])])


def _to_PascalCase(string: str) -> str:
    return string.replace(".", " ").title().replace(" ", "")

def _remove_properties_of_edge_endpoints(property_key: str,
                                         edge: Edge):
    prop_var = property_key.removeprefix("elementId(").removesuffix(")")
    return not (property_key.startswith("elementId(") and property_key.endswith(")") and
            (str(edge.src) == prop_var or str(edge.tgt) == prop_var))


def _merge_overlapping_order_and_schemata(set_of_order_and_schemata: set[OrderAndSchema],
                                          schema_condition: Callable[[list[OrderAndSchema]], bool] | None) -> set[OrderAndSchema]:
    """Takes a set of sets and returns a new set of sets where overlapping sets have been merged.
    Optionally, the merge may only happen when a condition on the to-be-merged sets is met."""
    list_of_order_and_schemata: list[OrderAndSchema] = list(set_of_order_and_schemata)
    merged_list_of_order_and_schemata: list[OrderAndSchema] = []

    merging = True
    i = 0

    while merging:
        if (len(merged_list_of_order_and_schemata) == 0 or
            (schema_condition is not None and not schema_condition([list_of_order_and_schemata[i]]))
        ):
            # If this is the first item in the new list or if it is not eligible for merging
            merged_list_of_order_and_schemata.append(list_of_order_and_schemata[i])
        else:
            assert len(merged_list_of_order_and_schemata) > 0
            # condition is no longer needed here
            for j in range(len(merged_list_of_order_and_schemata)):
                if not list_of_order_and_schemata[i].schema.isdisjoint(merged_list_of_order_and_schemata[j].schema) and schema_condition([list_of_order_and_schemata[i], merged_list_of_order_and_schemata[j]]):
                    merged_list_of_order_and_schemata[j] = OrderAndSchema(
                        list_of_order_and_schemata[i].order,
                        merged_list_of_order_and_schemata[j].schema.union(list_of_order_and_schemata[i].schema)
                    )
                    break # If a merge has occurred there cannot occur a further merge --> break the loop!
                merged_list_of_order_and_schemata.append(list_of_order_and_schemata[i])

        i += 1
        if i >= len(list_of_order_and_schemata):
            merging = False

    return set(merged_list_of_order_and_schemata)

class DependencySet(set):
    """A subclass of :class:`set` providing functionalities for working with set of dependencies."""
    def __init__(self, dependencies: Iterable[Dependency]):
        """A set of SLPGDs."""
        if not accumulate(map(lambda x: isinstance(x, Dependency), dependencies), operator.__and__):
            raise ValueError("Not all of the provided \"dependencies\" are an instance of Dependency.")
        if not accumulate(map(lambda x: x[0].pattern == x[1].pattern, pairwise(dependencies)), operator.__and__):
            raise ValueError("Not all of the provided Dependencies have the same pattern.")
        super().__init__(dependencies)


    @classmethod
    def from_string_list(cls, lst: list[str]) -> DependencySet:
        """Creates a :class:`DependencySet` from a list of dependencies encoded as strings."""
        return cls(map(Dependency.from_string, lst))

    def add(self, element: Dependency):
        if not isinstance(element, Dependency):
            raise ValueError("The provided \"dependency\" is not an instance of Dependency.")
        if element.pattern == self.dependency_pattern:
            raise ValueError("Not all of the provided Dependencies have the same pattern.")

        super().add(element)

    def peek(self) -> Dependency:
        """Retrieves one dependency of the set of dependencies *without* removing it from the set.

        :returns: A dependency of the set of dependencies.
        """
        return next(iter(self))

    def infer_structural_deps(self, con: neo4j.Driver, database: str = "neo4j", except_dependants: set[Reference] | None = None) -> DependencySet:
        """Infers structural dependencies based on the pattern of the dependencies already contained in a DependencySet.
        A relational projection of the graph objects of the provided graph pattern is performed to retrieve all possible structural dependencies.

        :raises ValueError: If there are no dependencies yet in the dependency set."""

        if self.__len__() == 0:
            raise ValueError("This DependencySet is empty, thus no structural dependencies can be inferred.")

        # Phase 1: add source and target of edges as inferred deps
        for edge in filter(lambda e: isinstance(e, Edge), self.dependency_pattern.graph_objects):

            if edge.src.symbol is not None:
                inferred_dep: Dependency = Dependency.from_string(
                    f"{self.dependency_pattern}:{edge.symbol}->{edge.src.symbol}")
                if except_dependants is None or inferred_dep.right not in except_dependants:
                    # There is a named source of the edge in the pattern
                    self.add(inferred_dep)
            if edge.tgt.symbol is not None:
                inferred_dep: Dependency = Dependency.from_string(
                    f"{self.dependency_pattern}:{edge.symbol}->{edge.tgt.symbol}")
                if except_dependants is None or inferred_dep.right not in except_dependants:
                    # There is a named target of the edge in the pattern
                    self.add(inferred_dep)


        # Phase 2: add dependencies for all properties of each named matched graph object
        vars_in_pattern = self.dependency_pattern_variable_symbols

        for var in vars_in_pattern:
            result = con.execute_query(
                f"""MATCH {self.dependency_pattern} 
                    WITH KEYS({var}) AS keys
                    UNWIND keys AS key
                    RETURN COLLECT(DISTINCT key) AS props""",
                database_=database,
            )
            properties = dict(result[0][0])["props"]
            for prop in properties:
                inferred_dep: Dependency = Dependency.from_string(
                    f"{self.dependency_pattern}:{var}->{var}.{prop}")
                if except_dependants is None or inferred_dep.right not in except_dependants:
                    self.add(inferred_dep)

        return self

    @property
    def dependants(self) -> set[Reference]:
        """:returns: a set of all dependant references, i.e., references on the right side of a :class:`Dependency` contained within this DependencySet."""
        return set(map(lambda x: x.right, iter(self)))

    @property
    def dependency_pattern(self) -> Pattern:
        """:returns: the pattern of all dependencies contained within this :class:`DependencySet`."""
        return next(iter(self)).pattern

    @property
    def dependency_pattern_variable_symbols(self) -> set[str]:
        """:returns: a set of all symbols contained within the pattern of the dependencies in this set."""
        return set(filter(lambda x: x is not None, map(lambda x: x.symbol, self.dependency_pattern.graph_objects)))

    def _rel_schema_and_minimal_cover(self) -> RelSchema:
        set_of_rel_fds = FDSet()
        for dep in iter(self):
            left = set(map(lambda x: str(x), dep.left))
            right = {str(dep.right)}
            set_of_rel_fds.add(FD(left, right))

        minimal_cover = set_of_rel_fds.basis()
        rel_schema = RelSchema(set_of_rel_fds.attributes(), minimal_cover)
        return rel_schema

    def get_transformations_rel_synthesize(self, con: neo4j.Driver, database = "neo4j") -> tuple[list[str], str]:
        """Calculates a list of GQL/Cypher queries to normalize a graph that matches the :attr:`dependency_pattern`.

        :returns: a list of the GQL/Cypher queries for normalizing the graph"""
        transformations: list[str] = []
        new_pattern_list = [str(self.dependency_pattern)]


        # 1. Create rel. projection of the graph pattern
        rel_schema = self._rel_schema_and_minimal_cover()
        print(rel_schema)
        # 2. Perform normalization of this
        rel_synthesis = rel_schema.synthesize()
        rel_synthesis_order_and_schemata_non_merged: set[OrderAndSchema] = set()
        rel_synthesis_order_and_schemata: set[OrderAndSchema]


        def _allowed_to_merge(order_schemata: list[OrderAndSchema]) -> bool:
            allowed = True
            for order_schema in order_schemata:
                if sum(map(lambda x: x.startswith("elementId(") and x.endswith(")"), order_schema.schema)) == 1:
                    graph_object_var: str = next(filter(lambda x: x.startswith("elementId(") and x.endswith(")"),
                                                        order_schema.schema)).removeprefix("elementId(").removesuffix(")")
                    graph_object: GraphObject = self.dependency_pattern.get_graph_object_by_symbol(graph_object_var)
                    if isinstance(graph_object, Node):
                        allowed = allowed and True
                    else:
                        allowed = False
                else:
                    allowed = False
            return allowed

        for schema in rel_synthesis:
            item: OrderAndSchema = OrderAndSchema(len(set(filter(lambda x: "." not in x, schema.attributes))), frozenset(map(lambda x: f"elementId({x})" if "." not in x else x, schema.attributes)))
            rel_synthesis_order_and_schemata_non_merged.add(item)

        # Merge schemata representing nodes that have the same node
        rel_synthesis_order_and_schemata: set[OrderAndSchema] = _merge_overlapping_order_and_schemata(rel_synthesis_order_and_schemata_non_merged, _allowed_to_merge)
        rel_synthesis_order_and_schemata: list[OrderAndSchema] = list(rel_synthesis_order_and_schemata)

        rel_synthesis_order_and_schemata.sort(key=lambda x: x.order)

        # 2. For each rel. schema compare it with individual schemata of the graph objects before normalization to retrieve transformations
        i = 0 # counter is used for retrieving unique query variables
        properties_to_remove: set[str] = set()

        query_vars_schema_dict: dict[str,frozenset[str]] = {}
        for order_schema in rel_synthesis_order_and_schemata:
            ids_in_schema = set(filter(lambda x: x.startswith("elementId(") and x.endswith(")"), order_schema.schema)) # determines the "order" of the schema
            id_vars_in_schemata = set(map(lambda x: x.removeprefix("elementId(").removesuffix(")"), ids_in_schema))

            schema_after_norm = order_schema.schema
            match order_schema.order:
                case 0:
                    # The schema is new --> will be new node attached to another node
                    label = _to_PascalCase(" ".join(sorted(list(schema_after_norm))))

                    for prop in schema_after_norm:
                        var = prop.split(".")[0]
                        go = self.dependency_pattern.get_graph_object_by_symbol(var)
                        if isinstance(go, Node) and len(set(filter(lambda dep: prop != str(dep.right) , iter(self)))) > 0: # Foreign keys (i.e., the property responsible for an edge in the graph are never the determined attribute in a relation
                            transformations.append(f"""
MATCH {self.dependency_pattern} MERGE (:{label} {{
{",\n".join(map(lambda x: f"{_to_PascalCase(x)}: {x}", schema_after_norm))}
}})
""")
                            transformations.append(f"""
MATCH {self.dependency_pattern}, (x{i}:{label}) 
WHERE 
{" AND ".join(map(lambda x: f"{x}=x{i}.{_to_PascalCase(x)}", schema_after_norm))}
MERGE (x{i})<-[:{label}]-({var})
""")
                            # <-[:{_to_PascalCase(prop)}]-({var})
                            new_pattern_list.append(f"(x{i}:{label})<-[:{_to_PascalCase(prop)}]-({var})")
                          #  break # create only one node for a relation!!!
                    query_vars_schema_dict[f"x{i}"] = schema_after_norm

                    properties_to_remove = properties_to_remove.union(schema_after_norm)

                    i += 1
                    #
                    # for prop in properties_to_remove:
                    #     if prop.startswith(f"{var}."):
                    #         for edge_tgt in query_vars_schema_dict.keys():
                    #             if prop in query_vars_schema_dict[edge_tgt]:
                    #                 transformations.append(f"""
                    #         MATCH {"\nMATCH ".join(new_pattern_list)}
                    #         CREATE ({var})-[x{i}:{prop.replace(".", "").upper()}]->({edge_tgt})""")
                    #                 new_pattern_list.append(
                    #                     f"({var})-[x{i}:{prop.replace(".", "").upper()}]->({edge_tgt})")
                    #                 # TODO: optimize new pattern match list
                    #                 i += 1
                    #                 # Break the loop here to not have "redundant" edges (from foreign keys)


                    pass
                case 1:
                    # This schema represents objects that existed already before normalization
                    var = id_vars_in_schemata.pop()

                    result = con.execute_query(
                                f"""MATCH {self.dependency_pattern} 
WITH  KEYS({var}) AS keys
UNWIND keys AS key
RETURN COLLECT(DISTINCT key) AS props""",
                                database_= database,
                                # result_transformer_=Result.
                            )
                    properties = dict(result[0][0])["props"]
                    original_schema = set(map(lambda x: f"{var}.{x}", properties))
                    original_schema.add(f"elementId({var})")

                    if len(original_schema - original_schema.intersection(schema_after_norm)) > 0:
                        # Not all of the original properties have been retained --> remove the ones that are no longer present
                        properties_to_remove = properties_to_remove.union(original_schema - original_schema.intersection(schema_after_norm))



                    additional_props = set(schema_after_norm - original_schema)
                    # In case of an edge: check whether they are not the elementId of an edge
                    if isinstance(self.dependency_pattern.get_graph_object_by_symbol(var), Edge):
                        edge: Edge = self.dependency_pattern.get_graph_object_by_symbol(var)
                        additional_props = set(
                            filter(lambda x: _remove_properties_of_edge_endpoints(x, edge), additional_props))
                    if len(additional_props) > 0:
                        # There are new properties in the graph object after normalization
                        transformations.append(f"""
MATCH {self.dependency_pattern} 
SET {",\n".join(map(lambda prop: f"{var}.{_to_PascalCase(prop)} = {prop}", additional_props))} 
                    """) # TODO: discuss whether to use the backtick and original name or the camelcase version

                    query_vars_schema_dict[var] = schema_after_norm
                    pass



                case 2 | 3:
                    # TODO: Add edge check!! Nodes cannot have more than one id in them! edges can have up to three!
                    var = set(filter(lambda x: x not in query_vars_schema_dict.keys(), id_vars_in_schemata)).pop()
                    # Since all variables of lower order have already been processed
                    result = con.execute_query(
                        f"""MATCH {self.dependency_pattern} 
                    WITH  KEYS({var}) AS keys
                    UNWIND keys AS key
                    RETURN COLLECT(DISTINCT key) AS props""",
                        database_=database,
                        # result_transformer_=Result.
                    )
                    properties = dict(result[0][0])["props"]
                    original_schema = set(map(lambda x: f"{var}.{x}", properties))
                    original_schema.add(f"elementId({var})")

                    if len(original_schema.intersection(schema_after_norm)) != len(original_schema):
                        # Not all of the original properties have been retained --> remove the ones that are no longer present
                        properties_to_remove = properties_to_remove.union(original_schema - original_schema.intersection(schema_after_norm))

                    additional_props = set(schema_after_norm - original_schema)
                    # In case of an edge: check whether they are not the elementId of an edge
                    if isinstance(self.dependency_pattern.get_graph_object_by_symbol(var), Edge):
                        edge: Edge = self.dependency_pattern.get_graph_object_by_symbol(var)
                        additional_props = set(
                            filter(lambda x: _remove_properties_of_edge_endpoints(x, edge), additional_props))

                    if len(additional_props) > 0:
                        # There are new properties in the graph object after normalization
                        transformations.append(f"""
MATCH {self.dependency_pattern} 
SET {",\n".join(map(lambda prop: f"{var}.{_to_PascalCase(prop)} = {prop}", additional_props))} 
                                            """)  # TODO: discuss whether to use the backtick and original name or the camelcase version

                    query_vars_schema_dict[var] = schema_after_norm
                    pass
                case _:
                    pass
                    # TODO: If this is reached there were problems with the dependencies ...

        if len(properties_to_remove) > 0:
            transformations.append(f"""
MATCH {self.dependency_pattern} 
REMOVE {", ".join(properties_to_remove)}
""")

        return transformations, ", ".join(new_pattern_list)

        #
        #     st.text(list(map(lambda x: (x.symbol, type(x)), st.session_state.dependencies[0].pattern.graph_objects)))
        #     if count_of_ids == 1:
        #         var = next(filter(lambda x: x.startswith("elementId(") and x.endswith(")"), schema)).removeprefix("elementId(").removesuffix(")")
        #         with GraphDatabase.driver(URI, auth=AUTH) as driver:
        #             result = driver.execute_query(
        #                 f"""MATCH {str(st.session_state.concat_of_patterns)}
        #         WITH  KEYS({var}) AS keys
        #         UNWIND keys AS key
        #         RETURN COLLECT(DISTINCT key) AS props""",
        #                 database_=DATABASE,
        #                 # result_transformer_=Result.
        #             )
        #             properties = dict(result[0][0])["props"]
        #         original_properties = set(map(lambda x: f"{var}.{x}", properties))
        #         original_properties.add(f"elementId({var})")
        #         st.text(original_properties)
        #         normalized_properties = set(schema.columns.values)
        #         new_properties = normalized_properties - original_properties
        #         if len(new_properties) > 0:
        #             st.text(f"New property(s) in node: {new_properties}")
        #             for prop in new_properties:
        #                 with GraphDatabase.driver(URI, auth=AUTH) as driver:
        #                     _ = driver.execute_query(
        #                         f"""MATCH {str(st.session_state.concat_of_patterns)}
        #                                     SET {var}.`{prop}` = {prop}""",
        #                         database_=DATABASE,
        #                         # result_transformer_=Result.
        #                     )
        #                     _ = driver.execute_query(
        #                         f"""MATCH {str(st.session_state.concat_of_patterns)}
        #                                    REMOVE {prop}""",
        #                         database_=DATABASE,
        #                         # result_transformer_=Result.
        #                     )
        #     if count_of_ids == 2:
        #         pass
        #         # an edge schema
        #
        #     if count_of_ids == 0:
        #         # a new node has to be created ...
        #         pass

    def __str__(self):
        return "\n".join(map(str, iter(self)))







