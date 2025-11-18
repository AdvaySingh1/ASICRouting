"""_summary_
    Generates the route string.

    Input: takes in an grid file (.grid),
    a netlist file (.nt) and an output file (.route)
"""

import sys
import argparse


def main(args):
    print("-- MAIN FUNCTION --")

    if not (args.grid_file and args.netlist_file and args.output_file):
        print("Didn't specify all the args")
        exit(1)

if __name__ == "__main__":
    # print(__file__)
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-g","--grid_file",type=str)
    parser.add_argument("-n","--netlist_file",type=str)
    parser.add_argument("-o","--output_file",type=str)
    args = parser.parse_args()
    main(args)
    x = 10


if __name__ == "__route__":
    print("Got called as route")

    # main(*args, **kwargs)