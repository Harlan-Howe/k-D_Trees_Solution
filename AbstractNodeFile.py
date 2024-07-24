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
        pass

    @abstractmethod
    def find_nearest(self,
                     target: Tuple[float, ...],
                     best_distance_so_far: float) -> Tuple[Optional[Tuple[float, ...]], Optional[float]]:
        pass

    def __repr__(self):
        return self.recursive_to_string()

    def __str__(self):
        return self.recursive_to_string()