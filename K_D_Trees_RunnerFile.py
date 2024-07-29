import random
import logging
from KinkaidDecorators import log_start_stop_method

from SplitterNodeFile import SplitterNode
from typing import Set, List, Tuple, Optional

from TwoDVisualizerFile import TwoDVisualizer

NUM_POINTS = 30
DIMENSION = 2
USE_VISUALIZER_IF_POSSIBLE = True

logging.basicConfig(level=logging.INFO) # simple version to the output console

@log_start_stop_method
def main():
    global root
    print("running.")
    dataset = build_dataset()
    print(dataset)
    root = SplitterNode(0)
    visualizer = None

    if USE_VISUALIZER_IF_POSSIBLE and DIMENSION == 2:
        visualizer = TwoDVisualizer(data=dataset)
        visualizer.set_root(root)
        root.build_subtree(dataset, visualizer)
        print(root)
        visualizer.display(wait_for_key=False)
    else:
        root.build_subtree(dataset)
        print(root)

    while True:
        print(f"Please give me {DIMENSION} numbers from 0-100, separated by spaces. ", end="")
        response_string = input()
        response_vals = response_string.split(" ")
        if len(response_vals) != DIMENSION:
            print("That was the wrong number of numbers.")
            continue
        result_list = []
        for val in response_vals:
            try:
                v = float(val)
                if 0 <= v <= 100:
                    result_list.append(v)
                else:
                    print(f"{v} was out of bounds.")
            except:
                print(f"'{val}' is not a number.")
        if len(result_list) == DIMENSION:
            target = tuple(result_list)
            break
        else:
            print("Try again.")

    closest, distance = root.find_nearest(target, None, float('inf'), visualizer)

    if visualizer is not None:
        visualizer.show_search_progress(target=target, best_point=closest, wait_for_key=True)
    print(f"The closest point to {target} is {closest}.")


def build_dataset() -> Set[Tuple[float, ...]]:
    """
    creates a set of NUM_POINTS Tuples of DIMENSION numbers from 0-100.
    :return: a set of NUM_POINTS Tuples, each of DIMENSION floats.
    """
    result = set(())
    for i in range(NUM_POINTS):
        while True:
            v: List[float] = []
            for j in range(DIMENSION):
                v.append(random.randrange(0, 100))
            pt = tuple(v)
            if pt in result:
                print("Duplicate.")
            else:
                result.add(tuple(v))
                break
    return result


if __name__ == "__main__":
    main()