import logging
import random

from AbstractNodeFile import AbstractNode
from typing import List, Tuple, Optional
from PointNodeFile import PointNode

from KinkaidDecorators import log_start_stop_method
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

    @log_start_stop_method
    def find_nearest(self,
                     target: Tuple[float, ...],
                     best_value_so_far: Optional[Tuple[float, ...]],
                     best_distance_so_far: float,
                     visualizer = None) -> Tuple[Optional[Tuple[float, ...]], Optional[float]]:
        """
        tries to find a datum closer to the target than the best_distance_so_far. If it finds one in either half of its
        split, returns the best datum and the shortest distance from the target; otherwise returns None for both.
        :param target: a data point for which we are searching for the nearest neighbor
        :param best_distance_so_far: the closest distance we have found from elsewhere on the tree.
        :param visualizer: a TwoDVisualizer used to show the progress of this search, if this is a 2d dataset.
        :return: Either (closest value, shortest distance) if we can improve on best_distance_so_far, or (None, None),
        otherwise.
        """
        found_better = False
        best_value = best_value_so_far
        best_distance = best_distance_so_far
        if target[self.get_axis()] < self.get_threshold():
            preferred_branch = self.get_left()
            secondary_branch = self.get_right()
        else:
            preferred_branch = self.get_right()
            secondary_branch = self.get_left()
        id = random.randint(0,1000)
        if preferred_branch is not None:
            logging.info(f"{id} going to preferred.")
            value, dist = preferred_branch.find_nearest(target, best_value, best_distance, visualizer=visualizer)

            if value is not None:
                found_better = True
                best_value = value
                best_distance = dist

        if visualizer is not None:
            visualizer.show_search_progress(target=target, best_point=best_value, axis=self.get_axis(), threshold=self.get_threshold(), wait_for_key=True)
        if secondary_branch is not None and abs(target[self.get_axis()] - self.get_threshold()) < best_distance:
            logging.info(f"{id} going to secondary.")
            value, dist = secondary_branch.find_nearest(target, best_value, best_distance, visualizer=visualizer)
            if value is not None:
                found_better = True
                best_value = value
                best_distance = dist

        else:
            if secondary_branch is None:
                logging.info(f"{id} no secondary to go to.")
            else:
                logging.info(f"{id} separation is {abs(target[self.get_axis()] - self.get_threshold())} and {best_distance=}")
        if found_better:

            return best_value, best_distance
        return None, None

