import pygame
import random
import math
from ui import UI
from color import Color

class Game(UI):
    def __init__(self, screen, screen_size, map_sq, map_size):
        super().__init__(screen, screen_size, map_sq, map_size)
        self.running = True
    

def main():
    ## LOCAL CONSTANTS ##
    SQUARE_SIZE = 40
    N_MAP_SQ = (100, 100)
    MAP_SIZE = (N_MAP_SQ[0] * SQUARE_SIZE, N_MAP_SQ[1] * SQUARE_SIZE)
    
    SCREEN_SIZE = (1800, 1100)
    SCREEN_CENTER = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
    N_SCREEN_SQ = (math.ceil(SCREEN_SIZE[0] / SQUARE_SIZE), math.ceil(SCREEN_SIZE[1] / SQUARE_SIZE))
    
    ## Initialize Game and PyGame ##
    pygame.init()
    pygame.display.set_caption("Pathfinder Visualizer")
    surface = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    game = Game(surface, SCREEN_SIZE, N_MAP_SQ, MAP_SIZE)

    ######################
    ##  Main Game Loop  ##
    ######################
    while game.running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                game.running = False
            # elif e.type == pygame.MOUSEBUTTONDOWN:
            #     if e.button == 1:
            #         game.mouse.update_position(e.pos)
        
        surface.fill(Color.Black.value)
        
        game.update()
        
        pygame.display.update()
        clock.tick(15)
    
    
    ## Entry Point ##
if __name__ == "__main__":
    main()