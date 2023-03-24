from codecs import getincrementaldecoder
from importlib.resources import path
import pygame
import random
import math

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200
CENTER_Y = WINDOW_HEIGHT // 2
CENTER_X = WINDOW_WIDTH // 2

N_MAP_SQUARES_X = 180
N_MAP_SQUARES_Y = 280
SQUARE_SIZE = 48

WINDOW_SQUARES_X = math.ceil(WINDOW_WIDTH // SQUARE_SIZE)
WINDOW_SQUARES_Y = math.ceil(WINDOW_HEIGHT // SQUARE_SIZE)

MAP_WIDTH = N_MAP_SQUARES_X * SQUARE_SIZE
MAP_HEIGHT = N_MAP_SQUARES_Y * SQUARE_SIZE

PATH_WIDTH = max(10, min(20, N_MAP_SQUARES_X // 10))
HALF_PATH = PATH_WIDTH // 2
MAP_OFFSET = N_MAP_SQUARES_X // 2 - PATH_WIDTH


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GRAY = (133, 146, 158)
GREEN = (82, 190, 128)
BROWN = (175, 96, 26)

colors = [BLACK, WHITE, GRAY, GREEN, BROWN]




pygame.init()
pygame.font.init()
pygame.display.set_caption("Testing Map Generation")

text = pygame.font.SysFont('Comic Sans MS', 16)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Square: 
    def __init__(self, x, y, color, path, fill):
        self.x = x * SQUARE_SIZE
        self.y = y * SQUARE_SIZE
        self.size = SQUARE_SIZE
        self.color = color
        self.fill = fill
        self.path = path

    def draw(self, x_origin, y_origin, zoom):
        x = (self.x - x_origin) * zoom + CENTER_X
        y = (self.y - y_origin) * zoom + CENTER_Y
        size = self.size * zoom
        pygame.draw.rect(screen, self.color, (x, y, size, size), self.fill)


class Path:
    def __init__(self):
        self.x = 0
        self.width = PATH_WIDTH
        self.l_bounds = PATH_WIDTH + HALF_PATH
        self.r_bounds = N_MAP_SQUARES_X - PATH_WIDTH - HALF_PATH


class Grid:
    # Pick a starting position for 3 paths 
    # TODO: Need to make this modular based on N number of players/paths
    left_pos = random.randint(PATH_WIDTH + HALF_PATH, MAP_OFFSET - (PATH_WIDTH + HALF_PATH))
    middle_pos = random.randint(left_pos + PATH_WIDTH + HALF_PATH, N_MAP_SQUARES_X / 2 + left_pos - PATH_WIDTH)
    right_pos = random.randint(middle_pos + PATH_WIDTH + HALF_PATH, N_MAP_SQUARES_X - PATH_WIDTH - HALF_PATH)

    def __init__(self):
        self.squares = self.constructGrid(self.left_pos, self.middle_pos, self.right_pos)
        self.left_convergence = N_MAP_SQUARES_Y // random.randint(2, 4)
        self.right_convergence = N_MAP_SQUARES_Y // random.randint(2, 4)

    def updatePathLocations(self):
        l_path_deviation = random.randint(-1, 1)
        m_path_deviation = random.randint(-1, 1)
        r_path_deviation = random.randint(-1, 1)

        new_left_path = self.left_pos + l_path_deviation
        new_middle_path = self.middle_pos + m_path_deviation
        new_right_path = self.right_pos + r_path_deviation

        left_middle_mediant = (self.left_pos + self.middle_pos) / 2
        middle_right_mediant = (self.right_pos + self.middle_pos) / 2

        left_edge_bounds = PATH_WIDTH + HALF_PATH
        left_middle_bounds = left_middle_mediant - PATH_WIDTH
        middle_left_bounds = left_middle_mediant + PATH_WIDTH
        middle_right_bounds = middle_right_mediant - PATH_WIDTH
        right_middle_bounds = middle_right_mediant + PATH_WIDTH
        right_edge_bounds = N_MAP_SQUARES_X - PATH_WIDTH - HALF_PATH


        if left_edge_bounds < new_left_path < left_middle_bounds:
            self.left_pos = new_left_path
        else:
            self.left_pos -= l_path_deviation
           
        if middle_left_bounds < new_middle_path < middle_right_bounds:
            self.middle_pos = new_middle_path
        else:
            self.middle_pos -= m_path_deviation

        if right_middle_bounds < new_right_path < right_edge_bounds:
            self.right_pos = new_right_path
        else:
            self.right_pos -= m_path_deviation


    def constructGrid(self, first_x, second_x, third_x):
        grid = [[0 for _ in range(N_MAP_SQUARES_X)] for _ in range(N_MAP_SQUARES_Y)]

        for y in range(N_MAP_SQUARES_Y):
            l_path_mod_l = random.randint(-1, 1)
            l_path_mod_r = random.randint(-1, 1)
            m_path_mod_l = random.randint(-1, 1)
            m_path_mod_r = random.randint(-1, 1)
            r_path_mod_l = random.randint(-1, 1)
            r_path_mod_r = random.randint(-1, 1)

            for x in range(N_MAP_SQUARES_X):
                color = BROWN
                path = False
                fill = 0


                if self.left_pos - HALF_PATH - l_path_mod_l < x < self.left_pos + HALF_PATH + l_path_mod_r or \
                   self.middle_pos - HALF_PATH - m_path_mod_l < x < self.middle_pos + HALF_PATH + m_path_mod_r or \
                   self.right_pos - HALF_PATH - r_path_mod_l < x < self.right_pos + HALF_PATH + r_path_mod_r:
                    color = GREEN
                    path = True
                    fill = 1

                grid[y][x] = Square(x, y, color, path, fill)

            self.updatePathLocations()


        return grid


    def draw(self, origin_x, origin_y, zoom):
        visible_x = int(CENTER_X * 2 / zoom)
        visible_y = int(CENTER_Y * 2 / zoom)
        min_y = max(0, int((origin_y - visible_y // 2) // SQUARE_SIZE))
        max_y = min(N_MAP_SQUARES_Y, int((origin_y + visible_y // 2) // SQUARE_SIZE) + 1)
        min_x = max(0, int((origin_x - visible_x // 2) // SQUARE_SIZE))
        max_x = min(N_MAP_SQUARES_X, int((origin_x + visible_x // 2) // SQUARE_SIZE) + 1)

        for row in self.squares[min_y:max_y]:
            for square in row[min_x:max_x]:
                square.draw(origin_x, origin_y, zoom)


class Camera: 
    def __init__(self):
        self.x_location = MAP_WIDTH / 2
        self.y_location = MAP_HEIGHT / 2
        self.prev_mouse_x = None
        self.prev_mouse_y = None
        self.zoom = 0.2
        self.max_zoom = 2.75
    
    def minZoom(self):
        dx = min(self.x_location - CENTER_X, MAP_WIDTH - self.x_location - CENTER_X)
        dy = min(self.y_location - CENTER_Y, MAP_HEIGHT - self.y_location - CENTER_Y)

        min_x_zoom = WINDOW_WIDTH / (2 * dx + WINDOW_WIDTH)
        min_y_zoom = WINDOW_HEIGHT / (2 * dy + WINDOW_HEIGHT)

        return max(min_x_zoom, min_y_zoom) / 3

    def update(self):
        if pygame.mouse.get_pressed()[1]:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.prev_mouse_x is not None and self.prev_mouse_y is not None:
                dx = mouse_x - self.prev_mouse_x
                dy = mouse_y - self.prev_mouse_y
                
                new_x = self.x_location - dx / self.zoom
                new_y = self.y_location - dy / self.zoom

                if 0 <= new_x - CENTER_X and new_x + CENTER_X <= MAP_WIDTH:
                    self.x_location = new_x
            
                if 0 <= new_y - CENTER_Y and new_y + CENTER_Y <= MAP_HEIGHT:
                    self.y_location = new_y


            self.prev_mouse_x = mouse_x
            self.prev_mouse_y = mouse_y
        else:
            self.prev_mouse_x = None
            self.prev_mouse_y = None

    def render(self, grid):
        grid.draw(self.x_location, self.y_location, self.zoom)


def main():
    grid = Grid()
    camera = Camera()
    running = True
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    new_zoom = camera.zoom * 1.1
                    camera.zoom = min(camera.max_zoom, new_zoom)
                elif e.button == 5:
                    new_zoom = camera.zoom / 1.1
                    min_zoom = camera.minZoom()
                    camera.zoom = max(min_zoom, new_zoom)

        screen.fill(BLACK)

        camera.update()
        camera.render(grid)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()