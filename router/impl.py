import heapq
from .helpers import *

# TODO remember that while printing out the output, the layer needs to be incremented by one again

class grid_maze_router:
    def __init__(self, **kwargs):
        self.grid_file = kwargs['grid_file']
        self.netlist_file = kwargs['netlist_file']
        self.output_file = kwargs['output_file']
        debug_print(f"grid_maze_router getting instantaed as {__name__}")
        # parse the input files
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

            self.grid = []
            self.layers = 0
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
            self.netlist = {}
            for line in n_f:
                net, l1, c1, r1, l2, c2, r2 = (int(val) for val in line.strip().split(" "))
                self.netlist[net] = (((l1-1), c1, r1), ((l2-1), c2, r2))

        self.print_netlist()


    def _parse_input_files(self):
        self._parse_grid_file()
        self._parse_netlist_file()


    def _run_two_point_sigle_layer_no_penalties_path_calculator(self):
        # do the dijkstra's algorithm
        layer_neighbors = ((1, 0), (-1, 0), (0, 1), (0, -1))
        # for net, ((l1, c1, r1), (l2, c2, r2)) in self.netlist.items():
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
                    raise("Encountered a blocked gate. Likely the source")
                
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

        
    def run(self):
        self._run_two_point_sigle_layer_no_penalties_path_calculator()
                

            
        

    


                