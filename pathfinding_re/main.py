import pygame
import pygame_gui
import random
import math
from color import Color
from map import Map
from camera import Camera

class Game:
    def __init__(self, screen: pygame.Surface, screen_size: tuple([int, int]), n_map_sq: tuple([int, int]), sq_size: int):
        self.running = True
        self.map = Map(screen, screen_size, n_map_sq, sq_size)
        self.camera = Camera((n_map_sq[0] * sq_size, n_map_sq[1] * sq_size), screen_size)

    def update(self):
        self.map.update()
        self.camera.update()


def main():
    ## Constants ##
    SQ_SIZE = 40
    N_MAP_SQ_X = 100
    N_MAP_SQ_Y = 100
    MAP_WIDTH = N_MAP_SQ_X * SQ_SIZE
    MAP_HEIGHT = N_MAP_SQ_Y * SQ_SIZE

    SCREEN_WIDTH = 1800
    SCREEN_HEIGHT = 1200
    SCREEN_CENTER_X = SCREEN_WIDTH // 2
    SCREEN_CENTER_Y = SCREEN_HEIGHT // 2
    N_SCREEN_SQ_X = math.ceil(SCREEN_WIDTH / SQ_SIZE)
    N_SCREEN_SQ_Y = math.ceil(SCREEN_HEIGHT / SQ_SIZE)
    
    ## Initialize PyGame ##
    pygame.init()
    pygame.display.set_caption("Pathfinding Visualizer")
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    ## Instantiate Game ##
    game = Game(surface, (SCREEN_WIDTH, SCREEN_HEIGHT), (N_MAP_SQ_X, N_MAP_SQ_Y), SQ_SIZE)
    
    ## Main Game Loop ##
    while game.running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                game.running = False
            # if e.type == pygame.USEREVENT:
            #     if e.user_type == pygame_gui.UI_BUTTON_PRESSED:
            #         if e.ui_element == button:
            #             print("Hello World")
    
        surface.fill(Color.Brown.value)
        
        game.update()
        game.map.draw((game.camera.zoom, (game.camera.x, game.camera.y)))
        
        pygame.display.update()
        clock.tick(15)
    

## Entry Point ##
if __name__ == "__main__":
    main()