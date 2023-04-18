# TODO: if an end point is in an unreachable area:
# remove the point, collapse the area, and find a new endpoint

import random

class PathFinder:
    def __init__(self, map_sq):
        self.n_map_sq_x = map_sq[0]
        self.n_map_sq_y = map_sq[1]
        self.start_quadrant = None
        self.start_bounds = None    # (min_x, max_x), (min_y, max_y)
        self.start_loc = None
        self.start_index = 0
        self.end_quadrant = None
        self.end_bounds = None
        self.end_loc = None
        self.end_index = 0
        self.squares = []
    
    def find_path(self, bounds):
        (start_x, end_x), (start_y, end_y) = bounds
        index_x = random.randint(start_x, end_x - 1)
        index_y = random.randint(start_y, end_y - 1)
        index = self.pos_to_index(index_y, index_x)
        
        while not self.squares[index].path:
            index_x = random.randint(start_x, end_x - 1)
            index_y = random.randint(start_y, end_y - 1)
            index = self.pos_to_index(index_y, index_x)

        return index, (index_x, index_y)
    
    def find_start_point(self):
        index, index_xy = self.find_path(self.start_bounds)
        self.start_loc = index_xy
        self.start_index = index
        
    def find_end_point(self):
        index, index_xy = self.find_path(self.end_bounds)
        self.end_loc = index_xy
        self.end_index = index
        
    def index_to_pos(self, index):
        return (index % self.n_map_sq_x, index // self.n_map_sq_x)
    
    def pos_to_index(self, y, x):
        return y * self.n_map_sq_x + x