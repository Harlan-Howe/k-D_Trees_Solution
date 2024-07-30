import csv
from typing import Dict, Tuple

from SplitterNodeFile import SplitterNode


def main():
    print("Weather Runner")

    data_from_file = load_data("Weather Data 2014-2024.tsv")
    print(f"Loaded {len(data_from_file)} days.")

    root = SplitterNode(0)
    root.build_subtree(set(data_from_file.keys()))

    # print(root)
    while True:
        search_value = request_weather_day()
        print(f"You're looking for {search_value=}")

        closest, distance = root.find_nearest(search_value, None, float('inf'))

        if closest is None:
            print("There was a problem... Search says none.")
        else:
            print(f"{closest=}\t{distance=}\nDescription: {data_from_file[closest]}")

def load_data(filename: str) -> Dict[Tuple[float, float, float, float], str]:
    """
    read the data from the tsv (tab-separated values) file and load it into a dictionary in the format:
    (precipitation, max_temp, min_temp, day_of_year) --> Description
    :param filename: the name of the file to open
    :return: the dictionary of information found in that file.
    """
    result = {}
    tsv_file = open(filename)
    read_tsv = csv.reader(tsv_file, delimiter="\t")  # note: you'll need to import "csv.py" package.

    for day in read_tsv:   # going line-by-line through file.
        try:
            datum = (float(day[0]), float(day[1]), float(day[2]), float(day[3]))
            description = day[4]
            result[datum] = description
        except ValueError:
            print(f"skipping line: {day}.")  # this will happen for the column headers line, for instance.
    return result

def request_weather_day() -> Tuple[float, float, float, float]:
    print("Please enter information about a day's weather:")
    precip = input("How much precipitation, in inches? ")
    max = input("Max temperature (°F)? ")
    min = input("Min temperature (°F)? ")
    day = input("Day of year (0-366)? ")
    return (float(precip), float(max), float(min), float(day))

if __name__ == "__main__":
    main()