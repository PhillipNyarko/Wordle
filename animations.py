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
BLACK = (0, 0, 0)

def update_display():
    pygame.display.update()


def fade_rect(rect, fade_in=True, fade_out=False):
    if fade_in:
        for i in range(100):
            rect = pygame.Rect(200, 300, 45, 30)
            pygame.draw.rect(SCREEN, WHITE, rect, 0, 1)
            update_display()
    else:
        pass


def bad_input_animation(row, tile_size, tile_spacing, letters):
    x_pos_inc = 0

    tile_list = []
    letter_list = []
    letter_rect_list = []

    win_width = pygame.display.get_surface().get_size()[0]
    win_height = pygame.display.get_surface().get_size()[1]

    font_size = int(win_height / 30)

    font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

    def fill_tiles():
        for index in tile_list:
            SCREEN.fill(BG_BLACK, rect=index)

    def draw_tile_and_letter():
        SCREEN.blit(letter_list[k], letter_rect_list[k])
        pygame.draw.rect(SCREEN, FULL_TILE_GRAY, tile_list[k], TILE_THICKNESS)

    SCREEN.fill(BG_BLACK, rect=row)
    bad_input_card_font_size = int(win_height / 65)
    bad_input_card_font = pygame.font.Font("NeueHelvetica-Bold.otf", bad_input_card_font_size)

    bad_input_card = pygame.Rect(win_width / 2 - tile_size, win_height / 10, tile_size * 2, tile_size / 1.4)
    bad_input_text = bad_input_card_font.render("Not in word list", True, BLACK)
    bad_input_text_x = bad_input_card.x + (bad_input_card.width / 2)
    bad_input_text_y = bad_input_card.y + (bad_input_card.height / 2)
    bad_input_card_rect = bad_input_text.get_rect(center=(bad_input_text_x, bad_input_text_y))
    pygame.draw.rect(SCREEN, WHITE, bad_input_card, 0, 3)
    SCREEN.blit(bad_input_text, bad_input_card_rect)

    for j in range(len(letters)):
        x_pos = row.x + x_pos_inc
        tile = pygame.Rect(x_pos, row.y, tile_size, tile_size)
        tile.centery = row.centery
        tile_list.append(tile)
        x_pos_inc += tile_size + tile_spacing

        letter_x = tile.x + (tile.width / 2)
        letter_y = tile.y + (tile.height / 2)
        letter = font.render(letters[j].upper(), True, WHITE)
        letter_list.append(letter)
        letter_rect = letter.get_rect(center=(letter_x, letter_y))
        letter_rect_list.append(letter_rect)

        SCREEN.blit(letter, letter_rect)
        pygame.draw.rect(SCREEN, FULL_TILE_GRAY, tile, TILE_THICKNESS)
        update_display()

    oscillations = 8
    oscillation_multiplier = .8   # scales the translations
    for i in range(oscillations):
        if i <= oscillations / 2:
            if i % 2 == 0:
                translation = -(i**oscillation_multiplier)
            else:
                translation = i ** oscillation_multiplier
        else:
            if i % 2 == 0:
                translation = -(i**oscillation_multiplier)
            else:
                translation = i ** oscillation_multiplier

        fill_tiles()

        for k in range(len(tile_list)):
            if i <= oscillations/2:
                tile_list[k].x += translation
            else:
                tile_list[k].x -= translation
            letter_rect_list[k] = letter_list[k].get_rect(center=(tile_list[k].x + tile_list[k].width / 2, tile_list[k].y + tile_list[k].height / 2))
            draw_tile_and_letter()

        update_display()
        time.sleep(0.1)

    time.sleep(1)
    for i in range(WHITE[0], 17, -3):
        txt_color = abs(i - WHITE[0])
        pygame.draw.rect(SCREEN, (i, i, (i+1 if i < WHITE[0] else WHITE[0])), bad_input_card, 0, 3)
        txt_r = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_g = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_b = txt_color if txt_color < BG_BLACK[2] else BG_BLACK[2]
        bad_input_text = bad_input_card_font.render("Not in word list", True, (txt_r, txt_g, txt_b))
        SCREEN.blit(bad_input_text, bad_input_card_rect)
        update_display()


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
