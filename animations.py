import time

import pygame
import pyautogui

pygame.init()

# global variables
WIN_WIDTH = pyautogui.size()[0]/1.2
WIN_HEIGHT = pyautogui.size()[1]/1.2
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
TILE_SIZE = WIN_HEIGHT/15

# font and styling variables
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


def game_won():
    pass


def animate_tile(x_pos, y_pos, size, input_letter, value):
    font_size = int(WIN_HEIGHT / 30)
    ry = size
    ry_pos = y_pos
    for i in range(60):
        rect = pygame.Rect(x_pos, ry_pos, size, ry)
        rect.center = (rect.x + rect.width / 2, rect.y + rect.height / 2)

        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

        letter_x = rect.x + (rect.width / 2)
        letter_y = rect.y + (rect.height / 2)
        letter = font.render(input_letter.upper(), True, WHITE)
        letter_rect = letter.get_rect(center=(letter_x, letter_y))

        pygame.draw.rect(SCREEN, TILE_GRAY, rect, tile_thickness)
        SCREEN.blit(letter, letter_rect)
        update_display()

        time.sleep(0.003)
        SCREEN.fill(BG_BLACK)
        font_size -= 1
        ry -= 1
        ry_pos += .5

    for i in range(60):
        rect = pygame.Rect(x_pos, ry_pos, size, ry)
        rect.center = (rect.x + rect.width / 2, rect.y + rect.height / 2)

        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

        letter_x = rect.x + (rect.width / 2)
        letter_y = rect.y + (rect.height / 2)
        letter = font.render(input_letter.upper(), True, WHITE)
        letter_rect = letter.get_rect(center=(letter_x, letter_y))

        pygame.draw.rect(SCREEN, GREEN, rect, 0)
        SCREEN.blit(letter, letter_rect)
        update_display()

        time.sleep(0.003)
        SCREEN.fill(BG_BLACK)
        font_size += 1
        ry += 1
        ry_pos -= .5

while True:
    animate_tile(WIN_WIDTH/2.3, WIN_HEIGHT/2, TILE_SIZE, "x", "Green")
