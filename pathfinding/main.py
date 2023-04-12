import pygame
import math
import random
import noise
from enum import Enum
from camera import Camera
from color import Color
from square import Square

# Globals
SQUARE_SIZE = 25
N_MAP_SQUARES_X = 100
N_MAP_SQUARES_Y = 100
MAP_WIDTH = N_MAP_SQUARES_X * SQUARE_SIZE
MAP_HEIGHT = N_MAP_SQUARES_Y * SQUARE_SIZE

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
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
    def __init__(self):
        self.squares = []
        self.generate_map()
        self.generate_points()
        
    def generate_map(self):
        for y in range(N_MAP_SQUARES_Y):
            for x in range(N_MAP_SQUARES_X):
                self.squares.append(Square(screen, CENTER_X, CENTER_Y, x, y, SQUARE_SIZE, Color.Gray, True, 1))
        
    def generate_points(self):
        # picks a random point on the top third of the map and makes it red
        start = self.squares[random.randint(0, N_MAP_SQUARES_Y // 3 * N_MAP_SQUARES_X)]
        start.color = Color.LightRed
        start.fill = 0
        start.path = False
        
        # picks a random point in the bottom third of the map and makes it green
        end = self.squares[random.randint(math.ceil(N_MAP_SQUARES_Y / 1.5 * N_MAP_SQUARES_X), N_MAP_SQUARES_X * N_MAP_SQUARES_Y)]
        end.color = Color.LightGreen
        end.fill = 0
        end.path = False

    def generate_noise(self):
        base = random.randint(0, 4096)
        
        for y in range(N_MAP_SQUARES_Y):
            for x in range(N_MAP_SQUARES_X):
                if snoise2(x, y, 1, base=base) > 0.5:
                    self.squares[Square(screen, CENTER_X, CENTER_Y, x, y, SQUARE_SIZE, Color.Gray, False, 1)]


class Game:
    def __init__(self):
        self.running = True
        self.map = Map()
        
    def draw(self, xloc, yloc, zoom):
        for square in self.map.squares:
            square.draw(xloc, yloc, zoom)
    

# main function
def main():
    game = Game()
    camera = Camera(MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    while game.running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                game.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    new_zoom = camera.zoom * 1.1
                    camera.zoom = min(camera.max_zoom, new_zoom)
                elif e.button == 5:
                    new_zoom = camera.zoom / 1.1
                    min_zoom = camera.minZoom()
                    camera.zoom = max(min_zoom, new_zoom)

        screen.fill(Color.Black.value)

        camera.update()
        camera.render(game)

        pygame.display.update()
        clock.tick(60)
    

if __name__ == '__main__':
    main()