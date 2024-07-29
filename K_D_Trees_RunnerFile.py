import random
import logging
from KinkaidDecorators import log_start_stop_method

from SplitterNodeFile import SplitterNode
from typing import List, Tuple, Optional

from TwoDVisualizerFile import TwoDVisualizer

NUM_POINTS = 80
DIMENSION = 2

logging.basicConfig(level=logging.INFO) # simple version to the output console

@log_start_stop_method
def main():
    global root
    print("running.")
    dataset = build_dataset()
    print(dataset)
    root = SplitterNode(0)
    visualizer = None

    if DIMENSION == 2:
        visualizer = TwoDVisualizer(data=dataset)
        visualizer.set_root(root)
        root.build_subtree(dataset, visualizer)
        print(root)
        visualizer.display(wait_for_key=True)
    else:
        root.build_subtree(dataset)
        print(root)

    target = (random.randrange(0, 100), random.randrange(0, 100))
    closest, distance = root.find_nearest(target, None, float('inf'), visualizer)
    if DIMENSION == 2:
        visualizer.show_search_progress(target=target, best_point=closest, wait_for_key=True)
    print(f"The closest point to {target} is {closest}.")

def build_dataset():
    result = []
    for i in range(NUM_POINTS):
        while True:
            v: List[float] = []
            for j in range(DIMENSION):
                v.append(random.randrange(0, 100))
            pt = tuple(v)
            if pt in result:
                print("Duplicate.")
            else:
                result.append(tuple(v))
                break
    return result


if __name__ == "__main__":
    main()