import random

from SplitterNodeFile import SplitterNode
from typing import List, Tuple, Optional

from TwoDVisualizerFile import TwoDVisualizer

NUM_POINTS = 20
DIMENSION = 2


def main():
    global root
    print("running.")
    dataset = build_dataset()
    print(dataset)

    visualizer = TwoDVisualizer(data=dataset)
    root = SplitterNode(0)
    visualizer.set_root(root)
    root.build_subtree(dataset, visualizer)
    # root.build_subtree(dataset)

    print(root)

    visualizer.display(wait_for_key=True)

def build_dataset():
    result = []
    for i in range(NUM_POINTS):
        v: List[float] = []
        for j in range(DIMENSION):
            v.append(random.randrange(0, 100))
        result.append(tuple(v))
    return result


if __name__ == "__main__":
    main()