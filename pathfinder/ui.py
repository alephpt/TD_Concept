import pygame_gui
import pygame
from camera import Camera
from color import Color

class UI(Camera):
    def __init__(self, screen_size, map_sq, square_size):
        self.surface = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager(screen_size)
        super().__init__(self.surface, screen_size, map_sq, square_size)
        # self.labels = []
        # self.values = []
        # self.sliders = []
        # self.init_sliders()
        self.buttons = []
        self.init_buttons()
    
    def init_sliders(self):
        # Scale Slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 20), (50, 20)), "Scale", self.manager, object_id="#scale_label"))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 40), (200, 20)), self.noise.scale, (0.01, 10.0), self.manager, object_id="#scale_slider"))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 20), (60, 20)), str(self.sliders[0].current_value), self.manager))
    
        # Octaves Slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 60), (65, 20)), "Octaves", self.manager, object_id="#octaves_label"))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 80), (200, 20)), self.noise.octaves, (1, 10), self.manager, object_id="#octaves_slider"))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 60), (60, 20)), str(self.sliders[1].current_value), self.manager))
        
        # Persistence Slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 100), (90, 20)), "Persistence", self.manager, object_id="#persistence_label"))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 120), (200, 20)), self.noise.persistence, (0.1, 3.0), self.manager, object_id="#persistence_slider"))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 100), (60, 20)), str(self.sliders[2].current_value), self.manager))
        
        # Lacunarity Slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 140), (85, 20)), "Lacunarity", self.manager, object_id="#lacunarity_label"))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 160), (200, 20)), self.noise.lacunarity, (0.1, 3.0), self.manager, object_id="#lacunarity_slider"))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 140), (60, 20)), str(self.sliders[3].current_value), self.manager))
    
    def init_buttons(self):
        self.buttons.append(pygame_gui.elements.UIButton(pygame.Rect((30, 30), (100, 50)), "Generate", self.manager, object_id="#generate_button"))
    
    def update_sliders(self):
        self.noise.scale = self.sliders[0].current_value
        self.values[0].set_text(str(self.noise.scale))
        
        self.noise.octaves = self.sliders[1].current_value
        self.values[1].set_text(str(self.noise.octaves))
        
        self.noise.persistence = self.sliders[2].current_value
        self.values[2].set_text(str(self.noise.persistence))
        
        self.noise.lacunarity = self.sliders[3].current_value
        self.values[3].set_text(str(self.noise.lacunarity))
        
    def update(self):
        self.surface.fill(Color.Black.value)
        
        self.manager.update(self.clock.get_time())
        self.manager.draw_ui(self.surface)

        self.update_viewport() 
        self.render()
        
        pygame.display.update()
        self.clock.tick(15)