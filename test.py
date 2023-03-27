import pygame

WINDOW_X = 800
WINDOW_Y = 600

pygame.init()
pygame.display.set_caption("test")
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), (WINDOW_X / 4, WINDOW_Y / 4, WINDOW_X / 2, WINDOW_Y / 2), 0)

    pygame.display.update()