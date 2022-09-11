import pygame
import time
from win32api import GetSystemMetrics


pygame.init()

# global variables
CLOCK = pygame.time.Clock()
WIN_WIDTH = GetSystemMetrics(0)/1.1
WIN_HEIGHT = GetSystemMetrics(1)/1.1
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
tile_thickness = 2

# colors
WHITE = (225, 225, 225)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)


def update_display():
    pygame.display.update()


def animate_row(output, tile_matrix, current_row):
    for i in tile_matrix[current_row:current_row+5]:
        pygame.draw.rect(SCREEN, BG_BLACK, i, tile_thickness)
        update_display()
        time.sleep(.05)


    print(tile_matrix)
    print(output)
