import math
import random

import cv2
import numpy as np
from typing import List, Tuple, Optional

from AbstractNodeFile import AbstractNode
from SplitterNodeFile import SplitterNode

SCALE = 4
MARGIN = 10
DELAY_MS = 250

class TwoDVisualizer:

    def __init__(self, root: Optional[AbstractNode] = None, data: Optional[List[Tuple[float, ...]]] = None):
        self.myCanvas = None
        self.clear()
        self.rect_stack: Optional[List[Tuple[float, float, float, float]]] = None
        self._root = root
        self._data = data

    def set_root(self, root: AbstractNode):
        self._root = root

    def has_root(self) -> bool:
        return self._root is not None

    def clear(self):
        self.myCanvas = np.zeros((200*SCALE+2*MARGIN, 200*SCALE+2*MARGIN, 3), dtype=float)

    def display(self, wait_for_key: bool = False):
        self.clear()
        self.show_dots_and_divisions()

        cv2.imshow("Data", self.myCanvas)
        if wait_for_key:
            cv2.waitKey()
        else:
            cv2.waitKey(DELAY_MS)

    def show_dots_and_divisions(self):
        for d in self._data:
            cv2.circle(img=self.myCanvas, center=(int(MARGIN + 2 * SCALE * d[0]), int(MARGIN + 2 * SCALE * d[1])),
                       radius=SCALE,
                       color=(0.5, 0.5, 0.5), thickness=-1)
        self.rect_stack = [(0, 0, 100, 100)]
        self.display_subtree(self._root)

    def display_subtree(self, sub_root: Optional[AbstractNode]):
        rect = self.rect_stack.pop(-1)
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
            if axis == 0:
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
            else:
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
        self.clear()
        self.show_dots_and_divisions()
        cv2.circle(img=self.myCanvas,
                   center=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                   radius=SCALE,
                   color=(0, 1.0, 0),
                   thickness=-1)


        if best_point is not None:
            d = math.sqrt(pow(target[0] - best_point[0], 2)+pow(target[1] - best_point[1], 2))
            cv2.circle(img=self.myCanvas,
                       center=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                       radius=int(2 * SCALE * d),
                       color=(0, 1.0, 0),
                       thickness=1)
            cv2.line(img=self.myCanvas,
                     pt1=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                     pt2=(int(MARGIN + 2 * SCALE * best_point[0]), int(MARGIN + 2 * SCALE * best_point[1])),
                     color=(0, 1.0, 0),
                     thickness=1)


        if threshold > -1:
            edge_pt = [target[0], target[1]]
            edge_pt[axis] = threshold
            cv2.line(img=self.myCanvas,
                     pt1=(int(MARGIN + 2 * SCALE * target[0]), int(MARGIN + 2 * SCALE * target[1])),
                     pt2=(int(MARGIN + 2 * SCALE * edge_pt[0]), int(MARGIN + 2 * SCALE * edge_pt[1])),
                     color=(0, 1.0, 1.0),
                     thickness=1)
            overlay = self.myCanvas.copy()
            if axis == 1:
                cv2.line(img=overlay,
                         pt1=(MARGIN, int(MARGIN + 2 * SCALE * edge_pt[1])),
                         pt2=(int(MARGIN + 2 * SCALE * 100), int(MARGIN + 2 * SCALE * edge_pt[1])),
                         color=(0, 1.0, 0),
                         thickness=1)
            else:
                cv2.line(img=overlay,
                         pt1=(int(MARGIN + 2 * SCALE * edge_pt[0]),MARGIN),
                         pt2=(int(MARGIN + 2 * SCALE * edge_pt[0]),int(MARGIN + 2 * SCALE * 100)),
                         color=(0, 1.0, 0),
                         thickness=1)
            self.myCanvas = cv2.addWeighted(overlay, 0.3, self.myCanvas, 0.7, 0)

        cv2.imshow("Data", self.myCanvas)
        if wait_for_key:
             cv2.waitKey()
        else:
            cv2.waitKey(DELAY_MS)