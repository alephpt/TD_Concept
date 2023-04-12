import pygame

class Square: 
    def __init__(self, screen, map_center_x, map_center_y, x, y, size, color, path, fill):
        self.screen = screen
        self.x_center = map_center_x
        self.y_center = map_center_y
        self.x = x * size
        self.y = y * size
        self.size = size
        self.color = color
        self.fill = fill
        self.path = path

    def draw(self, x_origin, y_origin, zoom):
        x = (self.x - x_origin) * zoom + self.x_center
        y = (self.y - y_origin) * zoom + self.y_center
        size = self.size * zoom
        pygame.draw.rect(self.screen, self.color.value, (x, y, size, size), self.fill)