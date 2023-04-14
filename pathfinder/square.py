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
    def draw(self, camera_props = (1, (0, 0))):
        zoom = camera_props[0]
        origin_x, origin_y = camera_props[1]
        
        size = self.size
        x = self.x
        y = self.y
        
        draw.rect(self.screen, self.color, (x, y, size, size), self.outline)