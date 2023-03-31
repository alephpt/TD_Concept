from locale import getlocale
from sys import path_hooks
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
pygame.display.set_caption('Path Mapping')

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Color(Enum): 
    Black = (0, 0, 0)
    Red = (138, 34, 6)
    Purple = (84, 84, 222)
    Green = (41, 95, 64)
    Orange = (111, 64, 15)
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
    Stronghold = 5


class GameMode(Enum):
    Solo = 0
    Cooperative = 1
    Survival = 2
    Combative = 3

class Orientation(Enum):
    RightFacing = 0
    TopDown = 1
    LeftFacing = 2
    BottomUp = 3
    
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
    def Solo(cls, index, location):
        return cls(NodeType.Solo, index, Color.Purple.value, location[0], location[1], NODE_RADIUS)

    @classmethod
    def Entry(cls, index, location):
        return cls(NodeType.Entry, index, Color.Green.value, location[0], location[1], NODE_RADIUS)

    @classmethod
    def Intermediate(cls, index, location):
        return cls(NodeType.Intermediate, index, Color.Orange.value, location[0], location[1], NODE_RADIUS)

    @classmethod
    def Exit(cls, index, location):
        return cls(NodeType.Exit, index, Color.Red.value, location[0], location[1], NODE_RADIUS)

    @classmethod
    def Spawn(cls, index, location):
        return cls(NodeType.Spawn, index, Color.LightRed.value, location[0], location[1], NODE_RADIUS // 2)

    @classmethod
    def Stronghold(cls, index,location):
        return cls(NodeType.Stronghold, index, Color.LightGreen.value, location[0], location[1], NODE_RADIUS // 2)


class Map:
    def __init__(self, game_mode, template, orientation, n_players):
        self.orientation = orientation
        self.spawn_points = template['spawn']
        self.playable_nodes = template['playable']
        self.strongholds = template['stronghold']
        self.playable_layers = template['playable_layers']
        self.game_mode = game_mode
        self.n_players = n_players
        self.nodes = []
    
    def draw(self):
        for this_node in self.nodes:
            if this_node.next_node is not None:
                for next_node in this_node.next_node:
                    pygame.draw.line(screen, Color.Brown.value, (this_node.x_loc, this_node.y_loc), (next_node.x_loc, next_node.y_loc), 8)
        
        for node in self.nodes:
            node.draw()

    def connectEdges(self):
        node_map = {(node.type.name, node.index): node for node in self.nodes}

        for node in self.nodes:
            next_nodes = None

            if node.type == NodeType.Stronghold:
                node.next_node = None
                continue
            elif node.type == NodeType.Spawn:
                next_nodes = self.spawn_points[node.index].get('next_nodes', [])
            elif node.type in [NodeType.Solo, NodeType.Exit, NodeType.Entry, NodeType.Intermediate]:
                next_nodes = self.playable_nodes[node.index].get('next_nodes', [])

            for next_node_data in next_nodes:
                print(node.type.name, node.index, "->", next_node_data['type'], next_node_data['index'])
                if next_node := node_map.get((next_node_data['type'], next_node_data['index'])):
                    node.next_node.append(next_node)

    def getXDimension(self, divisor):
        return (N_MAP_SQ_X - PATH_WIDTH * 2) // divisor \
                if self.orientation in [Orientation.TopDown, Orientation.BottomUp] else \
                (N_MAP_SQ_Y - PATH_WIDTH * 2) // divisor

    def getYDimension(self, divisor):
        return (N_MAP_SQ_Y - PATH_WIDTH * 2) // divisor \
                if self.orientation in [Orientation.TopDown, Orientation.BottomUp] else \
                (N_MAP_SQ_X - PATH_WIDTH * 2) // divisor

    def getSectionDimensions(self, x_layers, y_layers): 
        # If the Orientation is Horizontal, we want to swap the Dimensions of X and Y for the Screen
        # Note: This function is note rotating anything, only swapping Height for Width
        return (self.getXDimension(x_layers), self.getYDimension(y_layers))

    def instantiatePlayables(self):
        if self.playable_layers == 1:
            layer_count = len(self.playable_nodes)
            section_width, section_height = self.getSectionDimensions(layer_count, 1)

            for i in range(layer_count):
                self.nodes.append(Node.Solo(i, self.getPlayableLocation(i, 0, section_width, section_height)))
        else:
            section_height = self.getYDimension(self.playable_layers)
            idx = 0

            for layer in range(self.playable_layers):
                nodes = [n for n in self.playable_nodes if n['layer'] == layer]
                section_width = self.getXDimension(len(nodes))
                for i in range(len(nodes)):
                        location = self.getPlayableLocation(i, layer, section_width, section_height)

                        if self.orientation == Orientation.BottomUp:
                            location = (location[0], N_MAP_SQ_Y - location[1])
                        if self.orientation == Orientation.RightFacing:
                            location = (N_MAP_SQ_X - location[0], location[1])

                        if layer == 0:
                            self.nodes.append(Node.Entry(idx, location))
                        elif self.playable_nodes[idx]['next_nodes'][0]['type'] == 'Stronghold':
                            self.nodes.append(Node.Exit(idx, location))
                        else:
                            self.nodes.append(Node.Intermediate(idx, location))

                        idx += 1

    def instantiateStrongholds(self):
        n_strongholds = len(self.strongholds)
        section_size = self.getXDimension(n_strongholds)

        for i in range(n_strongholds):
            self.nodes.append(Node.Stronghold(i, self.getStrongholdLocation(i, section_size)))

    def instantiateSpawns(self):
        n_spawns = len(self.spawn_points)
        section_size = self.getXDimension(n_spawns)
        
        for i in range(n_spawns):
            self.nodes.append(Node.Spawn(i, self.getSpawnLocation(i, section_size)))

    def getLocation(self, x_data, y_data):
        y_index = 0
        y_section_size = 0
        x_index = 0
        x_section_size = 0
        x_location = 0
        y_location = 0

        if isinstance(x_data, tuple):
            x_index, x_section_size  = x_data
            x_location = random.randint(x_section_size * x_index + PATH_WIDTH + PATH_HALF, x_section_size * (x_index + 1))
        else:
            x_location = x_data

        if isinstance(y_data, tuple):
            y_index ,y_section_size = y_data
            y_location = random.randint(y_section_size * y_index + PATH_WIDTH + PATH_HALF, y_section_size * (y_index + 1))
        else:
            y_location = y_data
        
        # Todo: Determine if we need this? :think:
        # if we are inverting the map vertically, we need to flip the locations horizontally
        # if self.orientation == Orientation.BottomUp:
        #    x_location = N_MAP_SQ_X - x_location
        # if we are inverting the map horizontally, we need to flip the locations vertically
        # elif self.orientation == Orientation.RightFacing:
        #    y_location = N_MAP_SQ_Y - y_location


        return (x_location, y_location)

    def getStrongholdLocation(self, i, section_size):
        if self.orientation == Orientation.TopDown:
            return self.getLocation((i, section_size), N_MAP_SQ_Y)
        elif self.orientation == Orientation.BottomUp:
            return  self.getLocation((i, section_size), 0)
        elif self.orientation == Orientation.RightFacing:
            return  self.getLocation(0, (i, section_size))
        elif self.orientation == Orientation.LeftFacing:
            return  self.getLocation(N_MAP_SQ_X, (i, section_size))

    def getSpawnLocation(self, i, section_size):
        if self.orientation == Orientation.TopDown:
            return self.getLocation((i, section_size), 0)
        elif self.orientation == Orientation.BottomUp:
            return self.getLocation((i, section_size), N_MAP_SQ_Y)
        elif self.orientation == Orientation.RightFacing:
            return self.getLocation(N_MAP_SQ_X, (i, section_size))
        elif self.orientation == Orientation.LeftFacing:
            return self.getLocation(0, (i, section_size))

    def getPlayableLocation(self, ix, iy, section_width, section_height):
        if self.orientation in [Orientation.TopDown, Orientation.BottomUp]:
            return self.getLocation((ix, section_width), (iy, section_height))
        elif self.orientation in [Orientation.LeftFacing, Orientation.RightFacing]:
            return self.getLocation((iy, section_height), (ix, section_width))


    def generate(self):
        self.instantiateSpawns()
        self.instantiateStrongholds()
        self.instantiatePlayables()
        self.connectEdges()

            
class Game:
    def __init__(self, game_mode, orientation, n_players):
        self.running = True
        self.game_mode = game_mode
        self.map_data = json.load(open('graph.json', 'r'))
        self.map_template = self.map_data[n_players - 1]['layouts'][0] #random.choice(self.map_data[n_players - 1]['layouts'])
        self.n_players = n_players
        self.world_map = Map(game_mode, self.map_template, orientation, n_players)


def main():
    players = 3 #random.randint(1, 3)
    orientation = Orientation.RightFacing
    game_mode = GameMode.Cooperative
    game = Game(game_mode, orientation, players)
    game.world_map.generate()

    while game.running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.running = False
        
        screen.fill(Color.Black.value)
        game.world_map.draw()
        
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main()
    