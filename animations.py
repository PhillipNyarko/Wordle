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
TILE_THICKNESS = 2
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


def invalid_word_animation(tile_spacing=6, tile_size=62, letters=["c","r","a","n","e"], row=pygame.Rect(400, 200, 320, 62)):
    x_pos_inc = 0
    tile_list = []
    letter_list = []
    letter_rect_list = []
    win_height = pygame.display.get_surface().get_size()[1]
    font_size = int(win_height / 30)
    font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

    for j in range(len(letters)):
        x_pos = row.x + x_pos_inc
        y_pos = row.y
        tile = pygame.Rect(x_pos, y_pos, tile_size, tile_size)
        tile_list.append(tile)
        tile.centery = row.centery
        x_pos_inc += tile_size + tile_spacing

        letter_x = tile.x + (tile.width / 2)
        letter_y = tile.y + (tile.height / 2)
        letter = font.render(letters[j].upper(), True, WHITE)
        letter_list.append(letter)
        letter_rect = letter.get_rect(center=(letter_x, letter_y))
        letter_rect_list.append(letter_rect)

        SCREEN.blit(letter, letter_rect)
        pygame.draw.rect(SCREEN, TILE_GRAY, tile, TILE_THICKNESS)
        update_display()

    number = 10
    oscillation_multiplier = 1.1
    for i in range(number//2):
        translation = i**oscillation_multiplier
        if i % 2 == 0:
            translation = -(i**oscillation_multiplier)

        for j in tile_list:
            SCREEN.fill(BG_BLACK, rect=j)

        for k in range(len(tile_list)):
            letter_rect_list[k] = letter_list[k].get_rect(center=(tile_list[k].x + tile_list[k].width / 2, tile_list[k].y + tile_list[k].height / 2))
            tile_list[k].x += translation
            pygame.draw.rect(SCREEN, TILE_GRAY, tile_list[k], TILE_THICKNESS)
            SCREEN.blit(letter_list[k], letter_rect_list[k])
        update_display()
        time.sleep(0.1)

    for y in range(number//2, -1, -1):
        translation = y ** oscillation_multiplier
        if y % 2 == 0:
            translation = -(y ** oscillation_multiplier)

        for j in tile_list:
            SCREEN.fill(BG_BLACK, rect=j)

        for k in range(len(tile_list)):
            letter_rect_list[k] = letter_list[k].get_rect(
                center=(tile_list[k].x + tile_list[k].width / 2, tile_list[k].y + tile_list[k].height / 2))
            tile_list[k].x += translation
            pygame.draw.rect(SCREEN, TILE_GRAY, tile_list[k], TILE_THICKNESS)
            SCREEN.blit(letter_list[k], letter_rect_list[k])
        update_display()
        time.sleep(0.1)

def game_won():
    pass


def input_animation(tile, input_letter, offset=5):
    def inflate_tile(tile_offset, negative=False):
        if negative:
            tile_offset -= tile_offset*2

        win_height = pygame.display.get_surface().get_size()[1]
        font_size = int(win_height / 30) + tile_offset
        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

        letter_x = tile.x + (tile.width / 2)
        letter_y = tile.y + (tile.height / 2)
        letter = font.render(input_letter.upper(), True, WHITE)
        letter_rect = letter.get_rect(center=(letter_x, letter_y))

        SCREEN.fill(BG_BLACK, rect=tile)
        tile.inflate_ip(tile_offset, tile_offset)
        SCREEN.blit(letter, letter_rect)
        pygame.draw.rect(SCREEN, TILE_GRAY, tile, TILE_THICKNESS)
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

        pygame.draw.rect(SCREEN, TILE_GRAY, rect, TILE_THICKNESS)
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


SCREEN.fill(BG_BLACK)
invalid_word_animation()
time.sleep(1)