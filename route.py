"""_summary_
    Generates the route string.

    Input: takes in an grid file (.grid),
    a netlist file (.nt) and an output file (.route)
"""

import sys
import argparse
# import router
from router import grid_maze_router



def main(args):
    if not (args.grid_file and args.netlist_file and args.output_file):
        print("Didn't specify all the args")
        exit(1)


    r = grid_maze_router(
        grid_file=args.grid_file,
        netlist_file=args.netlist_file,
        output_file=args.output_file)
    
    r.run()


if __name__ == "__main__":
    if __debug__:
        print("RUNNING IN DEBUG MODE")
    # print(__file__)
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-g","--grid_file",type=str)
    parser.add_argument("-n","--netlist_file",type=str)
    parser.add_argument("-o","--output_file",type=str)
    args = parser.parse_args()

    print(args)
    main(args)
    x = 10

def some():
    if __name__ == "route":
        print("Got called as route")

    # main(*args, **kwargs)