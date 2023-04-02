from locale import getlocale
from sys import path_hooks
import pygame
from enum import Enum
import random
import math
import json

SQ_SIZE = 10
N_MAP_SQ_X = 180
N_MAP_SQ_Y = 240

MAP_WIDTH = N_MAP_SQ_X * SQ_SIZE
MAP_HEIGHT = N_MAP_SQ_Y * SQ_SIZE

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_CENTER_WIDTH = WINDOW_WIDTH // 2
WINDOW_CENTER_HEIGHT = WINDOW_HEIGHT // 2
WINDOW_SQ_X = math.ceil(WINDOW_WIDTH / SQ_SIZE)
WINDOW_SQ_Y = math.ceil(WINDOW_HEIGHT / SQ_SIZE)


PATH_WIDTH = max(13, min(22, N_MAP_SQ_X // 10))
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

    def draw(self, cam_x, cam_y, zoom):
        pygame.draw.circle(screen, self.color, ((self.x_loc - cam_x) * zoom + WINDOW_CENTER_WIDTH, (self.y_loc - cam_y) * zoom + WINDOW_CENTER_HEIGHT), self.radius)

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

# Responsible for generating the Node Map
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
    
    # render all of our connections, and nodes
    def draw(self, camera_x, camera_y, zoom):
        visible_x = WINDOW_CENTER_WIDTH * 2 // zoom
        visible_y = WINDOW_CENTER_HEIGHT * 2 // zoom
        min_y = max(0, (camera_y - visible_y // 2) // SQ_SIZE)
        max_y = min(N_MAP_SQ_Y, (camera_y + visible_y // 2) // SQ_SIZE + 1)
        min_x = max(0, (camera_x - visible_x // 2) // SQ_SIZE)
        max_x = min(N_MAP_SQ_X, (camera_x + visible_x // 2) // SQ_SIZE + 1)


        for this_node in self.nodes:
            if this_node.next_node is not None:
                for next_node in this_node.next_node:
                    pygame.draw.line(screen, Color.Brown.value, ((this_node.x_loc - camera_x) * zoom + WINDOW_CENTER_WIDTH, (this_node.y_loc - camera_y) * zoom + WINDOW_CENTER_HEIGHT), ((next_node.x_loc - camera_x) * zoom + WINDOW_CENTER_WIDTH, (next_node.y_loc - camera_y) * zoom + WINDOW_CENTER_HEIGHT), int(16 * zoom))
        
        for node in self.nodes:
            node.draw(camera_x, camera_y, zoom)

    # Looks up a nodes configuration based on a nodes index and appends the associated next_node
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

    # if we have a single playable layer we add solo nodes, otherwise we add Entry, Intermediate and Exit nodes
    def instantiatePlayables(self):
        # gets number of playable nodes, section dimensions, and adds solo nodes if we only have 1 layer
        if self.playable_layers == 1:
            layer_count = len(self.playable_nodes)
            section_width, section_height = self.getSectionDimensions(layer_count, 1)

            for i in range(layer_count):
                self.nodes.append(Node.Solo(i, self.getPlayableLocation(i, 0, section_width, section_height)))
        # Otherwise we have no solo nodes and we need to account for sectioning
        else:
            section_height = self.getYDimension(self.playable_layers)
            idx = 0

            for layer in range(self.playable_layers):
                nodes = [n for n in self.playable_nodes if n['layer'] == layer]
                n_nodes = len(nodes)
                section_width = self.getXDimension(n_nodes)

                for i in range(n_nodes):
                    if self.playable_nodes[idx]['next_nodes']:
                        location = self.getPlayableLocation(i, layer, section_width, section_height)

                        # Adjust location if we invert vertically or horizontally
                        if self.orientation == Orientation.BottomUp:
                            location = (location[0], N_MAP_SQ_Y - location[1])
                        if self.orientation == Orientation.RightFacing:
                            location = (N_MAP_SQ_X - location[0], location[1])

                        # If we are in the first layer it's an entry node
                        if layer == 0:
                            self.nodes.append(Node.Entry(idx, location))
                        # If the next node is a stronghold we have an exit
                        elif self.playable_nodes[idx]['next_nodes'][0]['type'] == 'Stronghold':
                            self.nodes.append(Node.Exit(idx, location))
                        # Otherwise we have an intermediary node
                        else:
                            self.nodes.append(Node.Intermediate(idx, location))

                    idx += 1

    # gets number of strongholds and section size, and appends stronghold nodes based on location
    def instantiateStrongholds(self):
        n_strongholds = len(self.strongholds)
        section_size = self.getXDimension(n_strongholds)

        for i in range(n_strongholds):
            self.nodes.append(Node.Stronghold(i, self.getStrongholdLocation(i, section_size)))
    
    # gets number of spawns and section size, and appends spawn nodes based on location
    def instantiateSpawns(self):
        n_spawns = len(self.spawn_points)
        section_size = self.getXDimension(n_spawns)
        
        for i in range(n_spawns):
            self.nodes.append(Node.Spawn(i, self.getSpawnLocation(i, section_size)))

    # If the Orientation is Horizontal, we want to swap the Dimensions of X and Y for the Screen
    # Note: This function is NOT rotating anything. Only swaping Width and Height based on orientation
    def getSectionDimensions(self, x_layers, y_layers): 
        return (self.getXDimension(x_layers), self.getYDimension(y_layers))

    def getXDimension(self, divisor):
        return (N_MAP_SQ_X - PATH_WIDTH * 2) // divisor \
                if self.orientation in [Orientation.TopDown, Orientation.BottomUp] else \
                (N_MAP_SQ_Y - PATH_WIDTH * 2) // divisor

    def getYDimension(self, divisor):
        return (N_MAP_SQ_Y - PATH_WIDTH * 2) // divisor \
                if self.orientation in [Orientation.TopDown, Orientation.BottomUp] else \
                (N_MAP_SQ_X - PATH_WIDTH * 2) // divisor

    # The following 3 location functions are responsible for 'rotating' the orientation
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

    # if the input values are tuples, we calculate the section size * the index + the offset
    # X and Y data should swapped based on orientation before we ever get the location
    def getLocation(self, x_data, y_data):
        x_location = random.randint(x_data[1] * x_data[0] + PATH_WIDTH + PATH_HALF, x_data[1] * (x_data[0] + 1) + PATH_HALF) if isinstance(x_data, tuple) else x_data
        y_location = random.randint(y_data[1] * y_data[0] + PATH_WIDTH + PATH_HALF, y_data[1] * (y_data[0] + 1) + PATH_HALF) if isinstance(y_data, tuple) else y_data

        return (x_location, y_location)

    def generate(self):
        self.instantiateSpawns()
        self.instantiateStrongholds()
        self.instantiatePlayables()
        self.connectEdges()


class Camera: 
    def __init__(self):
        self.x_location = MAP_WIDTH / 2
        self.y_location = MAP_HEIGHT / 2
        self.prev_mouse_x = None
        self.prev_mouse_y = None
        self.zoom = 1
        self.max_zoom = 2.75
    


    def update(self):
        if pygame.mouse.get_pressed()[1]:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.prev_mouse_x is not None and self.prev_mouse_y is not None:
                dx = mouse_x - self.prev_mouse_x
                dy = mouse_y - self.prev_mouse_y
                
                new_x = self.x_location - dx / self.zoom
                new_y = self.y_location - dy / self.zoom

                if 0 <= new_x - WINDOW_CENTER_WIDTH and new_x + WINDOW_CENTER_WIDTH <= MAP_WIDTH:
                    self.x_location = new_x
            
                if 0 <= new_y - WINDOW_CENTER_HEIGHT and new_y + WINDOW_CENTER_HEIGHT <= MAP_HEIGHT:
                    self.y_location = new_y


            self.prev_mouse_x = mouse_x
            self.prev_mouse_y = mouse_y
        else:
            self.prev_mouse_x = None
            self.prev_mouse_y = None

    def zoomIn(self):
        new_zoom = self.zoom * 1.1
        self.zoom = min(self.max_zoom, new_zoom)

    def minZoom(self):
        dx = min(self.x_location - WINDOW_CENTER_WIDTH, MAP_WIDTH - self.x_location - WINDOW_CENTER_WIDTH)
        dy = min(self.y_location - WINDOW_CENTER_HEIGHT, MAP_HEIGHT - self.y_location - WINDOW_CENTER_HEIGHT)

        min_x_zoom = WINDOW_WIDTH / (2 * dx + WINDOW_WIDTH)
        min_y_zoom = WINDOW_HEIGHT / (2 * dy + WINDOW_HEIGHT)

        return max(min_x_zoom, min_y_zoom) / 3

    def zoomOut(self):
        new_zoom = self.zoom / 1.1
        min_zoom = self.minZoom()
        self.zoom = max(min_zoom, new_zoom)

    def render(self, game):
        game.draw(self.x_location, self.y_location, self.zoom)

            
class Game:
    def __init__(self, game_mode, orientation, n_players):
        self.running = True
        self.game_mode = game_mode
        self.map_data = json.load(open('graph.json', 'r'))
        self.map_template = random.choice(self.map_data[n_players - 1]['layouts'])
        self.n_players = n_players
        self.world_map = Map(game_mode, self.map_template, orientation, n_players)
        self.camera = Camera()


def main():
    players = 8 #random.randint(1, 3)
    orientation = Orientation.TopDown
    game_mode = GameMode.Cooperative
    game = Game(game_mode, orientation, players)
    game.world_map.generate()

    while game.running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    print("zooming in")
                    game.camera.zoomIn()
                elif e.button == 5:
                    print("zooming out")
                    game.camera.zoomOut()
        
        screen.fill(Color.Black.value)
        game.camera.update()
        game.camera.render(game.world_map)
        
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main()
    