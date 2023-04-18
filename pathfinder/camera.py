    # TODO: Only draw squares within the screen size, based on the camera position
from pygame import mouse
from map import Map

class Mouse:
    def __init__(self):
        self.prev_pos = (0, 0)
        
    def update_position(self, pos):
        self.prev_pos = pos

class Camera(Map):
    def __init__(self, screen, screen_size, map_sq, square_size):
        super().__init__(screen, screen_size, map_sq, square_size)
        self.mouse = Mouse()
        self.max_zoom = 2.5
    
    def move(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        # calculate the difference between the current mouse position and the previous mouse position
        dx = (mouse_x - self.mouse.prev_pos[0]) / self.zoom
        dy = (mouse_y - self.mouse.prev_pos[1]) / self.zoom
        
        # calculate the new x and y location and scale the window size by the zoom
        new_x = self.camera_pos[0] - dx
        new_y = self.camera_pos[1] - dy
        window_x_scaled = self.screen_center_x / self.zoom // 1.5
        window_y_scaled = self.screen_center_y / self.zoom // 1.5

        # check if the new x and y location are within the map boundaries
        if 0 < new_x - window_x_scaled and new_x + window_x_scaled < self.map_width:
            self.camera_pos = (new_x, self.camera_pos[1])
        if 0 < new_y - window_y_scaled and new_y + window_y_scaled < self.map_height:
            self.camera_pos = (self.camera_pos[0], new_y)

    def zoomIn(self):
        new_zoom = self.zoom * 1.1
        self.zoom = min(self.max_zoom, new_zoom)

    def minZoom(self):
        dx = min(self.camera_pos[0] - self.screen_center_x, self.map_width - self.camera_pos[0] - self.screen_center_x)
        dy = min(self.camera_pos[1] - self.screen_center_y, self.map_height - self.camera_pos[1] - self.screen_center_y)

        min_x_zoom = self.screen_width / (dx + self.screen_width)
        min_y_zoom = self.screen_height / (dy + self.screen_height)

        return max(min_x_zoom, min_y_zoom) / 3

    def zoomOut(self):
        new_zoom = self.zoom / 1.1
        min_zoom = self.minZoom()
        self.zoom = max(min_zoom, new_zoom)

    def update_viewport(self):
        current_mouse_pos = mouse.get_pos()
        if mouse.get_pressed()[1]:
            # TODO: Update the location based on the zoom level 
            #       if we are at the edge of the map - zoom to a location
            # TODO: Update Zoom and Location simultaneously
            self.move(current_mouse_pos)
        self.mouse.update_position(current_mouse_pos)
    
    def render(self):
        self.draw()
