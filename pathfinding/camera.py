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
        self.zoom = 1
        self.max_zoom = 3.66

    def move(self, mouse_x, mouse_y):
        if self.prev_mouse_x is not None and self.prev_mouse_y is not None:
            # calculate the difference between the current mouse position and the previous mouse position
            dx = (mouse_x - self.prev_mouse_x) / self.zoom
            dy = (mouse_y - self.prev_mouse_y) / self.zoom
            
            # calculate the new x and y location and scale the window size by the zoom
            new_x = self.x_location - dx
            new_y = self.y_location - dy
            window_x_scaled = self.center_window_x / self.zoom // 1.25
            window_y_scaled = self.center_window_y / self.zoom // 1.4

            # check if the new x and y location are within the map boundaries
            if 0 < new_x - window_x_scaled and new_x + window_x_scaled < self.map_width:
                self.x_location = new_x
            if 0 < new_y - window_y_scaled and new_y + window_y_scaled < self.map_height:
                self.y_location = new_y

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[2]:
            self.move(mouse_x, mouse_y)
        
        self.prev_mouse_x = mouse_x
        self.prev_mouse_y = mouse_y

    def zoomIn(self):
        new_zoom = self.zoom * 1.1
        self.zoom = min(self.max_zoom, new_zoom)

    def minZoom(self):
        dx = min(self.x_location - self.center_window_x, self.map_width - self.x_location - self.center_window_x)
        dy = min(self.y_location - self.center_window_y, self.map_height - self.y_location - self.center_window_y)

        min_x_zoom = self.window_x / (3 * dx + self.window_x)
        min_y_zoom = self.window_y / (dy + self.window_y)

        return max(min_x_zoom, min_y_zoom) / 3

    def zoomOut(self):
        new_zoom = self.zoom / 1.1
        min_zoom = self.minZoom()
        self.zoom = max(min_zoom, new_zoom)

    def render(self, game):
        game.draw(self.x_location, self.y_location, self.zoom)
        self.update()