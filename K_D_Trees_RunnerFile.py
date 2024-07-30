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
    # create the dataset and empty root splitternode.
    dataset = build_dataset()
    print(dataset)
    root = SplitterNode()

    # create the visualizer (if using)
    visualizer = None
    if USE_VISUALIZER_IF_POSSIBLE and DIMENSION == 2:
        visualizer = TwoDVisualizer(data=dataset)

    # build the tree, with or without visualizer.
    if visualizer is not None:
        visualizer.set_root(root)
        root.build_subtree(dataset, visualizer)
        print(root)
        visualizer.display(wait_for_key=False)
    else:
        root.build_subtree(dataset)
        print(root)

    while True:
        # get a target value to search for
        target = ask_for_target()

        closest, distance = root.find_nearest(target,  # the point to which we want the closest point in the dataset
                                              None,  # the best point so far... we're just starting so there isn't one.
                                              float('inf'),  # the closest distance point so far... inifinity so far
                                              visualizer)

        if visualizer is not None:
            visualizer.show_search_progress(target=target, best_point=closest, wait_for_key=False)
        print(f"The closest point to {target} is {closest}.")


def ask_for_target() -> Tuple[float, ...]:
    """
    request DIMENSION numbers from 0-100 from the user, and keep asking until you get them.
    :return: a tuple consisting of DIMENSION numbers from 0-100.
    """
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
    return target


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