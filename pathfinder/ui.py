import pygame_gui
from camera import Camera

class UI(Camera):
    def __init__(self, screen, screen_size, map_sq, square_size):
        super().__init__(screen, screen_size, map_sq, square_size)
    
    def update(self):
        self.update_viewport()    
        self.render()