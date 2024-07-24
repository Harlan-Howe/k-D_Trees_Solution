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
                     best_distance_so_far: float) -> Tuple[Optional[Tuple[float, ...]], Optional[float]]:
        distance_squared = 0
        for i in range(len(self._value)):
            distance_squared += pow(target[i]-self._value[i], 2)
        distance = math.sqrt(distance_squared)
        if distance < best_distance_so_far:
            return self._value, distance
        else:
            return None, None

