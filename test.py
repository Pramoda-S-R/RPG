import pygame
import sys

pygame.init()
screen_width , screen_height = 960, 640
screen = pygame.display.set_mode((screen_width, screen_height))

while True:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print(event.key)