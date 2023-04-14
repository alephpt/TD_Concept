    # TODO: Only draw squares within the screen size, based on the camera position
from pygame import mouse
from map import Map

class Mouse:
    def __init__(self):
        self.prev_pos = (0, 0)
        
    def update_position(self, pos):
        self.prev_pos = pos

class Camera(Map):
    def __init__(self, screen, screen_size, map_sq, map_size):
        super().__init__(screen, screen_size, map_sq)
        self.mouse = Mouse()
        self.camera_pos = (0, 0)
        self.map_size = map_size
        self.zoom = 1
        self.max_zoom = 2.5
    
    def move(self, current_mouse_pos):
        dx = (current_mouse_pos[0] - self.mouse.prev_pos[0]) / self.zoom
        dy = (current_mouse_pos[1] - self.mouse.prev_pos[1]) / self.zoom
    
        new_x = self.camera_pos[0] - dx
        new_y = self.camera_pos[1] - dy
        
        scaled_center_x = self.screen_size[0] / self.zoom
        scaled_center_y = self.screen_size[1] / self.zoom
        
        if scaled_center_x < new_x < self.map_size[0] - scaled_center_x:
            self.camera_pos = (new_x, self.camera_pos[1])
        if scaled_center_y < new_y < self.map_size[1] - scaled_center_y:
            self.camera_pos = (self.camera_pos[0], new_y)
    
    def update_camera(self):
        current_mouse_pos = mouse.get_pos()
        print(self.mouse.prev_pos, current_mouse_pos)
        self.move(current_mouse_pos)
        
        self.mouse.update_position(current_mouse_pos)
    
    def zoomIn(self):
        pass
    
    def zoomOut(self):
        pass
        
    def maxZoom(self):
        pass
    
    def minZoom(self):
        pass
    
    def render(self):
        self.draw()
