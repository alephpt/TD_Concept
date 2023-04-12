import pygame

class Camera: 
    def __init__(self, map_width, map_height, window_width, window_height):
        self.map_width = map_width
        self.map_height = map_height
        self.x_location = map_width / 2
        self.y_location = map_height / 2
        self.prev_mouse_x = None
        self.prev_mouse_y = None
        self.window_x = window_width
        self.window_y = window_height
        self.center_window_x = self.window_x // 2
        self.center_window_y = self.window_y // 2
        self.zoom = .5
        self.max_zoom = 2.75

    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.prev_mouse_x is not None and self.prev_mouse_y is not None:
            dx = mouse_x - self.prev_mouse_x
            dy = mouse_y - self.prev_mouse_y
            
            new_x = self.x_location - dx / self.zoom
            new_y = self.y_location - dy / self.zoom

            if 0 <= new_x - self.center_window_x and new_x + self.center_window_x <= self.map_width:
                self.x_location = new_x
        
            if 0 <= new_y - self.center_window_y and new_y + self.center_window_y <= self.map_height:
                self.y_location = new_y


        self.prev_mouse_x = mouse_x
        self.prev_mouse_y = mouse_y

    def update(self):
        if pygame.mouse.get_pressed()[1]:
            self.move()

    def zoomIn(self):
        new_zoom = self.zoom * 1.1
        self.zoom = min(self.max_zoom, new_zoom)

    def minZoom(self):
        dx = min(self.x_location - self.center_window_x, self.map_width - self.x_location - self.center_window_x)
        dy = min(self.y_location - self.center_window_y, self.map_height - self.y_location - self.center_window_y)

        min_x_zoom = self.window_x / (2 * dx + self.window_x)
        min_y_zoom = self.window_y / (2 * dy + self.window_y)

        return max(min_x_zoom, min_y_zoom) / 3

    def zoomOut(self):
        new_zoom = self.zoom / 1.1
        min_zoom = self.minZoom()
        self.zoom = max(min_zoom, new_zoom)

    def render(self, game):
        game.draw(self.x_location, self.y_location, self.zoom)