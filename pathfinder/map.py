# TODO: create list of possible spawn combinations
from path import PathFinder
from square import Square
from color import Color

class Map(PathFinder):
    def __init__(self, screen, screen_size, map_sq):
        super().__init__(map_sq)
        
        self.screen = screen
        self.screen_size = screen_size
        self.create_map()
    
    def init_map(self):
        for y in range(self.n_map_sq_y):
            for x in range(self.n_map_sq_x):
                index = y * self.n_map_sq_x + x
                self.squares.append(Square(self.screen, self.screen_size, index, (x, y), 40, Color.Gray, 1))
    
    def create_map(self):
        # Populate the list of map squares with black squares
        self.init_map()
        # Generate noise and convert squares to 'mountains' or 'water'
        # Generate spawn and end points
            # TODO: Can we extrapolate end point quality check on creation?
    
    def draw(self):
        for square in self.squares:
            square.draw()
            