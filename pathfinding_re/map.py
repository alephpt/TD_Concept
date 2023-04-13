from square import Square
from path import Pathfinder
from color import Color


class Map(Pathfinder):
    def __init__(self, screen: any, screen_size: tuple([int, int]), n_map_sq: tuple([int, int]), sq_size: int):
        super().__init__()
        self.screen = screen
        self.screen_x = screen_size[0]
        self.screen_y = screen_size[1]
        self.n_sq_x = n_map_sq[0]
        self.n_sq_y = n_map_sq[1]
        self.sq_size = sq_size
        self.squares = []
        self.create_map()
    
    def populate_blank_map(self):
        for x in range(self.n_sq_x):
            for y in range(self.n_sq_y):
                self.squares.append(Square(self.screen, (self.screen_x // 2, self.screen_y // 2), (x, y), self.sq_size, Color.Gray, 1))
    
    def create_map(self):
        # Populate Array of Blank Squares
        self.populate_blank_map()
        # Generate Noise
        # Plot Start and End Points
        return
    
    def update(self):
        self.find_path()
        
    def draw(self, camera):
        for square in self.squares:
            ## TODO: Only draw squares that are in the camera's view
            square.draw(camera[0], camera[1])