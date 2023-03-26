import pygame
import random
import math

SQ_SIZE = 22
N_MAP_SQ_X = 100
N_MAP_SQ_Y = 300

MAP_WIDTH = N_MAP_SQ_X * SQ_SIZE
MAP_HEIGHT = N_MAP_SQ_Y * SQ_SIZE

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CENTER_WIDTH = WINDOW_WIDTH / 2
CENTER_HEIGHT = WINDOW_HEIGHT / 2

WINDOW_SQ_X = WINDOW_WIDTH // SQ_SIZE
WINDOW_SQ_Y = WINDOW_HEIGHT // SQ_SIZE

PATH_WIDTH = max(13, min(22, N_MAP_SQ_X // 8))
CENTER_PATH = PATH_WIDTH // 2

BLACK = (0, 0, 0)
WHITE = (222, 222, 222)
GRAY = (132, 236, 128)
GREEN = (41, 95, 64)
BROWN = (87, 48, 13)

COLORS = [BLACK, WHITE, GRAY, GREEN, BROWN]

pygame.init()
pygame.display.set_caption("Path Mapping")

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))





def main():
    game_loop = True
    
    while game_loop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game_loop = False
        
        screen.fill(BLACK)
        
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
    