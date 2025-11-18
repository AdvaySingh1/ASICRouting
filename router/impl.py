import heapq
from collections import deque # for path info
from .helpers import *

# TODO remember that while printing out the output, the layer needs to be incremented by one again

class grid_maze_router:
    def __init__(self, **kwargs):
        self.grid_file = kwargs['grid_file']
        self.netlist_file = kwargs['netlist_file']
        self.output_file = kwargs['output_file']
        debug_print(f"grid_maze_router getting instantaed as {__name__}")
        # parse the input files

        self.grid = []
        self.path_info = {}
        self.netlist = {}
        self.layers = 0
        self.cols = 0
        self.rows = 0
        self.visited = set()

        self._parse_input_files()

    
    def print_grid(self):
        for l in self.grid:
            for r in l:
                print(r)
            print()
    
    def print_netlist(self):
        for net, (src, dst) in self.netlist.items():
            print(f"net: {net}. Src {src}. Dst {dst}")
    
    def _parse_grid_file(self):
        with open(self.grid_file, "r") as g_f:
            cols, rows, bend_p, via_p = (g_f.readline().strip().split(" "))
            self.cols, self.rows, self.bend_p, self.via_p = int(cols), int(rows), int(bend_p), int(via_p)

            debug_print(f"Grid size: {cols} * {rows}. Bend penalty: {bend_p}. Via penalty: {via_p}")

            for curr_row, line in enumerate(g_f):
                if not curr_row % self.rows:
                    self.layers += 1
                    self.grid.append([None for _ in range(self.rows)])
                row = [int(val) for val in line.strip().split(" ")]

                if len(row) != self.cols:
                    raise("Invalid number of columns in grid")
                
                self.grid[-1][curr_row % self.rows] = row
                    
            self.print_grid()
    
    def _parse_netlist_file(self):
        with open(self.netlist_file, "r") as n_f:
            self.num_nets = int(n_f.readline().strip())
            for line in n_f:
                net, l1, c1, r1, l2, c2, r2 = (int(val) for val in line.strip().split(" "))
                self.netlist[net] = (((l1-1), c1, r1), ((l2-1), c2, r2))
                # add the sources to the visited set
                self.visited.add((l1-1, c1, r1))

        self.print_netlist()


    def _parse_input_files(self):
        self._parse_grid_file()
        self._parse_netlist_file()


    def _run_two_point_sigle_layer_no_penalties_path_calculator(self):
        # do the dijkstra's algorithm
        layer_neighbors = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for net, (src, dst) in self.netlist.items():
            visited = set()
            l, c, r = src
            print(f"----------------net: {net}")
            print(f"l: {l}. r: {r}. c: {c}")
            frontier = [(self.grid[l][r][c], (l, c, r))]
            while frontier:
                path_cost, (l, c, r) = heapq.heappop(frontier)

                # see if it's been blocked
                if (self.grid[l][r][c] == -1):
                    continue
                
                # see if it's been visited
                if ((l, c, r) in visited):
                    continue
                
                # see if it's the dst
                if ((l, c, r) == dst): 
                    debug_print(f"Found route for {net} with pathcost of {path_cost}")
                    # TODO 

                visited.add((l, c, r))

                for dx, dy in layer_neighbors:
                    nc, nr = c + dx, r + dy
                    # check range
                    if not (0 <= nc < self.cols and 0 <= nr < self.rows):
                        continue
                    n_cost = self.grid[l][nr][nc]

                    # if not an obstacle
                    if (n_cost > 0):
                        heapq.heappush(frontier, (n_cost + path_cost, (l, nc, nr)))

            
            print("Done searching for the results")


    def _backtrace(self, net, path_info, pos):
        self.path_info[net] = deque()
        l, c, r = pos
        while ((l, c, r) in path_info):
            self.path_info[net].appendleft((l, c, r))
            if (l, c, r) in path_info:
                # not the src yet
                dir = path_info[(l, c, r)]
                if dir == 'N':
                    r -= 1
                elif dir == 'S':
                    r += 1
                elif dir == 'E':
                    c += 1
                elif dir == 'W':
                    c -= 1
                elif dir == 'U':
                    l += 1
                    # indicate a via
                    self.path_info[net].appendleft((2, c, r)) # 1 is added while printing
                else:
                    # indicate a via
                    self.path_info[net].appendleft((2, c, r))
                    l -= 1
        # append the src
        self.path_info[net].appendleft((l, c, r))

    
    def _clean_up(self, net):
        for l, c, r in self.path_info[net]:
            self.visited.add((l, c, r))
                
    
    def _print_paths(self, to_output_file=False):
        if (to_output_file):
            with open(self.output_file, "w") as o_f:
                for net in range (1, self.num_nets+1):
                    print(f"{net}", file=o_f)
                    for l, c, r in self.path_info[net]:
                        print(f"{l+1} {c} {r}", file=o_f)
                    print("0", file=o_f)
        else:
            for net in range (1, self.num_nets+1):
                # TODO remove this first line
                if net not in self.path_info: continue
                print(f"{net}")
                for l, c, r in self.path_info[net]:
                    print(f"{l+1} {c} {r}")
                print("0")


    def _run_two_point_sigle_layer_no_penalties_with_path_info(self):
        # do the dijkstra's algorithm
        # now this stores the dir we came from
        layer_neighbors = (((1, 0), 'W'), ((-1, 0), 'E'), ((0, 1), 'N'), ((0, -1), 'S'))
        self.paths = {}
        for net, (src, dst) in self.netlist.items():
            visited = self.visited.copy()
            path_info = {}
            l, c, r = src
            print(f"----------------net: {net}")
            print(f"l: {l}. r: {r}. c: {c}")
            frontier = [(self.grid[l][r][c], (l, c, r))]
            while frontier:
                path_cost, (l, c, r) = heapq.heappop(frontier)

                # see if it's been blocked
                if (self.grid[l][r][c] == -1):
                    continue
                
                # see if it's the dst
                if ((l, c, r) == dst): 
                    debug_print(f"Found route for {net} with pathcost of {path_cost}")

                    # TODO: need to add the path even if not reached
                    # back trace function
                    print("-----Printing path info-------")
                    print(path_info)
                    print("-----End Printing path info-------")

                    self._backtrace(net, path_info, dst)

                    # also clean up
                    self._clean_up(net)
                        

                for (dx, dy), dir in layer_neighbors:
                    nc, nr = c + dx, r + dy
                    # check range
                    if not (0 <= nc < self.cols and 0 <= nr < self.rows):
                        continue
                    # see if it's been visited
                    if ((l, nc, nr) in visited):
                        continue

                    n_cost = self.grid[l][nr][nc]
                    path_info[(l, nc, nr)] = dir
                    visited.add((l, nc, nr))

                    # if not an obstacle
                    if (n_cost > 0):
                        heapq.heappush(frontier, (n_cost + path_cost, (l, nc, nr)))

        print("Done searching for the results")
        self._print_paths()


    
    def _run_two_point_multi_layer_no_penalties_with_path_info(self):
        # do the dijkstra's algorithm
        # now this stores the dir we came from
        layer_neighbors = (((1, 0), 'W'), ((-1, 0), 'E'), ((0, 1), 'N'), ((0, -1), 'S'))


        layer_neighbors = (
            ((-1, 0, 0), 'U'),
            ((1, 0, 0), 'D'),
            ((0, 1, 0), 'W'),
            ((0, -1, 0), 'E'),
            ((0, 0, 1), 'N'), 
            ((0, 0, -1), 'S'))


        self.paths = {}
        for net, (src, dst) in self.netlist.items():
            visited = self.visited.copy()
            path_info = {}
            l, c, r = src
            print(f"----------------net: {net}")
            print(f"l: {l}. r: {r}. c: {c}")
            print(visited)
            frontier = [(self.grid[l][r][c], (l, c, r))]
            while frontier:
                path_cost, (l, c, r) = heapq.heappop(frontier)

                if (net == 3):
                    print((l, c, r))

                # see if it's been blocked
                if (self.grid[l][r][c] == -1):
                    continue

                
                # see if it's the dst
                if ((l, c, r) == dst): 
                    debug_print(f"Found route for {net} with pathcost of {path_cost}")

                    # TODO: need to add the path even if not reached
                    # back trace function
                    print("-----Printing path info-------")
                    print(path_info)
                    print("-----End Printing path info-------")

                    self._backtrace(net, path_info, dst)

                    # also clean up
                    self._clean_up(net)
                        

                for (dl, dx, dy), dir in layer_neighbors:
                    nl, nc, nr = l + dl, c + dx, r + dy
                    # check range
                    if not (0 <= nl < self.layers and 0 <= nc < self.cols and 0 <= nr < self.rows):
                        continue
                    # see if it's been visited
                    if ((nl, nc, nr) in visited):
                        continue
                    

                    n_cost = self.grid[nl][nr][nc]
                    # if not an obstacle
                    if (n_cost > 0):
                        if nl:
                            n_cost += self.via_p
                        path_info[(nl, nc, nr)] = dir
                        visited.add((nl, nc, nr))
                        heapq.heappush(frontier, (n_cost + path_cost, (nl, nc, nr)))

        print("Done searching for the results")
        self._print_paths()




        
    def run(self):
        # self._run_two_point_sigle_layer_no_penalties_path_calculator()
        # self._run_two_point_sigle_layer_no_penalties_with_path_info()
        self._run_two_point_multi_layer_no_penalties_with_path_info()

                

            
        

    


                