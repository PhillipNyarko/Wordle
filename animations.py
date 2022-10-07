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
        pass
    else:
        pass


def create_rect_and_letter(rect, rect_color, text, text_color, font_variable, rect_thickness, rounding=0):
    x_position = rect.x + (rect.width / 2)
    y_position = rect.y + (rect.height / 2)
    new_letter = font_variable.render(text, True, text_color)
    new_letter_rect = new_letter.get_rect(center=(x_position, y_position))
    pygame.draw.rect(SCREEN, rect_color, rect, rect_thickness, rounding)
    SCREEN.blit(new_letter, new_letter_rect)
    return new_letter, new_letter_rect


def bad_input_animation(tiles, user_guess):
    win_width = pygame.display.get_surface().get_size()[0]
    win_height = pygame.display.get_surface().get_size()[1]

    font_size = int(win_height / 30)
    font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

    letters = [font.render(i.upper(), True, WHITE) for i in user_guess]

    tile_size = tiles[0].width
    bad_input_crd_font_size = int(win_height / 65)
    bad_input_crd_font = pygame.font.Font("NeueHelvetica-Bold.otf", bad_input_crd_font_size)
    bad_input_crd = pygame.Rect(win_width / 2 - tile_size, win_height / 10, tile_size * 2, tile_size / 1.4)
    bad_input_txt = "Not in word list"
    bad_input_txt_rect = create_rect_and_letter(bad_input_crd, WHITE, bad_input_txt, BLACK, bad_input_crd_font, 0, 4)[1]

    def fill_tiles():
        for index in tiles:
            SCREEN.fill(BG_BLACK, rect=index)

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

        for j in range(len(tiles)):
            if i <= oscillations/2:
                tiles[j].x += translation
            else:
                tiles[j].x -= translation

            pygame.draw.rect(SCREEN, FULL_TILE_GRAY, tiles[j], TILE_THICKNESS)
            letter_rects = [
                letters[i].get_rect(center=(tiles[i].x + (tiles[i].width / 2), tiles[i].y + (tiles[i].height / 2))) for
                i in range(len(letters))
            ]
            SCREEN.blit(letters[j], letter_rects[j])

        update_display()
        time.sleep(0.1)

    for i in range(WHITE[0], 17, -1):
        txt_color = abs(i - WHITE[0])
        pygame.draw.rect(SCREEN, (i, i, (i+1 if i < WHITE[0] else WHITE[0])), bad_input_crd, 0, 3)
        txt_r = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_g = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_b = txt_color if txt_color < BG_BLACK[2] else BG_BLACK[2]
        bad_input_txt = bad_input_crd_font.render("Not in word list", True, (txt_r, txt_g, txt_b))
        SCREEN.blit(bad_input_txt, bad_input_txt_rect)
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
