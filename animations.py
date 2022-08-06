import pygame
import time

pygame.init()

WHITE = (225, 225, 225)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)
font = pygame.font.Font("NeueHelvetica-Bold.otf", 30)


def update_display():
    pygame.display.update()
