from __future__ import annotations

__author__ = "Johannes Schrott"
__email__ = "johannes.schrott@tuwien.ac.at"


from .gnfd import *
import neo4j

__all__ = ['Node','Edge','GNFD','LeftEdge','Pattern','PatternConcat','RightEdge','DependencySet']

class DependencySet(set[GNFD]):
    @classmethod
    def from_string_list(cls, lst: list[str]) -> DependencySet:
        """Creates a :class:`DependencySet` from a list of dependencies encoded as strings."""
        return cls(map(GNFD.from_string, lst))

    def get_normal_form(self, session: neo4j.Session) -> str:
        """
        :param session: A session that is connected to a Neo4J compatible database
        :returns: the normal form of the graph in the Neo4J compatible database under this set of dependencies."""
        res: str

        return "to be implemented"
        # if self.is_in_global_normal_form():
        #     res = "global GN-"
        # else:
        #     res = "GN-"
        #
        # if self.is_in_bcnf(session):
        #     res += "BCNF"
        # elif self.is_in_3nf(session):
        #     res += "3NF"
        # elif self.is_in_2nf(session):
        #     res += "2NF"
        # elif self.is_in_1nf(session):
        #     res += "1NF"
        # else:
        #     res += "0NF"
        #
        # return res

    def is_in_global_normal_form(self) -> bool:
        """:returns: :any:`True` when there is no inter-graph dependency, :any:`False` otherwise."""
        return sum(map(lambda dep: dep.is_inter_graph_object, self)) == 0

    @property
    def lp_suitable(self) -> bool:
        """:returns: :any:`True` when LP normalization (cf. <https://doi.org/10.1007/s00778-025-00902-2>) could be performed on this graph as its dependencies only target nodes and there are no inter graph dependencies."""
        return self.is_in_global_normal_form() and reduce(operator.and_,
                                                          map(lambda dep: dep.is_within_node, iter(self)))
