import pygame_gui
from camera import Camera

class UI(Camera):
    def __init__(self, screen, screen_size, map_sq, map_size):
        super().__init__(screen, screen_size, map_sq, map_size)
    
    def update(self):
        self.update_camera()
        self.render()