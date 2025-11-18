from .helpers import *

class grid_maze_router:
    def __init__(self, **kwargs):
        self.grid_file = kwargs['grid_file']
        self.netlist_file = kwargs['netlist_file']
        self.output_file = kwargs['output_file']
        debug_print(f"grid_maze_router getting instantaed as {__name__}")
        # parse the input files
        self.parse_input_files()

    
    def print_grid(self):
        for l in self.grid:
            for r in l:
                print(r)
            print()
    
    def print_netlist(self):
        for net, (src, dst) in self.netlist.items():
            print(f"net: {net}. Src {src}. Dst {dst}")
    
    def parse_grid_file(self):
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
    
    def parse_netlist_file(self):
        with open(self.netlist_file, "r") as n_f:
            self.num_nets = int(n_f.readline().strip())
            self.netlist = {}
            for line in n_f:
                net, l1, c1, r1, l2, c2, r2 = (int(val) for val in line.strip().split(" "))
                self.netlist[net] = ((l1, c1, r1), (l2, c2, r2))

        self.print_netlist()


    def parse_input_files(self):
        self.parse_grid_file()
        self.parse_netlist_file()


                







        """With syntax is somthing liekt his

        with f.open():
            do whatever
        otherwrise
        
        try:
            f.open
            do whatever
        catch
        
        
        """