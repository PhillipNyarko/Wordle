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


def fade_rect_in():
    pass


def fade_rect_out():
    pass


def animate_not_in_word_list():
    pass


def animate_row():  # animation that plays after enter on each row
    pass


def game_won():
    pass


