# TODO: if an end point is in an unreachable area:
# remove the point, collapse the area, and find a new endpoint

import random
from quadrants import Quadrant
from color import Color
from square import Square

class PathFinder:
    def __init__(self, map_sq, square_size):
        self.n_map_sq_x = map_sq[0]
        self.n_map_sq_y = map_sq[1]
        self.start_quadrant = None          # Quadrant enum value
        self.start_bounds = None            # ((min_x, max_x), (min_y, max_y))
        self.start_loc = None               # (x, y)
        self.start_index = 0                # int
        self.end_quadrant = None
        self.end_bounds = None
        self.end_loc = None
        self.end_index = 0
        self.square_size = square_size
        self.squares = []
    
    def find_path_location(self, bounds):
        (start_x, end_x), (start_y, end_y) = bounds
        index_x = random.randint(start_x, end_x - 1)
        index_y = random.randint(start_y, end_y - 1)
        index = self.pos_to_index(index_y, index_x)
        
        while not self.squares[index].path:
            index_x = random.randint(start_x, end_x - 1)
            index_y = random.randint(start_y, end_y - 1)
            index = self.pos_to_index(index_y, index_x)

        return index, (index_x, index_y)
       
    def create_start_location(self):
        # Get a random quadrant for the start region, and get the bounds of that quadrant
        self.start_quadrant = self.end_quadrant.get_starting_quadrant()
        self.start_bounds = self.start_quadrant.get_start_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        # get and set a random index, (x, y) value for a given start point
        self.start_index, self.start_loc = self.find_path_location(self.start_bounds)
        # update the squares list with the new start points        
        self.squares[self.start_index] = Square(self.start_index, self.start_loc, self.square_size, Color.Green, 0)
    
    # TODO: Look at removing redundant path tracing
    def create_new_start(self):
        self.start_quadrant = random.choice([q for q in Quadrant if q != self.end_quadrant])
        self.start_bounds = self.start_quadrant.get_start_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        # TODO: We want to append to start list, not replace
        self.start_index, self.start_loc = self.find_path_location(self.start_bounds)
        self.squares[self.start_index] = Square(self.start_index, self.start_loc, self.square_size, Color.Green, 0)
    
    def create_end_location(self):
        # Get random quadrant for the end region, and get the bounds of that quadrant
        self.end_quadrant = Quadrant.get_random_quadrant()
        self.end_bounds = self.end_quadrant.get_end_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        # get and set a random index, (x, y) value for a given end point
        self.end_index, self.end_loc = self.find_path_location(self.end_bounds)
        # update the squares list with the new end points
        self.squares[self.end_index] = Square(self.end_index, self.end_loc, self.square_size, Color.Red, 0)
    
    
    def index_to_pos(self, index):
        return (index % self.n_map_sq_x, index // self.n_map_sq_x)
    
    def pos_to_index(self, y, x):
        return y * self.n_map_sq_x + x