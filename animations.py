import time

import pygame
import pyautogui

pygame.init()

# fix tile flip animation
# fix correct word animation
# add play again button

# global variables
WIN_WIDTH = pyautogui.size()[0]/1.2
WIN_HEIGHT = pyautogui.size()[1]/1.2
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
TILE_SIZE = WIN_HEIGHT/15
TILE_THICKNESS = 2

# colors
WHITE = (225, 225, 225)
RED = (225, 0, 0)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)
BLACK = (0, 0, 0)


def update_display():
    pygame.display.update()

def create_rect_and_letter(rect, rect_color, text, text_color, font_variable, rect_thickness, rounding=0):
    x_position = rect.x + (rect.width / 2)
    y_position = rect.y + (rect.height / 2)
    new_letter = font_variable.render(text, True, text_color)
    new_letter_rect = new_letter.get_rect(center=(x_position, y_position))
    pygame.draw.rect(SCREEN, rect_color, rect, rect_thickness, rounding)
    SCREEN.blit(new_letter, new_letter_rect)
    return new_letter, new_letter_rect


def fill_tiles(tiles, fill=True):
    if isinstance(tiles, list):
        for tile in tiles:
            SCREEN.fill(BG_BLACK, rect=tile)
    else:
        if fill:
            SCREEN.fill(BG_BLACK, rect=tiles)
        else:
            pygame.draw.rect(SCREEN, BG_BLACK, tiles, TILE_THICKNESS)


