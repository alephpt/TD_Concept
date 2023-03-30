import pygame
from enum import Enum
import random
import math
import json

SQ_SIZE = 10
N_MAP_SQ_X = 120
N_MAP_SQ_Y = 80

MAP_WIDTH = N_MAP_SQ_X * SQ_SIZE
MAP_HEIGHT = N_MAP_SQ_Y * SQ_SIZE

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CENTER_WIDTH = WINDOW_WIDTH / 2
CENTER_HEIGHT = WINDOW_HEIGHT / 2

PATH_WIDTH = max(13, min(22, N_MAP_SQ_X // 8))
PATH_HALF = PATH_WIDTH // 2

L_EDGE = PATH_WIDTH
R_EDGE = N_MAP_SQ_X - L_EDGE
T_EDGE = PATH_WIDTH + PATH_HALF
B_EDGE = N_MAP_SQ_Y - T_EDGE

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
    def __init__(self, node_type, index, color, location_x, location_y, radius):
        self.type = node_type
        self.index = index
        self.x_loc = location_x * SQ_SIZE
        self.y_loc = location_y * SQ_SIZE
        self.color = color
        self.radius = radius
        self.next_node = []

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x_loc, self.y_loc), self.radius)

    @classmethod
    def Solo(cls, index, l_edge, r_edge, t_edge, b_edge):
        return cls(NodeType.Solo, index, Color.Purple.value, random.randint(l_edge, r_edge), random.randint(t_edge, b_edge), NODE_RADIUS)

    @classmethod
    def Entry(cls, index, l_edge, r_edge, t_edge, b_edge):
        return cls(NodeType.Entry, index, Color.Green.value, random.randint(l_edge, r_edge), random.randint(t_edge, b_edge), NODE_RADIUS)

    @classmethod
    def Intermediate(cls, index, l_edge, r_edge, t_edge, b_edge):
        return cls(NodeType.Intermediate, index, Color.Orange.value, random.randint(l_edge, r_edge), random.randint(t_edge, b_edge), NODE_RADIUS)

    @classmethod
    def Exit(cls, index, l_edge, r_edge, t_edge, b_edge):
        return cls(NodeType.Exit, index, Color.Red.value, random.randint(l_edge, r_edge), random.randint(t_edge, b_edge), NODE_RADIUS)

    @classmethod
    def Spawn(cls, index, l_edge, r_edge):
        return cls(NodeType.Spawn, index, Color.LightRed.value, random.randint(l_edge, r_edge), 0, NODE_RADIUS // 2)

    @classmethod
    def Target(cls, index, l_edge, r_edge):
        return cls(NodeType.Target, index, Color.LightGreen.value, random.randint(l_edge, r_edge), N_MAP_SQ_Y, NODE_RADIUS // 2)



class Map:
    def __init__(self, game_mode, n_players, template):
        self.spawn_points = template["spawn"]
        self.playable_nodes = template["playable"]
        self.strongholds = template["stronghold"]
        self.player_layers = template["playable_layers"]
        self.game_mode = game_mode
        self.n_players = n_players
        self.nodes = []
    
    def draw(self):
        for this_node in self.nodes:
            if this_node.next_node:
                for next_node in this_node.next_node:
                    pygame.draw.line(screen, Color.Brown.value, (this_node.x_loc, this_node.y_loc), (next_node.x_loc, next_node.y_loc), 8)
            this_node.draw()        

    def connectEdges(self):
        for node in self.nodes:
            if node.type == NodeType.Spawn:
                node_map = self.spawn_points[node.index]["next_node"]
                next_node_type = node_map["type"]

    def instantiateNodes(self, ):
        n_strongholds = len(self.strongholds)
        stronghold_sections = (N_MAP_SQ_X - PATH_WIDTH * 2) // n_strongholds
        n_spawns = len(self.spawn_points)
        spawn_sections = (N_MAP_SQ_X - PATH_WIDTH * 2) // n_spawns

        for i in range(n_strongholds):
            self.nodes.append(Node.Target(i, stronghold_sections * i + L_EDGE + PATH_HALF, stronghold_sections * (i + 1)))
        
        if self.player_layers == 1:
            layer_count = len(self.playable_nodes)
            section_width = (N_MAP_SQ_X - PATH_WIDTH * 2) // (layer_count - 1)

            for i in range(layer_count):
                self.node.append(Node.Solo(i, section_width * i + L_EDGE + PATH_HALF, section_width * (i + 1)), T_EDGE, B_EDGE)
        else:
            layer_height = N_MAP_SQ_Y // (self.player_layers + 1)

            # for every layer
            for layer in range(self.player_layers):
                players_per_layer = len([n for n in self.playable_nodes if n["layer"] == layer])
                section_width = (N_MAP_SQ_X - PATH_WIDTH * 2) // (players_per_layer - 1)
                
                for i in range(self.playable_nodes):
                    if self.playable_nodes[i]["layer"] == layer:
                        if layer == 0:
                            # check if next node is a stronghold -> solo node
                            if self.playable_nodes[i]["next_node"]["type"] == "stronghold":
                                self.node.append(Node.Solo(i, \
                                                           section_width * i + L_EDGE + PATH_HALF, \
                                                           section_width * (i + 1), \
                                                           layer_height * layer, \
                                                           layer_height * (layer + 1)))
                            # else it's an entry node
                            else: 
                                self.node.append(Node.Entry(i, \
                                                           section_width * i + L_EDGE + PATH_HALF, \
                                                           section_width * (i + 1), \
                                                           layer_height * layer, \
                                                           layer_height * (layer + 1)))
                        # else if a nodes next type is stronghold it's an exit node
                        elif self.playable_nodes[i]["next_node"]["type"] == "stronghold":
                            self.node.append(Node.Exit(i, \
                                                           section_width * i + L_EDGE + PATH_HALF, \
                                                           section_width * (i + 1), \
                                                           layer_height * layer, \
                                                           layer_height * (layer + 1)))
                        # else it's in the middle
                        else:
                            self.node.append(Node.Intermediary(i, \
                                                           section_width * i + L_EDGE + PATH_HALF, \
                                                           section_width * (i + 1), \
                                                           layer_height * layer, \
                                                           layer_height * (layer + 1)))

        for spawn_node in self.spawn_points:
            self.nodes.append(Node.Spawn(i, spawn_sections * i + L_EDGE + PATH_HALF, spawn_sections * (i + 1)))

    def generate(self):
        self.instantiateNodes()
        self.connectEdges()


            
class Game:
    def __init__(self, game_mode, n_players):
        self.running = True
        self.game_mode = game_mode
        self.map_data = json.load(open('graph.json', 'r'))
        self.map_template = random.choice(self.map_data[n_players - 1]['layouts'])
        self.n_players = n_players
        self.world_map = Map(game_mode, n_players, self.map_template)


def main():
    players = 2
    game_mode = GameMode.Cooperative
    game = Game(game_mode, players)
    game.world_map.generate()

    print(json.dumps(game.world_map.data, indent=2))
    
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
    