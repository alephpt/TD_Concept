import pygame
from enum import Enum
import random
import math

SQ_SIZE = 10
N_MAP_SQ_X = 120
N_MAP_SQ_Y = 80

MAP_WIDTH = N_MAP_SQ_X * SQ_SIZE
MAP_HEIGHT = N_MAP_SQ_Y * SQ_SIZE

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CENTER_WIDTH = WINDOW_WIDTH / 2
CENTER_HEIGHT = WINDOW_HEIGHT / 2

WINDOW_SQ_X = WINDOW_WIDTH // SQ_SIZE
WINDOW_SQ_Y = WINDOW_HEIGHT // SQ_SIZE

PATH_WIDTH = max(13, min(22, N_MAP_SQ_X // 8))
PATH_HALF = PATH_WIDTH // 2

L_EDGE = PATH_WIDTH
R_EDGE = N_MAP_SQ_X - L_EDGE
T_EDGE = PATH_WIDTH + PATH_HALF
B_EDGE = N_MAP_SQ_Y - T_EDGE

N_PLAYERS = 1
NODE_RADIUS = 30

pygame.init()
pygame.display.set_caption("Path Mapping")

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Color(Enum): 
    Black = (0, 0, 0)
    Red = (132, 68, 13)
    Purple = (84, 84, 222)
    Green = (41, 95, 64)
    Orange = (222, 123, 15)
    Brown = (87, 48, 13)
    LightRed = (222, 138, 138)
    LightGreen = (175, 198, 170)
    Gray = (132, 236, 128)
    White = (222, 222, 222)


class NodeType(Enum):
    Spawn = 0
    Solo = 1
    Entry = 2
    Intermediate = 3
    Exit = 4
    Target = 5


class GameModes(Enum):
    Solo = 0
    Cooperative = 1
    Survival = 2
    Combative = 3

    
class Node:
    def __init__(self, type, location_x, location_y):
        self.type = type
        self.x_loc = location_x * SQ_SIZE
        self.y_loc = location_y * SQ_SIZE
        

class Map:
    def __init__(self):
        self.nodes = []
    
    def draw(self):
        for path in range(len(self.nodes) - 1):
            pygame.draw.line(screen, Color.Brown.value, (self.nodes[path].x_loc, self.nodes[path].y_loc), \
                                                        (self.nodes[path + 1].x_loc, self.nodes[path + 1].y_loc), 8)
        
        for node in self.nodes:
            if node.type == NodeType.Solo:
                pygame.draw.circle(screen, Color.Purple.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            if node.type == NodeType.Spawn:
                pygame.draw.circle(screen, Color.LightRed.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            if node.type == NodeType.Target:
                pygame.draw.circle(screen, Color.LightGreen.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            if node.type == NodeType.Entry:
                pygame.draw.circle(screen, Color.Green.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            if node.type == NodeType.Intermediate:
                pygame.draw.circle(screen, Color.Orange.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            if node.type == NodeType.Exit:
                pygame.draw.circle(screen, Color.Red.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            
            
    
    def instantiateNodes(self):
        if N_PLAYERS == 1:
            self.nodes.append(Node(NodeType.Spawn, random.randint(L_EDGE, R_EDGE), 0))
            self.nodes.append(Node(NodeType.Solo, random.randint(L_EDGE, R_EDGE), random.randint(T_EDGE, B_EDGE)))
            self.nodes.append(Node(NodeType.Target, random.randint(L_EDGE, R_EDGE), N_MAP_SQ_Y))
        else:
            for i in range(N_PLAYERS):
                self.nodes.append(Node(NodeType.Exit, 0, 0))
    
    
    

def main():
    game_loop = True
    game_map = Map()
    game_map.instantiateNodes()
    
    while game_loop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game_loop = False
        
        screen.fill(Color.Black.value)
        game_map.draw()
        
        pygame.display.update()
        clock.tick(15)

if __name__ == "__main__":
    main()
    