def bad_input_animation(tiles, user_guess):
    pygame.event.clear()
    win_width = pygame.display.get_surface().get_size()[0]
    win_height = pygame.display.get_surface().get_size()[1]

    font_size = int(win_height / 30)
    font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

    tile_size = tiles[0].width
    bad_input_crd_font_size = int(win_height / 65)
    bad_input_crd_font = pygame.font.Font("NeueHelvetica-Bold.otf", bad_input_crd_font_size)
    bad_input_crd = pygame.Rect(win_width / 2 - tile_size, win_height / 10, tile_size * 2, tile_size / 1.4)
    bad_input_txt = "Not in word list"
    bad_input_txt_rect = create_rect_and_letter(bad_input_crd, WHITE, bad_input_txt, BLACK, bad_input_crd_font, 0, 4)[1]

    def user_skip_animation():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    pygame.draw.rect(SCREEN, BG_BLACK, bad_input_crd, 0, 3)
                    return True

    def shake_row():
        fill_tiles(tiles)
        for j in range(len(tiles)):
            tiles[j].x += translation
            pygame.draw.rect(SCREEN, FULL_TILE_GRAY, tiles[j], TILE_THICKNESS)
            create_rect_and_letter(tiles[j], FULL_TILE_GRAY, user_guess[j].upper(), WHITE, font, 2)
        update_display()
        time.sleep(0.065)

    oscillations = 20
    skip_animation = False
    for i in range(oscillations//2):
        if user_skip_animation():
            skip_animation = True
        if skip_animation:
            break
        translation = i + 1 if i % 2 == 0 else -(i+1)
        shake_row()
    for i in range(oscillations//2, 0, -1):
        if user_skip_animation():
            skip_animation = True
        if skip_animation:
            break
        translation = i if i % 2 == 0 else -i
        shake_row()
    for i in range(WHITE[0], 17, -1):
        if user_skip_animation():
            skip_animation = True
        if skip_animation:
            break
        txt_color = abs(i - WHITE[0])
        pygame.draw.rect(SCREEN, (i, i, (i+1 if i < WHITE[0] else WHITE[0])), bad_input_crd, 0, 3)
        txt_r = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_g = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_b = txt_color if txt_color < BG_BLACK[2] else BG_BLACK[2]
        bad_input_txt = bad_input_crd_font.render("Not in word list", True, (txt_r, txt_g, txt_b))
        SCREEN.blit(bad_input_txt, bad_input_txt_rect)
        update_display()
    if skip_animation:
        return True


def game_won(prev_tiles, curr_tiles, user_guess):  # after every frame, re-render the row above the current row
    win_height = pygame.display.get_surface().get_size()[1]
    font_size = int(win_height / 30)
    font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

    for index, tile in enumerate(curr_tiles):
        scale = 16
        init_height = tile.height
        letter, letter_rect = create_rect_and_letter(tile, GREEN, user_guess[index].upper(), WHITE, font, 0)

        for i in range(init_height//scale):
            fill_tiles(tile)
            pygame.draw.rect(SCREEN, BG_BLACK, tile, 0)

            tile.y -= 10
            letter_rect.y -= 10
            pygame.draw.rect(SCREEN, GREEN, tile, 0)
            SCREEN.blit(letter, letter_rect)
            if i % 2 == 0:
                update_display()
                time.sleep(0.04)

        for i in range(init_height//scale): #################
            fill_tiles(tile)
            pygame.draw.rect(SCREEN, BG_BLACK, tile, 0)

            tile.y += 10
            letter_rect.y += 10
            pygame.draw.rect(SCREEN, GREEN, tile, 0)
            SCREEN.blit(letter, letter_rect)
            if i % 2 == 0:
                update_display()
                time.sleep(0.04)

def game_lost():
    # render actual word at the end
    # animate reset button
    pass


def input_animation(tile, input_letter, offset=5):
    def inflate_tile(tile_offset, negative=False):
        if negative:
            tile_offset -= tile_offset*2

        win_height = pygame.display.get_surface().get_size()[1]
        font_size = int(win_height / 30) + tile_offset
        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

        letter, letter_rect = create_rect_and_letter(tile, TILE_GRAY, input_letter.upper(), WHITE, font, TILE_THICKNESS)

        SCREEN.fill(BG_BLACK, rect=tile)
        tile.inflate_ip(tile_offset, tile_offset)
        SCREEN.blit(letter, letter_rect)
        pygame.draw.rect(SCREEN, TILE_GRAY, tile, TILE_THICKNESS)
        update_display()

    inflate_tile(offset)
    time.sleep(0.051)
    inflate_tile(offset, negative=True)


def valid_word_animation(tiles, color_values, user_guess):
    colors = []

    if user_guess == "ezera":
        colors = [(149,149,213), (170, 170, 80), (255,153,153), (96,155,103), (100,129,155)]
    else:
        for index, value in enumerate(color_values):
            if value == "Green":
                colors.append(GREEN)
            elif value == "Yellow":
                colors.append(YELLOW)
            elif value == "Gray":
                colors.append(TILE_GRAY)

    for index, tile in enumerate(tiles):
        top_rect = pygame.Rect((tile.x, tile.y), (tile.width, 0))
        bottom_rect = pygame.Rect((tile.x, tile.y + tile.height), (tile.width, 0))
        win_height = pygame.display.get_surface().get_size()[1]
        font_size = int(win_height / 30)
        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

        loops = 108
        rate = 1
        delay = 0.0035 / (tile.height / 101)
        for i in range(loops//2):
            pygame.draw.rect(SCREEN, BG_BLACK, top_rect, 0)
            pygame.draw.line(SCREEN, FULL_TILE_GRAY,
                             (top_rect.x, top_rect.y + top_rect.height),
                             (top_rect.x + top_rect.width-1, top_rect.y + top_rect.height))
            top_rect.height +=  rate
            pygame.draw.rect(SCREEN, BG_BLACK, bottom_rect, 0)
            pygame.draw.line(SCREEN, FULL_TILE_GRAY,
                             (bottom_rect.x, bottom_rect.y-1),
                             (bottom_rect.x + bottom_rect.width - 1, bottom_rect.y-1))
            bottom_rect.height += rate
            bottom_rect.y -= rate
            if i % 5 == 0:
                update_display()
                time.sleep(delay)

        for i in range(loops//2):
            top_rect.height -= rate
            bottom_rect.y += rate
            bottom_rect.height -= rate
            letter, letter_rect = create_rect_and_letter(tile, colors[index], user_guess[index].upper(), WHITE, font, 0)
            SCREEN.blit(letter, letter_rect)
            pygame.draw.rect(SCREEN, BG_BLACK, top_rect, 0)
            pygame.draw.rect(SCREEN, BG_BLACK, bottom_rect, 0)
            if i % 5 == 0:
                update_display()
                time.sleep(delay)
#
def reset_animation():
    pass





