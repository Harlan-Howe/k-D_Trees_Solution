import logging
import math
from typing import Tuple, Optional

from AbstractNodeFile import AbstractNode


class PointNode(AbstractNode):
    def __init__(self, value: Tuple[float, ...]):
        self._value = value

    def is_a_leaf(self):
        return True

    def get_left(self) -> Optional["AbstractNode"]:
        return None

    def get_right(self) -> Optional["AbstractNode"]:
        return None

    def get_value(self) -> Optional[Tuple[float, ...]]:
        return self._value

    def recursive_to_string(self, depth: int = 0) -> str:
        return "\t" * depth + str(self._value) + "\n"

    def find_nearest(self,
                     target: Tuple[float, ...],
                     best_value_so_far: Optional[Tuple[float, ...]],
                     best_distance_so_far: float,
                     visualizer=None) -> Tuple[Optional[Tuple[float, ...]], Optional[float]]:
        """
        finds the distance between the target and this node's value. If this distance is shorter than the best distance
        found so far, returns this node's value and the distance we just found. Otherwise, returns None for both value
        and distance.
        :param target: the datum for which we are trying to find a nearest neighbor
        :param best_value_so_far: the closest datum found previously in this search process, or None if we haven't found
        one.
        :param best_distance_so_far: the distance from the target upon which we are trying to improve
        :param visualizer: a hook to a visualizer, so we can see progress if this is 2-d. Not used.
        :return: (value, distance) if we can improve, (None, None) otherwise.
        """
        # TODO #3 - both target and self._value are Tuples of floats (e.g., (0.707, 0.707) or (1.0, 2.0, 3.0, 4.0))
        #           with the same (unspecified) number of floats in them. You need to find the distance between them
        #           via Pythagoras - the square root of the sum of the squares of the differences of the pairs.
        distance = float('inf')  # replace this line.

        # ---------- put the "to do" #3 code above this line.
        if distance < best_distance_so_far:
            logging.info(f"Found an improvement: {distance=}")
            if visualizer is not None:
                visualizer.show_search_progress(target=target, best_point=self._value, wait_for_key=True)
            return self._value, distance
        else:
            return None, None

