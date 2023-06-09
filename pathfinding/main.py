import pygame
import pygame_gui
import math
import random
from enum import Enum
from camera import Camera
from color import Color
from square import Square
from pathfinder import Path
import noise

# Globals
SQUARE_SIZE = 40
N_MAP_SQUARES_X = 150
N_MAP_SQUARES_Y = 150
MAP_WIDTH = N_MAP_SQUARES_X * SQUARE_SIZE
MAP_HEIGHT = N_MAP_SQUARES_Y * SQUARE_SIZE

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
SCREEN_SQUARES_X = math.ceil(SCREEN_WIDTH / SQUARE_SIZE)
SCREEN_SQUARES_Y = math.ceil(SCREEN_HEIGHT / SQUARE_SIZE)

# initialize pygame
pygame.init()
pygame.display.set_caption('Path Mapping')

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
class Map:
    def __init__(self, sliders):
        self.squares = []
        self.start_index = None
        self.target_index = None
        self.generate_noise(sliders)
        self.generate_points()
        self.pathfinder = Path(N_MAP_SQUARES_X, N_MAP_SQUARES_Y, self.start_index, self.target_index, screen, CENTER_X, CENTER_Y, SQUARE_SIZE, self.squares)
        
    def blank_map(self):
        for y in range(N_MAP_SQUARES_Y):
            for x in range(N_MAP_SQUARES_X):
                self.squares.append(Square(screen, CENTER_X, CENTER_Y, N_MAP_SQUARES_X, x, y, SQUARE_SIZE, Color.Gray, True, 1))
        
    def generate_points(self):
        start_index = Path.find_path(self.squares, 0, N_MAP_SQUARES_Y // 6.75 * N_MAP_SQUARES_X)
        start = self.squares[start_index]
        start.color = Color.LightRed
        start.fill = 0
        start.path = False
        self.start_index = start_index
        
        
        # picks a random point in the bottom third of the map and makes it green
        target_index = Path.find_path(self.squares, math.ceil(N_MAP_SQUARES_Y / 1.25 * N_MAP_SQUARES_X), N_MAP_SQUARES_X * N_MAP_SQUARES_Y)
        end = self.squares[target_index]
        end.color = Color.LightGreen
        end.fill = 0
        end.path = False
        self.target_index = target_index
        

    def generate_noise(self, sliders):
        self.blank_map()
        
        base = random.randint(0, 4096)
        
        scale = sliders[0].current_value
        octaves = sliders[1].current_value
        persistence = sliders[2].current_value
        lacunarity = sliders[3].current_value
        
        for y in range(N_MAP_SQUARES_Y):
            for x in range(N_MAP_SQUARES_X):
                if noise.snoise2(x * scale * 12.75, y * scale * 15.75, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=base) > 0.175 or \
                   noise.snoise2(x * scale * 16.25, y * scale * 13, octaves=octaves * 2, persistence=persistence / 2.0, lacunarity=lacunarity, base=(base // 2)) > 0.675:
                    # create wall
                    self.squares[y * N_MAP_SQUARES_X + x] = Square(screen, CENTER_X, CENTER_Y, N_MAP_SQUARES_X, x, y, SQUARE_SIZE, Color.Brown, False, 0)
                #elif noise.snoise2(x * scale * 20, y * scale * 18, octaves=octaves, persistence=persistence, lacunarity=lacunarity * 1.6, base=(base * 2)) > 0.675:
                    # create water 
                    #self.squares[y * N_MAP_SQUARES_X + x] = Square(screen, CENTER_X, CENTER_Y, N_MAP_SQUARES_X, x, y, SQUARE_SIZE, Color.LightBlue, False, 0)
                else:
                    # create path
                    self.squares[y * N_MAP_SQUARES_X + x] = Square(screen, CENTER_X, CENTER_Y, N_MAP_SQUARES_X, x, y, SQUARE_SIZE, Color.Gray, True, 1)

    def update(self):
        self.pathfinder.find_entropic_path()


class Game:
    def __init__(self):
        self.running = True
        self.ui = UI()
        self.map = Map(self.ui.sliders)
        
    def draw(self, xloc, yloc, zoom):
        for square in self.map.squares:
            square.draw(xloc, yloc, zoom)

    def update(self):
        self.ui.update(self)
        self.map.update()


class UI:
    def __init__(self):
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.labels = []
        self.values = []
        self.sliders = []
        self.create_sliders()
        
    def create_sliders(self):
        # scale slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 20), (50, 20)), "Scale", self.manager, object_id='#scale_label'))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 40), (200, 20)), 0.1, (0.1, 1.0), self.manager, object_id='#scale_slider'))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 20), (60, 20)), str(self.sliders[0].current_value), self.manager))
        # octaves slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 60), (65, 20)), "Octaves", self.manager, object_id='#octaves_label'))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 80), (200, 20)), 1, (1, 10), self.manager, object_id='#octaves_slider'))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 60), (60, 20)), str(self.sliders[1].current_value), self.manager))
        # persistence slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 100), (90, 20)), "Persistence", self.manager, object_id='#persistence_label'))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 120), (200, 20)), 1.5, (0.1, 3.0), self.manager, object_id='#persistence_slider'))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 100), (60, 20)), str(self.sliders[2].current_value), self.manager))
        # lacunarity slider
        self.labels.append(pygame_gui.elements.UILabel(pygame.Rect((30, 140), (85, 20)), "Lacunarity", self.manager, object_id='#lacunarity_label'))
        self.sliders.append(pygame_gui.elements.UIHorizontalSlider(pygame.Rect((30, 160), (200, 20)), 2.6, (0.1, 3.0), self.manager, object_id='#lacunarity_slider'))
        self.values.append(pygame_gui.elements.UILabel(pygame.Rect((120, 140), (60, 20)), str(self.sliders[3].current_value), self.manager))
    
    def update_values(self):
        # scale slider value
        self.values[0].set_text(str(self.sliders[0].current_value))
        # octaves slider value
        self.values[1].set_text(str(self.sliders[1].current_value))
        # persistence slider value
        self.values[2].set_text(str(self.sliders[2].current_value))
        # lacunarity slider value
        self.values[3].set_text(str(self.sliders[3].current_value))
    
    def update(self, game):
        self.camera.render(game)
        #self.manager.update(clock.get_time())
        #self.manager.draw_ui(screen)

# main function
def main():
    game = Game()
    
    while game.running:
        for e in pygame.event.get():
            #game.ui.manager.process_events(e)
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                game.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    new_zoom = game.ui.camera.zoom * 1.1
                    game.ui.camera.zoom = min(game.ui.camera.max_zoom, new_zoom)
                elif e.button == 5:
                    new_zoom = game.ui.camera.zoom / 1.1
                    min_zoom = game.ui.camera.minZoom()
                    game.ui.camera.zoom = max(min_zoom, new_zoom)
            # elif e.type == pygame.USEREVENT:
            #     if e.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            #         if e.ui_element in game.ui.sliders:
            #             game.map.generate_noise(game.ui.sliders)
            #             game.ui.update_values()

        screen.fill(Color.Black.value)

        game.update()
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        game.ui.camera.prev_mouse_x = mouse_x
        game.ui.camera.prev_mouse_y = mouse_y

        pygame.display.update()
        clock.tick(30)
    

if __name__ == '__main__':
    main()