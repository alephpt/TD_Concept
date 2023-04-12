import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define constants
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1200
BACKGROUND_COLOR = (0, 0, 0)
NODE_COLOR = (0, 0, 255)
LINE_COLOR = (0, 255, 0)
NODE_RADIUS = 30


PLAYERS = 1

# Create a window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Node Connections")


BASE_TYPES = ["only", "front", "middle", "read"]

# Define nodes as (x, y) coordinates
nodes = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(5)]

def getBaseType(n):
    if PLAYERS == 1:
        return BASE_TYPES[n]
    
    return "middle"

class Base:
    def __init__(self, idx):
        self.type = getBaseType(idx)

class Player: 
    def __init__(self, idx):
        self.identity = idx
        self.base = Base(idx)

class Map:
    def __init__(self):
        self.player = [Player(n) for n in range(PLAYERS)]


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen with a background color
    screen.fill(BACKGROUND_COLOR)

    # Draw lines connecting the nodes
    for i in range(len(nodes) - 1):
        pygame.draw.line(screen, LINE_COLOR, nodes[i], nodes[i + 1], 8)

    # Draw nodes
    for node in nodes:
        pygame.draw.circle(screen, NODE_COLOR, node, NODE_RADIUS)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()