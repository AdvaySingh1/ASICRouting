

class grid_maze_router:
    def __init__(self, **kwargs):
        self.grid_file = kwargs['grid_file']
        self.netlist_file = kwargs['netlist_file']
        self.output_file = kwargs['output_file']
        print(f"My grid file is {self.grid_file}")


        if __name__=="router":
            print("Got called as router")

