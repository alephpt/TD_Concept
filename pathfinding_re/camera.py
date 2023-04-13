import pygame

class Mouse:
    def __init__(self):
        self.prev_x = 0
        self.prev_y = 0
    
    def update(self, location):
        self.prev_x = location[0]
        self.prev_y = location[1]

class Camera:
    def __init__(self, map_size, window_size):
        self.map_width = map_size[0]
        self.map_height = map_size[1]
        self.x = self.map_width / 2
        self.y = self.map_height / 2
        self.window_width = window_size[0]
        self.window_height = window_size[1]
        self.center_window_x = self.window_width // 2        
        self.center_window_y = self.window_height // 2
        self.zoom = 1
        self.max_zoom = 2.5
        self.mouse = Mouse()
        
    def move(self, current_mouse_x, current_mouse_y):
        dx = current_mouse_x - self.mouse.prev_x
        dy = current_mouse_y - self.mouse.prev_y
        
        new_x = self.x - dx
        new_y = self.y - dy
        
        window_x_scaled = self.center_window_x * self.zoom
        window_y_scaled = self.center_window_y * self.zoom
        
        if window_x_scaled < new_x < self.map_width - window_x_scaled:
            self.x = new_x
        if window_y_scaled < new_y < self.map_height - window_y_scaled:
            self.y = new_y

    def zoomIn(self):
        pass
    
    def zoomOut(self):
        pass
    
    def minZoom(self):
        pass
    
    def maxZoom(self):
        pass
    
    def update(self):
        curr_mouse_x, curr_mouse_y = pygame.mouse.get_pos()
        
        if pygame.mouse.get_pressed()[1]:
            self.move(curr_mouse_x, curr_mouse_y)

        self.mouse.update((curr_mouse_x, curr_mouse_y))