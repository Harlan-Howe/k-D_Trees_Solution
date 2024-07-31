import logging
import random

from AbstractNodeFile import AbstractNode
from typing import List, Tuple, Optional, Set
from PointNodeFile import PointNode

from KinkaidDecorators import log_start_stop_method
NUM_POINTS_FOR_MEDIAN = 10


class SplitterNode(AbstractNode):

    def __init__(self, axis: int = 0):
        # Note: variables with leading _ are intended as private variables.
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

    def is_a_leaf(self) -> bool:
        return False

    def get_left(self) -> Optional["AbstractNode"]:
        return self._left_node

    def get_right(self) -> Optional["AbstractNode"]:
        return self._right_node

    def get_value(self) -> Optional[Tuple[float, ...]]:
        return None

    def get_median_value(self, data_to_split: Set[Tuple[float, ...]]) -> float:
        """
        gets the median value along the current axis of a random subset of the given data (or all of the data),
        depending on NUM_POINTS_FOR_MEDIAN and the length of the dataset.
        :param data_to_split: the data in which to find the median value along the current axis.
        :return: a float of the median value along the current axis.
        """
        # TODO #0 - you've been given a variable, data_to_split, which consists of a Set of Tuples of floats. You also
        #           have a variable you can access via self.get_axis() that is the index of the item in all these tuples
        #           we care about....  [don't change anything here... move to #0a.]
        nums: List[float] = []
        if 0 < NUM_POINTS_FOR_MEDIAN < len(data_to_split):
            list_to_split = list(data_to_split)  # makes a list from the set.
            # TODO #0a - ... fill "nums" in with the items at the specified index for NUM_POINTS_FOR_MEDIAN entries in
            #            list_to_split.
        else:
            # TODO #0b - ... fill "nums" in with the items at the specified index for all the entries in data_to_split.
            for datum in data_to_split:
                nums.append(datum[self.get_axis()])

        # TODO #0c - return the median float value stored in "nums."
        return -1  # replace this!!!!

    def split_data(self, data_to_split: Set[Tuple[float, ...]]) -> Tuple[float,
                                                                         Set[Tuple[float, ...]],
                                                                         Set[Tuple[float, ...]]]:
        """
        determines a median value of the data_to_split (or a random subset of it) along the current axis and divides the
        data_to_split into two sets, one with the data on this axis below the median, and own with the data on this
        axis above the median. Any values of the data on this axis equal to the median are randomly distributed between
        the sets, so that all the data to split are placed into either the left or right set, and the sum of the
        left and right sets lengths match the length of data_to_split.
        :param data_to_split: the set we wish to divide
        :return: two subsets of the data_to_split.
        """
        threshold = self.get_median_value(data_to_split)
        left_set: Set[Tuple[float, ...]] = set(())  # create empty sets.
        right_set: Set[Tuple[float, ...]] = set(())

        for datum in data_to_split:
            # TODO #1 - for each datum, find the float stored at index self.get_axis(). If this is less than the
            #           threshold, put datum into the left set. If it is more than the threshold, put it into the right
            #           set. If it matches the threshold, "flip a coin" (each time) to decide which set to put it into.
            pass  # replace this line.

        return threshold, left_set, right_set

    def build_subtree(self, data_to_split: Set[Tuple[float, ...]], visualizer=None) -> None:
        """
        recursively build a tree from the data in the data_to_split set, with this SplitterNode as its root.
        :param data_to_split: the set of Tuples of floats that we wish to load into the tree.
        :param visualizer: if not None, this will display the creation of the data set in a 2-d format.
        :return: Nothing... but this SplitterNode will now be the root of a tree (or subtree).
        """
        self._dimension = len(next(iter(data_to_split)))  # this is a fancy way of getting one datum from the set.

        self._threshold, left_set, right_set = self.split_data(data_to_split)

        if visualizer is not None:
            visualizer.display()

        # TODO # 2a - If there is only one tuple in left_set, create a new PointNode based on that item, and set
        #             self._left_node to be that PointNode. (Hint: look at the first line of this method.) However,
        #             if there is more than one tuple in left_set, create a new SplitterNode, based on the next axis
        #             in the rotation after self.get_axis(), set the self._left_node to be that SplitterNode, and
        #             recursively tell that node to build subtree, based on the left set and the given visualizer.

        # TODO # 2b - Repeat 2a, only for the right side.

    # NOTE: "To do" number 3 is in PointNodeFile.py.

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
                     visualizer=None) -> Tuple[Optional[Tuple[float, ...]], Optional[float]]:
        """
        tries to find a datum closer to the target than the best_distance_so_far. If it finds one in either half of its
        split, returns the best datum and the shortest distance from the target; otherwise returns None for both.
        :param target: a data point for which we are searching for the nearest neighbor
        :param best_value_so_far: the closest datum found in previous steps of this search, or None if we haven't found
        one yet.
        :param best_distance_so_far: the closest distance we have found from elsewhere on the tree.
        :param visualizer: a TwoDVisualizer used to show the progress of this search, if this is a 2d dataset.
        :return: Either (closest value, shortest distance) if we can improve on best_distance_so_far, or (None, None),
        otherwise.
        """
        found_better = False
        best_value = best_value_so_far
        best_distance = best_distance_so_far

        # TODO #4a - You've got target, a tuple of floats; self.get_axis(); and self.get_threshold(). Assign
        #            preferred_branch to be either self.get_left() or self.get_right(). Then assign secondary_branch to
        #            be the other. Note that self.get_left() or self.get_right() could be None, a SplitterNode, or
        #            a PointNode... any of these are ok.
        preferred_branch: Optional[AbstractNode] = None  # replace these lines with your code.
        secondary_branch: Optional[AbstractNode] = None

        if preferred_branch is not None:
            value, dist = preferred_branch.find_nearest(target, best_value, best_distance, visualizer=visualizer)
            # TODO #4b - if you have a non-None value back, that means the recursive call found an improvement on
            #            previous search results. If so, update best_value, best_distance and found_better.
            pass  # replace this line.

        if visualizer is not None:  # if there is a visualizer, have it show what we've found so far and the distance
            #                         to the threshold line, then wait for key press.
            visualizer.show_search_progress(target=target,
                                            best_point=best_value,
                                            axis=self.get_axis(),
                                            threshold=self.get_threshold(),
                                            wait_for_key=True)

        # TODO # 4c - update the second half of the following "if" statement so that the secondary branch is only
        #             accessed if the target is closer to the threshold on this axis than the best_distance. (Otherwise,
        #             there's no point looking on the other side of the threshold!)
        if secondary_branch is not None and True:  # replace the "True" with your condition from #4c here.
            # TODO # 4d - do the same thing for secondary that happened up with # 4b, including the equivalent
            #            recursive call.
            pass  # replace this line.

        else:
            pass  # potentially put a debug statement here to explain why you aren't going to the secondary branch.

        if found_better:
            return best_value, best_distance
        return None, None

