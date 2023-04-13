import pygame

class Square: 
    def __init__(self, screen, map_center_x, map_center_y, n_map_sq_x, x, y, size, color, path, fill):
        self.screen = screen
        self.index = y * n_map_sq_x + x
        self.x_center = map_center_x
        self.y_center = map_center_y
        self.x = x * size
        self.y = y * size
        self.size = size
        self.color = color
        self.path = path
        self.fill = fill
        self.entropy = 0
        self.checked = False

    def draw(self, x_origin, y_origin, zoom):
        x = (self.x - x_origin) * zoom + self.x_center
        y = (self.y - y_origin) * zoom + self.y_center
        size = self.size * zoom
        color = self.color if isinstance(self.color, tuple) else self.color.value
        pygame.draw.rect(self.screen, color, (x, y, size, size), self.fill)
        