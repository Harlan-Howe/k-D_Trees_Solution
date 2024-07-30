from abc import ABC, abstractmethod
from typing import Tuple, Optional


class AbstractNode(ABC):  # ABC means this is an abstract class
    @abstractmethod
    def is_a_leaf(self):
        pass

    @abstractmethod
    def get_left(self) -> Optional["AbstractNode"]:
        pass

    @abstractmethod
    def get_right(self) -> Optional["AbstractNode"]:
        pass

    @abstractmethod
    def get_value(self) -> Optional[Tuple[float, ...]]:
        pass

    @abstractmethod
    def recursive_to_string(self, depth: int = 0) -> str:
        """
        creates a string that represents this tree, with data values indented to make it appear tree-like
        :param depth: the number of tabs we should add on the front end of each line of this string
        :return: the descriptive string, which may wind up incorporated in another string, as this is recursive.
        """
        pass

    @abstractmethod
    def find_nearest(self,
                     target: Tuple[float, ...],
                     best_value_so_far: Optional[Tuple[float, ...]],
                     best_distance_so_far: float,
                     visualizer=None) -> Tuple[Optional[Tuple[float, ...]], Optional[float]]:
        """
        finds the nearest datum to the given target, presumably better than the best_value_so_far, beating the
        best_distance_so_far. rRturns the datum and distance of a better point
        :param target:  the tuple of floats for which we are trying to find the closest tuple of points in our data set.
        :param best_value_so_far: the closest point to target found so far in this search process, before this call
        :param best_distance_so_far: the distance to the best_value_so_far.
        :param visualizer: if this is not none, then this will show our search in progress.
        :return: the (tuple of floats, distance to that tuple), if there is one better than the ones given as parameters;
        otherwise, (None, None).
        """
        pass

    def __repr__(self):  # equivalent to Java's toString()
        return self.recursive_to_string()

    def __str__(self):  # equivalent to Java's toString()
        return self.recursive_to_string()