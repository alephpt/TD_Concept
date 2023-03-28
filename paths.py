import pygame
from enum import Enum
import random
import math
import json

from entry import N_MAP_SQUARES_X

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


class GameMode(Enum):
    Solo = 0
    Cooperative = 1
    Survival = 2
    Combative = 3

    
class Node:
    def __init__(self, type, color, location_x, location_y, radius):
        self.type = type
        self.x_loc = location_x * SQ_SIZE
        self.y_loc = location_y * SQ_SIZE
        self.color = color
        self.radius = radius
        self.next = []

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x_loc, self.y_loc), self.radius)

    @classmethod
    def Solo(cls, l_edge, r_edge, t_edge, b_edge):
        return cls(NodeType.Solo, Color.Purple.value, random.randint(l_edge, r_edge), random.randint(t_edge, b_edge), NODE_RADIUS)

    @classmethod
    def Spawn(cls, l_edge, r_edge):
        return cls(NodeType.Spawn, Color.LightRed.value, random.randint(l_edge, r_edge), 0, NODE_RADIUS // 2)

    @classmethod
    def Target(cls, l_edge, r_edge):
        return cls(NodeType.Spawn, Color.LightGreen.value, random.randint(l_edge, r_edge), N_MAP_SQ_Y, NODE_RADIUS // 2)



class Map:
    def __init__(self, game_mode, n_players):
        self.nodes = self.instantiateNodes(game_mode, n_players)
    
    def draw(self):
        for this_node in self.nodes:
            for next_node in node.next:
                pygame.draw.line(screen, Color.Brown.value, (this_node.x_loc, this_node.y_loc), (next_node.x_loc, next_node.y_loc), 8)
        
        for node in self.nodes:
            node.draw()        

            if node.type == NodeType.Entry:
                pygame.draw.circle(screen, Color.Green.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            if node.type == NodeType.Intermediate:
                pygame.draw.circle(screen, Color.Orange.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue
            if node.type == NodeType.Exit:
                pygame.draw.circle(screen, Color.Red.value, (node.x_loc, node.y_loc), NODE_RADIUS)
                continue

    def instantiateNodes(self, game_mode, n_players):
        nodes = []

        if game_mode == GameMode.Solo:
            nodes.append(Node.Spawn(L_EDGE, R_EDGE))
            nodes.append(Node.Solo(L_EDGE, R_EDGE, T_EDGE, B_EDGE))
            nodes.append(Node.Target(L_EDGE, R_EDGE))
        elif game_mode == GameMode.Cooperative:
            if n_players == 2:
                n_strongholds = random.randint(1, 2)
                node_mediant_x = random.randint(L_EDGE + PATH_HALF, R_EDGE - PATH_HALF)
                section_width = N_MAP_SQUARES_X - PATH_WIDTH * 2

                # drawn from one path to strongholds, and then reversed to avoid path overlap
                strongholds = [Node.Target(R_EDGE - section_width * i + L_EDGE, L_EDGE + section_width * i - R_EDGE) for i in range(n_strongholds)]
                spawn1 = Node.Spawn(L_EDGE, N_MAP_SQ_X // 2))
                
                nodes.append(Node.Spawn(N_MAP_SQ_X // 2, R_EDGE))



        return nodes
    


class Game:
    def __init__(self, game_mode, n_players):
        self.running = True
        self.game_mode = game_mode
        self.n_players = n_players
        self.world_map = Map(game_mode, n_players)


def main():
    game = Game(GameMode.Solo, N_PLAYERS)
    
    while game.running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.running = False
        
        screen.fill(Color.Black.value)
        game.world_map.draw()
        
        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    main()
    