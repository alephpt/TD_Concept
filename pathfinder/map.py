import noise, random, math
from path import PathFinder
from square import Square
from color import Color

class Noise:
    def __init__(self):
        self.scale = 0.06
        self.octaves = 2
        self.persistence = 1.5
        self.lacunarity = 2.6

class Map(PathFinder):
    def __init__(self, screen, screen_size, map_sq, square_size):
        super().__init__(map_sq, square_size)
        self.zoom = 0.25
        self.map_width = (map_sq[0] * square_size)
        self.map_height = (map_sq[1] * square_size)
        self.camera_pos = (self.map_width / 2, self.map_height / 2)
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
                self.squares.append(Square(index, (x, y), self.square_size, Color.Gray, 1, True))
    
    # Generate noise and convert a sequence of squares to mountains or water
    def create_noise(self):
        base = random.randint(0, 4096)
        
        for y in range(self.n_map_sq_y):
            for x in range(self.n_map_sq_x):
                index = y * self.n_map_sq_x + x
                if noise.pnoise2(x * self.noise.scale / 3.0, y * self.noise.scale / 3.0, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base) > 0.275:
                    self.squares[index] = Square(index, (x, y), self.square_size, Color.Blue, 0)
                elif noise.snoise2(x * self.noise.scale / 2.0, y * self.noise.scale, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base) > 0.215 or \
                   noise.snoise2(x * self.noise.scale * 2, y * self.noise.scale, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base + 1) > 0.515 or \
                   noise.snoise2(x * self.noise.scale * 2, y * self.noise.scale * 4, self.noise.octaves, self.noise.persistence, self.noise.lacunarity, base * 2) > 0.595:
                    self.squares[index] = Square(index, (x, y), self.square_size, Color.Brown, 0)
                else:
                    self.squares[index] = Square(index, (x, y), self.square_size, Color.Gray, 1, True)
    
    def create_locations(self):
        self.create_end_location()
        self.create_start_location()

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
            square.draw(self.screen, self.screen_size, self.zoom, self.camera_pos)
            
    def exec_pathfinding(self):
        self.find_path()