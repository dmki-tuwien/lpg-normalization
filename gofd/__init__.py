from __future__ import annotations

__author__ = "Johannes Schrott"
__email__ = "johannes.schrott@tuwien.ac.at"


from .gnfd import *
import neo4j

__all__ = ['Node','Edge', 'GOFD', 'LeftEdge', 'Pattern', 'PatternConcat', 'RightEdge', 'DependencySet']

class DependencySet(set[GOFD]):
    @classmethod
    def from_string_list(cls, lst: list[str]) -> DependencySet:
        """Creates a :class:`DependencySet` from a list of dependencies encoded as strings."""
        return cls(map(GOFD.from_string, lst))


    def is_in_global_normal_form(self) -> bool:
        """:returns: :any:`True` when there is no inter-graph dependency, :any:`False` otherwise."""
        return sum(map(lambda dep: dep.is_inter_graph_object, self)) == 0

    @property
    def lp_suitable(self) -> bool:
        """:returns: :any:`True` when LP normalization (cf. <https://doi.org/10.1007/s00778-025-00902-2>) could be performed on this graph as its dependencies only target nodes and there are no inter graph dependencies."""
        return self.is_in_global_normal_form() and reduce(operator.and_,
                                                          map(lambda dep: dep.is_within_node, iter(self)))
