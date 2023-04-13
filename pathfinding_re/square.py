from color import Color
from pygame import draw

class Square:
    def __init__(self, surface, screen_center, location, size, color, outline):
        self.screen = surface
        self.index = location
        self.screen_center_x = screen_center[0]
        self.screen_center_y = screen_center[1]
        self.x = location[0] * size
        self.y = location[1] * size
        self.size = size
        self.outlined = outline
        self.distance = 0
        self.set_color(color)
        
    # To Position?
    # To Index? 
    
    def set_color(self, color):
        self.color = color if isinstance(color, tuple) else color.value
    
    def draw(self, zoom, global_loc):
        x = self.x - global_loc[0] * zoom + self.screen_center_x
        y = self.y - global_loc[1] * zoom + self.screen_center_y
        size = self.size
        
        draw.rect(self.screen, self.color, (x, y, size, size), self.outlined)