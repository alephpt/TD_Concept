import pygame
import random
import math

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200
CENTER_Y = WINDOW_HEIGHT / 2
CENTER_X = WINDOW_WIDTH / 2

MAP_SQUARES_X = 180
MAP_SQUARES_Y = 450
SQUARE_SIZE = 48

WINDOW_SQUARES_X = math.ceil(WINDOW_WIDTH / SQUARE_SIZE)
WINDOW_SQUARES_Y = math.ceil(WINDOW_HEIGHT / SQUARE_SIZE)

MAP_WIDTH = MAP_SQUARES_X * SQUARE_SIZE
MAP_HEIGHT = MAP_SQUARES_Y * SQUARE_SIZE

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GRAY = (133, 146, 158)
GREEN = (82, 190, 128)
BROWN = (175, 96, 26)

colors = [WHITE, GRAY, GREEN, BROWN]

pygame.init()
pygame.font.init()
pygame.display.set_caption("Testing Map Generation")

text = pygame.font.SysFont('Comic Sans MS', 16)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Square: 
    def __init__(self, x, y, color):
        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE
        self.size = SQUARE_SIZE
        self.color = color
        self.fill = random.randint(0, 1)

    def draw(self, x_origin, y_origin, zoom):
        x = (self.x - x_origin) * zoom + CENTER_X
        y = (self.y - y_origin) * zoom + CENTER_Y
        size = self.size * zoom
        pygame.draw.rect(screen, self.color, (x, y, size, size), self.fill)



class Grid:
    def __init__(self, color):
        self.squares = [[Square(x, y, random.choice(colors)) for x in range(MAP_SQUARES_X)] for y in range(MAP_SQUARES_Y)]

    def draw(self, origin_x, origin_y, zoom):
        visible_x = int(CENTER_X * 2 / zoom)
        visible_y = int(CENTER_Y * 2 / zoom)
        min_y = max(0, int((origin_y - visible_y // 2) // SQUARE_SIZE))
        max_y = min(MAP_SQUARES_Y, int((origin_y + visible_y // 2) // SQUARE_SIZE) + 1)
        min_x = max(0, int((origin_x - visible_x // 2) // SQUARE_SIZE))
        max_x = min(MAP_SQUARES_X, int((origin_x + visible_x // 2) // SQUARE_SIZE) + 1)

        for row in self.squares[min_y:max_y]:
            for square in row[min_x:max_x]:
                square.draw(origin_x, origin_y, zoom)


class Camera: 
    def __init__(self):
        self.x_location = MAP_WIDTH / 2
        self.y_location = MAP_HEIGHT / 2
        self.prev_mouse_x = None
        self.prev_mouse_y = None
        self.zoom = 1.0
    
    def update(self):
        if pygame.mouse.get_pressed()[1]:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.prev_mouse_x is not None and self.prev_mouse_y is not None:
                dx = mouse_x - self.prev_mouse_x
                dy = mouse_y - self.prev_mouse_y
                
                if 0 < self.x_location - dx - CENTER_X < MAP_WIDTH - 2 * CENTER_X:
                    self.x_location -= dx
            
                if 0 < self.y_location - dy - CENTER_Y < MAP_HEIGHT - 2 * CENTER_Y:
                    self.y_location -= dy

            self.prev_mouse_x = mouse_x
            self.prev_mouse_y = mouse_y
        else:
            self.prev_mouse_x = None
            self.prev_mouse_y = None

    def render(self, grid):
        grid.draw(self.x_location, self.y_location, self.zoom)


def main():
    grid = Grid(WHITE)
    camera = Camera()
    running = True
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    camera.zoom *= 1.1
                elif e.button == 5:
                    camera.zoom /= 1.1

        screen.fill(BLACK)

        camera.update()
        camera.render(grid)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()