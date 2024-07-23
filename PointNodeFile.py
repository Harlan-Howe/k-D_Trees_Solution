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

