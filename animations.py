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


def invalid_word_animation(row=pygame.Rect(200,200, 320, 62)):
    for i in range(5):
        pygame.draw.rect(SCREEN, TILE_GRAY, row, tile_thickness)
        update_display()
        time.sleep(0.05)
        SCREEN.fill(BG_BLACK, rect=row)
        row.x += 10
        pygame.draw.rect(SCREEN, TILE_GRAY, row, tile_thickness)
        update_display()
        time.sleep(0.05)
        SCREEN.fill(BG_BLACK, rect=row)
        row.x -= 20
        pygame.draw.rect(SCREEN, TILE_GRAY, row, tile_thickness)
        update_display()
        time.sleep(0.05)
        SCREEN.fill(BG_BLACK, rect=row)
        row.x += 10
        pygame.draw.rect(SCREEN, TILE_GRAY, row, tile_thickness)
        update_display()
        time.sleep(0.05)


def game_won():
    pass


def input_animation(tile, input_letter, offset=5):
    def inflate_tile(tile_offset, negative=False):
        if negative:
            tile_offset -= tile_offset*2

        font_size = int(WIN_HEIGHT / 30) + tile_offset
        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

        letter_x = tile.x + (tile.width / 2)
        letter_y = tile.y + (tile.height / 2)
        letter = font.render(input_letter.upper(), True, WHITE)
        letter_rect = letter.get_rect(center=(letter_x, letter_y))

        SCREEN.fill(BG_BLACK, rect=tile)
        tile.inflate_ip(tile_offset, tile_offset)
        SCREEN.blit(letter, letter_rect)
        pygame.draw.rect(SCREEN, TILE_GRAY, tile, tile_thickness)
        update_display()

    inflate_tile(offset)
    time.sleep(0.051)
    inflate_tile(offset, negative=True)


def animate_tile(x_pos, y_pos, size, input_letter, value):
    font_size = int(WIN_HEIGHT / 30)
    ry = size
    ry_pos = y_pos
    for i in range(100):
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
        #font_size -= 1
        ry -= 1
        ry_pos += .5

    for i in range(100):
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
        #font_size += 1
        ry += 1
        ry_pos -= .5


