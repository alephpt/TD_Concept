from pygame import draw

class Square:
    def __init__(self, index, location, size, color, outline, path=False):
        self.index = index
        self.x = location[0] * size
        self.y = location[1] * size
        self.size = size
        self.outline = outline
        self.path = path
        self.set_color(color)
    
    def set_color(self, color):
        self.color = color if isinstance(color, tuple) else color.value
    
    # TODO: delete initialization of camera_props
    def draw(self, screen, screen_size, zoom, camera_pos):
        screen_center_x = screen_size[0] / 2
        screen_center_y = screen_size[1] / 2
        origin_x, origin_y = camera_pos
        
        size = self.size * zoom
        x = (self.x - origin_x) * zoom + screen_center_x 
        y = (self.y - origin_y) * zoom + screen_center_y
        
        draw.rect(screen, self.color, (x, y, size, size), self.outline)