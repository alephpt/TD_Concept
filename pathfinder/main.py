import pygame
import pygame_gui
from ui import UI

class Game(UI):
    def __init__(self, screen_size, map_sq, square_size):
        super().__init__(screen_size, map_sq, square_size)
        self.running = True
    
    def process_inputs(self):
        for e in pygame.event.get():
            self.manager.process_events(e)
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.zoomIn()
                elif e.button == 5:
                    self.zoomOut()
            elif e.type == pygame.USEREVENT:
                if e.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if e.ui_element in self.buttons:
                        self.create_new_start()
            #    if e.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            #        if e.ui_element in self.sliders:
            #             self.update_sliders()
            #             self.create_noise()

def main():
    ## LOCAL CONSTANTS ##
    SCREEN_SIZE = (1800, 1100)
    N_MAP_SQ = (150, 150)
    SQUARE_SIZE = 40
    
    ## Initialize Game and PyGame ##
    pygame.init()
    pygame.display.set_caption("Pathfinder Visualizer")

    game = Game(SCREEN_SIZE, N_MAP_SQ, SQUARE_SIZE)

    ######################
    ##  Main Game Loop  ##
    ######################
    while game.running:
        game.process_inputs()
        game.update()
    
    
## Entry Point ##
if __name__ == "__main__":
    main()