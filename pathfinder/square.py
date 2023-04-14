from pygame import draw

class Square:
    def __init__(self, screen, screen_size, index, location, size, color, outline):
        self.screen = screen
        self.screen_center_x = screen_size[0] / 2
        self.screen_center_y = screen_size[1] / 2
        self.index = index
        self.x = location[0] * size
        self.y = location[1] * size
        self.size = size
        self.outline = outline
        self.set_color(color)
    
    def set_color(self, color):
        self.color = color if isinstance(color, tuple) else color.value
    
    # TODO: delete initialization of camera_props
    def draw(self, zoom, camera_pos):
        origin_x, origin_y = camera_pos
        
        size = self.size * zoom
        x = (self.x - origin_x) * zoom + self.screen_center_x 
        y = (self.y - origin_y) * zoom + self.screen_center_y
        
        draw.rect(self.screen, self.color, (x, y, size, size), self.outline)