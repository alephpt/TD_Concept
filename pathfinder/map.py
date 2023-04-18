import noise, random, math
from path import PathFinder
from square import Square
from color import Color
from enum import Enum

class Noise:
    def __init__(self):
        self.scale = 0.06
        self.octaves = 2
        self.persistence = 1.5
        self.lacunarity = 2.6

# TODO: create list of possible spawn combinations TL;BR, TR;BL, BL;TR, BR;TL

## Top Left - ((0, Screen Width / 3), (0, Screen Height / 3))
## Top Right - ((Screen Width - Screen Width / 3, Screen Width), (0, Screen Height / 3))
## Bottom Left - ((0, Screen Width / 3), (Screen Height - Screen Height / 3, Screen Height))
## Bottom Right - ((Screen Width - Screen Width / 3, Screen Width), (Screen Height - Screen Height / 3, Screen Height))
class Quadrants(Enum):
    TOP_LEFT = 0
    BOTTOM_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3

    @staticmethod
    def get_random_quadrant():
        return random.choice(list(Quadrants))
    
    def get_starting_quadrant(self):
        if self == Quadrants.TOP_LEFT:
            return Quadrants.BOTTOM_RIGHT
        elif self == Quadrants.TOP_RIGHT:
            return Quadrants.BOTTOM_LEFT
        elif self == Quadrants.BOTTOM_LEFT:
            return Quadrants.TOP_RIGHT
        elif self == Quadrants.BOTTOM_RIGHT:
            return Quadrants.TOP_LEFT
    
    def get_quadrant_pos(self, map_sq_x, map_sq_y):
        if self == Quadrants.TOP_LEFT:
            return (0, map_sq_x // 3), (0, map_sq_y // 3)
        elif self == Quadrants.TOP_RIGHT:
            return (map_sq_x - map_sq_x // 3, map_sq_x), (0, map_sq_y // 3)
        elif self == Quadrants.BOTTOM_LEFT:
            return (0, map_sq_x // 3), (map_sq_y - map_sq_y // 3, map_sq_y)
        elif self == Quadrants.BOTTOM_RIGHT:
            return (map_sq_x - map_sq_x // 3, map_sq_x), (map_sq_y - map_sq_y // 3, map_sq_y)


class Map(PathFinder):
    def __init__(self, screen, screen_size, map_sq, square_size):
        super().__init__(map_sq)
        self.zoom = 0.25
        self.map_width = (map_sq[0] * square_size)
        self.map_height = (map_sq[1] * square_size)
        self.camera_pos = (self.map_width / 2, self.map_height / 2)
        self.square_size = square_size
        self.screen = screen
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.screen_center_x = screen_size[0] / 2
        self.screen_center_y = screen_size[1] / 2
        self.screen_squares = (math.ceil(screen_size[0] / square_size) * self.zoom, math.ceil(screen_size[1] / square_size) * self.zoom)
        self.noise = Noise()
        self.create_map()
    
    # Generates a grid of blank squares
    def init_map(self):
        for y in range(self.n_map_sq_y):
            for x in range(self.n_map_sq_x):
                index = y * self.n_map_sq_x + x
                self.squares.append(Square(self.screen, self.screen_size, index, (x, y), self.square_size, Color.Gray, 1, True))
    
    # Generate noise and convert a sequence of squares to mountains or water
    def create_noise(self):
        base = random.randint(0, 4096)
        
        for y in range(self.n_map_sq_y):
            for x in range(self.n_map_sq_x):
                index = y * self.n_map_sq_x + x
                if noise.pnoise2(x * self.noise.scale / 3.0, y * self.noise.scale / 3.0, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base) > 0.275:
                    self.squares[index] = Square(self.screen, self.screen_size, index, (x, y), self.square_size, Color.Blue, 0)
                elif noise.snoise2(x * self.noise.scale / 2.0, y * self.noise.scale, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base) > 0.215 or \
                   noise.snoise2(x * self.noise.scale * 2, y * self.noise.scale, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base + 1) > 0.515 or \
                   noise.snoise2(x * self.noise.scale * 2, y * self.noise.scale * 4, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base * 2) > 0.595:
                    self.squares[index] = Square(self.screen, self.screen_size, index, (x, y), self.square_size, Color.Brown, 0)
                else:
                    self.squares[index] = Square(self.screen, self.screen_size, index, (x, y), self.square_size, Color.Gray, 1, True)
    
    def create_locations(self):
        # Get random quadrant for start and end
        self.end_quadrant = Quadrants.get_random_quadrant()
        self.start_quadrant = self.end_quadrant.get_starting_quadrant()

        # get quandrant bounds
        self.start_bounds = self.start_quadrant.get_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        self.end_bounds = self.end_quadrant.get_quadrant_pos(self.n_map_sq_x, self.n_map_sq_y)
        
        # TODO: Check if end point is valid before creating start point
        # get random start and end points
        self.find_end_point()
        self.find_start_point()
        
        # draw new squares at start and end locations
        self.squares[self.start_index] = Square(self.screen, self.screen_size, self.start_index, self.start_loc, self.square_size, Color.Green, 0, )
        self.squares[self.end_index] = Square(self.screen, self.screen_size, self.end_index, self.end_loc, self.square_size, Color.Red, 0)
    
    def create_map(self):
        # Populate the list of map squares with black squares
        self.init_map()
        
        # Generate noise and convert squares to 'mountains' or 'water'
        self.create_noise()
 
        # TODO: Can we extrapolate end point quality check on creation?       
        # Generate spawn and end points
        self.create_locations()
    
    def draw(self):
        # TODO: Only draw the squares in the screen
        for square in self.squares:
            square.draw(self.zoom, self.camera_pos)