import pygame
import random
import math
from ui import UI
from color import Color

class Game(UI):
    def __init__(self, screen, screen_size, map_sq, square_size):
        super().__init__(screen, screen_size, map_sq, square_size)
        self.running = True
    

def main():
    ## LOCAL CONSTANTS ##
    SQUARE_SIZE = 40
    N_MAP_SQ = (100, 100)
    
    SCREEN_SIZE = (1800, 1100)
    N_SCREEN_SQ = (math.ceil(SCREEN_SIZE[0] / SQUARE_SIZE), math.ceil(SCREEN_SIZE[1] / SQUARE_SIZE))
    
    ## Initialize Game and PyGame ##
    pygame.init()
    pygame.display.set_caption("Pathfinder Visualizer")
    surface = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    game = Game(surface, SCREEN_SIZE, N_MAP_SQ, SQUARE_SIZE)

    ######################
    ##  Main Game Loop  ##
    ######################
    while game.running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                game.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    game.zoomIn()
                elif e.button == 5:
                    game.zoomOut()
        
        surface.fill(Color.Black.value)
        
        game.update()
        
        pygame.display.update()
        clock.tick(15)
    
    
    ## Entry Point ##
if __name__ == "__main__":
    main()