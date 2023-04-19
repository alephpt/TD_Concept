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
        self.walking = False
        self.mapped = False
        self.current_distance = 0
        self.mapping_squares = []
        self.squares = []
       
    ############################
    #    UTILITY FUNCTIONS     #
    ############################
       
    def index_to_pos(self, index):
        return (index % self.n_map_sq_x, index // self.n_map_sq_x)
    
    def pos_to_index(self, y, x):
        return y * self.n_map_sq_x + x  
          
    def find_available_path(self, bounds):
        (start_x, end_x), (start_y, end_y) = bounds
        index_x = random.randint(start_x, end_x - 1)
        index_y = random.randint(start_y, end_y - 1)
        index = self.pos_to_index(index_y, index_x)
        
        while not self.squares[index].path:
            index_x = random.randint(start_x, end_x - 1)
            index_y = random.randint(start_y, end_y - 1)
            index = self.pos_to_index(index_y, index_x)

        return index, (index_x, index_y) 
        
    def index_in_path(self, index):
        return self.squares[index].path
    
    def index_is_mapped(self, index):
        return self.squares[index].mapped
    
    def index_is_walked(self, index):
        return self.squares[index].walked
      
    def xy_in_bounds(self, x, y):
        return 0 <= x < self.n_map_sq_x and 0 <= y < self.n_map_sq_y

    ############################
    # ENDPOINT SPAWN FUNCTIONS #
    ############################  
       
    def create_start_location(self):
        # Get a random quadrant for the start region, and get the bounds of that quadrant
        self.start_quadrant = self.end_quadrant.get_starting_quadrant()
        self.start_bounds = self.start_quadrant.get_start_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        # get and set a random index, (x, y) value for a given start point
        self.start_index, self.start_loc = self.find_available_path(self.start_bounds)
        # update the squares list with the new start points        
        self.squares[self.start_index] = Square(self.start_index, self.start_loc, self.square_size, Color.Green, 0)
        self.squares[self.start_index].walked = True
        self.squares[self.start_index].mapped = True
    
    def create_new_start(self):
        self.start_quadrant = random.choice([q for q in Quadrant if q != self.end_quadrant])
        self.start_bounds = self.start_quadrant.get_start_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        # TODO: We want to append to start list, not replace
        self.start_index, self.start_loc = self.find_available_path(self.start_bounds)
        self.squares[self.start_index] = Square(self.start_index, self.start_loc, self.square_size, Color.Green, 0)
        self.squares[self.start_index].walked = True
        self.squares[self.start_index].mapped = True
    
    def create_end_location(self):
        # Get random quadrant for the end region, and get the bounds of that quadrant
        self.end_quadrant = Quadrant.get_random_quadrant()
        self.end_bounds = self.end_quadrant.get_end_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        # get and set a random index, (x, y) value for a given end point
        self.end_index, self.end_loc = self.find_available_path(self.end_bounds)
        # update the squares list with the new end points
        self.squares[self.end_index] = Square(self.end_index, self.end_loc, self.square_size, Color.Red, 0)
        self.squares[self.start_index].walked = True
        self.squares[self.start_index].mapped = True

    ############################
    #  PATHFINDING FUNCTIONS   #
    ############################  

    # TODO: Look at removing redundant path tracing
    ###   PATH FINDING FUNCTIONS   ###
    ##################################
    def find_exit(self):
        return
    
    ### DISTANCE MAPPING FUNCTIONS ###
    ##################################
    
    def check_mapped_square(self, x, y):
        return self.xy_in_bounds(x, y) and \
               self.index_in_path(self.pos_to_index(x, y)) and \
               not self.index_is_mapped(self.pos_to_index(x, y))
    
    def find_next_squares(self, index):
        # TODO: Check if we are in a dead end
        x, y = self.index_to_pos(index)
        curr_sq = []
        
        il, ib, ir, it = (x - 1, y), \
                         (x, y + 1), \
                         (x + 1, y), \
                         (x, y - 1)
        
        for idx in [il, ib, ir, it]:
            if idx in [self.start_index, self.end_index]:
                continue
            elif self.check_mapped_square(*idx):
                curr_sq.append(self.pos_to_index(*idx))
        
        return curr_sq
    
    def clean_up_mapping_squares(self):
        if len(self.mapping_squares) == 0:
            # Are We at the end?
            return
        
        for sq_idx in self.mapping_squares:
            # TODO: Interpolate between colors
            self.squares[sq_idx].set_color(Color.Gray)
            self.mapping_squares.remove(sq_idx)
    
    def endpoint_distance_map(self):
        current_iteration = self.mapping_squares.copy()
        self.clean_up_mapping_squares()
        
        for sq_idx in current_iteration:
            distance = self.squares[sq_idx].distance + 1
            next_squares = self.find_next_squares(sq_idx)
            
            if len(next_squares) == 0:
                continue
            
            for next_sq in next_squares:
                self.squares[next_sq].distance = distance
                self.squares[next_sq].outline = 0
                self.squares[next_sq].set_color(Color.Orange)
                self.squares[next_sq].mapped = True 
                
                self.mapping_squares.append(next_sq)
            
    def find_path(self):
        # If we have already found our path, we don't need to do anything
        if self.mapped and not self.walking:
            return

        # Determine if we are mapping the distances
        if not self.mapped:
            # Determine if we are starting the mapping process
            if len(self.mapping_squares) == 0:
                self.mapping_squares.append(self.end_index)
                return

            self.endpoint_distance_map()
        else: 
            self.find_exit()