import random

from AbstractNodeFile import AbstractNode
from typing import List, Tuple, Optional
from PointNodeFile import PointNode


NUM_POINTS_FOR_MEDIAN = 10


class SplitterNode(AbstractNode):

    def __init__(self, axis: int):
        self._axis: int = axis
        self._dimension = -1
        self._left_node: Optional[AbstractNode] = None  # Optional means it could be a Node, or it could be None.
        self._right_node: Optional[AbstractNode] = None
        self._threshold: float = -1

    def get_axis(self) -> int:
        return self._axis

    def get_dimension(self) -> int:
        return self._dimension

    def get_threshold(self) -> float:
        return self._threshold

    def is_a_leaf(self):
        return False

    def get_left(self) -> Optional["AbstractNode"]:
        return self._left_node

    def get_right(self) -> Optional["AbstractNode"]:
        return self._right_node

    def get_value(self) -> Optional[Tuple[float, ...]]:
        return None

    def recursive_to_string(self, depth: int = 0) -> str:
        return "To String not yet implemented"

    def split_data(self, data_to_split: List[Tuple[float, ...]]) -> Tuple[float,
                                                                          List[Tuple[float, ...]],
                                                                          List[Tuple[float, ...]]]:
        """
        determines a median value of the data_to_split (or a random subset of it) along the current axis and divides the
        data_to_split into two lists, one with the data on this axis below the median, and own with the data on this
        axis above or equal to the median.
        :param data_to_split: the list we wish to divide
        :return: two sublists of the data_to_split.
        """
        threshold = self.get_median_value(data_to_split)
        left_list: List[Tuple[float, ...]] = []
        right_list: List[Tuple[float, ...]] = []

        for i in range(len(data_to_split)):
            if data_to_split[i][self.get_axis()] < threshold:
                left_list.append(data_to_split[i])
            else:
                right_list.append(data_to_split[i])
        return threshold, left_list, right_list

    def get_median_value(self, data_to_split: List[Tuple[float, ...]]) -> float:
        """
        gets the median value along the current axis of a random subset of the given data (or all of the data),
        depending on NUM_POINTS_FOR_MEDIAN and the length of the dataset.
        :param data_to_split: the data in which to find the median value along the current axis.
        :return: a float of the median value along the current axis.
        """
        nums: List[float] = []
        if NUM_POINTS_FOR_MEDIAN > 0 and NUM_POINTS_FOR_MEDIAN > len(data_to_split):
            for i in range(NUM_POINTS_FOR_MEDIAN):
                nums.append(data_to_split[random.randint(0, len(data_to_split) - 1)][self.get_axis()])
        else:
            for i in range(len(data_to_split)):
                nums.append(data_to_split[i][self.get_axis()])

        nums.sort()
        return nums[int(len(nums) / 2)]

    def build_subtree(self, data_to_split: List[Tuple[float, ...]], visualizer=None) -> None:
        self._dimension = len(data_to_split[0])
        self._threshold, left_list, right_list = self.split_data(data_to_split)
        if visualizer is not None:
            visualizer.display()
        if len(left_list) == 1:
            self._left_node = PointNode(left_list[0])

        elif len(left_list) > 1:
            self._left_node = SplitterNode(axis=(self.get_axis() + 1) % self.get_dimension())
            self._left_node.build_subtree(data_to_split=left_list,
                                          visualizer=visualizer)


        if len(right_list) == 1:
            self._right_node = PointNode(right_list[0])

        elif len(right_list) > 1:
            self._right_node = SplitterNode(axis=(self.get_axis() + 1) % self.get_dimension())
            self._right_node.build_subtree(data_to_split=right_list,
                                           visualizer=visualizer)


    def recursive_to_string(self, depth: int = 0) -> str:
        if self.get_left() is None:
            left_string = ""
        else:
            left_string = self.get_left().recursive_to_string(depth=depth+1)
        if self.get_right() is None:
            right_string = ""
        else:
            right_string = self.get_right().recursive_to_string(depth=depth+1)
        descriptor = "\t" * depth + f"axis: {self.get_axis()} | threshold: {self.get_threshold()}\n"
        return left_string + descriptor + right_string
