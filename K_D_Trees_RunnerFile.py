import random

from AbstractNodeFile import SplitterNode
from typing import List, Tuple, Optional

NUM_POINTS = 20
DIMENSION = 2

def main():
    global root
    print("running.")
    dataset = buildDataSet()
    print(dataset)


    root = SplitterNode(0, dataset)

def buildDataSet():
    result: List[Optional[Tuple[float, ...]]] = []
    for i in range(NUM_POINTS):
        v: List[float] = []
        for j in range(DIMENSION):
            v.append(random.randrange(0, 100))
        result.append(tuple(v))
    return result

if __name__ == "__main__":
    main()