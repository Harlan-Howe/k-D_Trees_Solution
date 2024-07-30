import math
import random

import cv2
import numpy as np
from typing import List, Tuple, Optional, Set

from AbstractNodeFile import AbstractNode
from SplitterNodeFile import SplitterNode

SCALE = 4
MARGIN = 10
DELAY_MS = 250

class TwoDVisualizer:

    def __init__(self, root: Optional[AbstractNode] = None, data: Optional[Set[Tuple[float, ...]]] = None):
        self.myCanvas = None
        self.clear()
        self.rect_stack: Optional[List[Tuple[float, float, float, float]]] = None  # used later to display the boxes.
        self._root = root  # a SplitterNode that will serve as the root of the tree displayed by this visualizer.
        self._data = data  # a set of the Tuples of floats that are being incoporated into the tree and should be drawn
        #                    as dots later.

    def set_root(self, root: AbstractNode):
        self._root = root

    def has_root(self) -> bool:
        return self._root is not None

    def clear(self) -> None:
        """
        creates a blank canvas.
        :return: None
        """
        self.myCanvas = np.zeros((200*SCALE+2*MARGIN, 200*SCALE+2*MARGIN, 3), dtype=float)

    def display(self, wait_for_key: bool = False) -> None:
        """
        draws all the data points and a representation of the tree, updates the "Data" window, and either waits for
        the user to press a key or for DELAY_MS milliseconds before returning from this method
        :param wait_for_key: whether to wait for a keypress or a given amount of time after displaying the window.
        :return: None
        """
        self.clear()
        self.show_dots_and_divisions()

        cv2.imshow("Data", self.myCanvas)
        if wait_for_key:
            cv2.waitKey()
        else:
            cv2.waitKey(DELAY_MS)

    def show_dots_and_divisions(self):
        """
        draws all the data points and the structure of the tree to self.myCanvas.
        :return: None
        """
        for d in self._data:
            cv2.circle(img=self.myCanvas, center=(int(MARGIN + 2 * SCALE * d[0]), int(MARGIN + 2 * SCALE * d[1])),
                       radius=SCALE,
                       color=(0.5, 0.5, 0.5), thickness=-1)
        self.rect_stack = [(0, 0, 100, 100)]  # a stack keeping track of which rectangular area is currently being
        #                                       subdivided.
        self.display_subtree(self._root)

    def display_subtree(self, sub_root: Optional[AbstractNode]):
        """
        recursively draws the structure of this tree to the self.myCanvas array, for display later.
        :param sub_root: the root of the subtree under consideration, which will be taking place in the area outlined
        by the rectangle at the top of the self.rect_stack.
        :return: None
        """
        rect = self.rect_stack.pop(-1)  # get the top rectangle, which should hold all the data points in this subtree.
        if sub_root is None:
            return

        if sub_root.is_a_leaf():
            pt = sub_root.get_value()
            cv2.circle(img=self.myCanvas,
                       center=(int(MARGIN+2 * SCALE * pt[0]), int(MARGIN+2 * SCALE * pt[1])),
                       radius=SCALE,
                       color=(1.0, 1.0, 1.0), thickness=-1)
        else:
            splitter: SplitterNode = sub_root
            axis = splitter.get_axis()
            threshold = splitter.get_threshold()
            if axis == 0:  # split this rectangle horizontally into a left portion and a right portion.
                left_rect = (rect[0], rect[1], threshold, rect[3])
                right_rect = (threshold, rect[1], rect[2], rect[3])
                cv2.rectangle(img=self.myCanvas,
                              pt1=(int(MARGIN + 2 * SCALE * left_rect[0]), int(MARGIN + 2 * SCALE * left_rect[1])),
                              pt2=(int(MARGIN + 2 * SCALE * left_rect[2]), int(MARGIN + 2 * SCALE * left_rect[3])),
                              color=(1.0, 0.5, 0.5),
                              thickness=1)
                self.rect_stack.append(left_rect)
                cv2.rectangle(img=self.myCanvas,
                              pt1=(int(MARGIN + 2 * SCALE * right_rect[0]), int(MARGIN + 2 * SCALE * right_rect[1])),
                              pt2=(int(MARGIN + 2 * SCALE * right_rect[2]), int(MARGIN + 2 * SCALE * right_rect[3])),
                              color=(1.0, 0.5, 0.5),
                              thickness=1)
                self.rect_stack.append(right_rect)
                self.display_subtree(sub_root.get_right())
                self.display_subtree(sub_root.get_left())
            else:  # split this rectangle vertically into a top portion and a bottom portion
                top_rect = (rect[0], rect[1], rect[2], threshold)
                bottom_rect = (rect[0], threshold, rect[2], rect[3])
                cv2.rectangle(img=self.myCanvas,
                              pt1=(int(MARGIN + 2 * SCALE * top_rect[0]), int(MARGIN + 2 * SCALE * top_rect[1])),
                              pt2=(int(MARGIN + 2 * SCALE * top_rect[2]), int(MARGIN + 2 * SCALE * top_rect[3])),
                              color=( 0.5, 0.5, 1.0),
                              thickness=1)
                self.rect_stack.append(top_rect)
                cv2.rectangle(img=self.myCanvas,
                              pt1=(int(MARGIN + 2 * SCALE * bottom_rect[0]), int(MARGIN + 2 * SCALE * bottom_rect[1])),
                              pt2=(int(MARGIN + 2 * SCALE * bottom_rect[2]), int(MARGIN + 2 * SCALE * bottom_rect[3])),
                              color=(0.5, 0.5, 1.0),
                              thickness=1)
                self.rect_stack.append(bottom_rect)
                self.display_subtree(sub_root.get_right())
                self.display_subtree(sub_root.get_left())

    def show_search_progress(self,
                             target: Tuple[float, ...],
                             best_point: Optional[Tuple[float, ...]],
                             axis: int = -1,
                             threshold: float = -1,
                             wait_for_key: bool = False) -> None:
        """
        Draws the data and tree into self.myCanvas, but also shows the target datum, the closest datum found so far (if
        any) and potentially a horizontal or vertical line to the nearest threshold line, highlighting that line across
        the screen.
        :param target: the datum point from which we are searching for a nearby point.
        :param best_point: if not None, draw this datum dot and draw a line from the target to this point. Draw a circle
        around the target intersecting this point.
        :param axis: the direction the line to the threshold should go (0 -> horizontal, 1 -> vertical, -1 -> No line)
        :param threshold: the x- or y- value at which the axis line should stop. The line should extend in the given
        direction (by axis) from the target point to this value.
        :param wait_for_key: whether to wait for the user to press a key before we return, or we should wait a specified
        amount of time (DELAY_MS).
        :return: None
        """
        self.clear()
        self.show_dots_and_divisions()
        # draw the target dot in green.
        cv2.circle(img=self.myCanvas,
                   center=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                   radius=SCALE,
                   color=(0, 1.0, 0),
                   thickness=-1)

        if best_point is not None:  # draw the line from target to best point and the large circle around target.
            d = math.sqrt(pow(target[0] - best_point[0], 2)+pow(target[1] - best_point[1], 2))
            cv2.line(img=self.myCanvas,
                     pt1=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                     pt2=(int(MARGIN + 2 * SCALE * best_point[0]), int(MARGIN + 2 * SCALE * best_point[1])),
                     color=(0, 1.0, 0),
                     thickness=1)
            cv2.circle(img=self.myCanvas,
                       center=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                       radius=int(2 * SCALE * d),
                       color=(0, 1.0, 0),
                       thickness=1)

        # if a threshold is given, draw a horizontal or vertical yellow line from target to that threshold.
        if threshold > -1:
            edge_pt = [target[0], target[1]]
            edge_pt[axis] = threshold
            cv2.line(img=self.myCanvas,
                     pt1=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                     pt2=(int(MARGIN + 2 * SCALE * edge_pt[0]), int(MARGIN + 2 * SCALE * edge_pt[1])),
                     color=(0, 1.0, 1.0),
                     thickness=1)
            # ... and highlight that threshold in green.
            overlay = self.myCanvas.copy()
            if axis == 1:  # horizontal line to threshold, so threshold itself is vertical.
                cv2.line(img=overlay,
                         pt1=(MARGIN, int(MARGIN + 2 * SCALE * edge_pt[1])),
                         pt2=(int(MARGIN + 2 * SCALE * 100), int(MARGIN + 2 * SCALE * edge_pt[1])),
                         color=(0, 1.0, 0),
                         thickness=3)
            else:  # vertical line to threshold, so threshold itself is horizontal.
                cv2.line(img=overlay,
                         pt1=(int(MARGIN + 2 * SCALE * edge_pt[0]), MARGIN),
                         pt2=(int(MARGIN + 2 * SCALE * edge_pt[0]), int(MARGIN + 2 * SCALE * 100)),
                         color=(0, 1.0, 0),
                         thickness=3)
            self.myCanvas = cv2.addWeighted(overlay, 0.3, self.myCanvas, 0.7, 0)  # blend to give line 0.3 translucency

        cv2.imshow("Data", self.myCanvas)
        if wait_for_key:
            cv2.waitKey()
        else:
            cv2.waitKey(DELAY_MS)
