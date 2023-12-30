import random
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
RED = (225, 0, 0)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)
BLACK = (0, 0, 0)


def update_display():
    pygame.display.update()


# function to create rect and letter for animation purposes

def create_rect_and_letter(rect, rect_color, text, text_color, font_variable, rect_thickness, rounding=0):
    x_position = rect.x + (rect.width / 2)
    y_position = rect.y + (rect.height / 2)
    new_letter = font_variable.render(text, True, text_color)
    new_letter_rect = new_letter.get_rect(center=(x_position, y_position))
    pygame.draw.rect(SCREEN, rect_color, rect, rect_thickness, rounding)
    SCREEN.blit(new_letter, new_letter_rect)
    return new_letter, new_letter_rect


# used to fill tiles on command
def fill_tiles(tiles, fill=True):
    if isinstance(tiles, list):
        for tile in tiles:
            SCREEN.fill(BG_BLACK, rect=tile)
    else:
        if fill:
            SCREEN.fill(BG_BLACK, rect=tiles)
        else:
            pygame.draw.rect(SCREEN, BG_BLACK, tiles, TILE_THICKNESS)


# animation for when user has attempted to push a word that is not in the word list
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

    def user_skip_animation(): # breaks the animation if the user presses backspace during the animation
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    pygame.draw.rect(SCREEN, BG_BLACK, bad_input_crd, 0, 3)
                    return True

    def shake_row(): # animation for the row shake for invalid input
        fill_tiles(tiles)
        for j in range(len(tiles)):
            tiles[j].x += translation
            pygame.draw.rect(SCREEN, FULL_TILE_GRAY, tiles[j], TILE_THICKNESS)
            create_rect_and_letter(tiles[j], FULL_TILE_GRAY, user_guess[j].upper(), WHITE, font, 2)
        update_display()
        time.sleep(0.065)

    # oscillate the row back and forth at varying degrees of translation, then return to center
    oscillations = 10
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
    for i in range(WHITE[0], 17, -1): # animation a fade out for the box that tells the user their input is invalid
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


def game_won(prev_tiles, curr_tiles, user_guess, tile_colors, tile_letters):  # after every frame, re-render the row above the current row
    win_height = pygame.display.get_surface().get_size()[1]
    win_width = pygame.display.get_surface().get_size()[0]
    font_size = int(win_height / 30)
    font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)

    win_messages = ["Splendid", "Impressive", "Superb"] # list of congrats messages for the winner
    win_message = random.choice(win_messages)
    tile_size = curr_tiles[0].width
    msg_crd_font_size = int(win_height / 60)
    msg_crd_font = pygame.font.Font("NeueHelvetica-Bold.otf", msg_crd_font_size)
    msg_crd = pygame.Rect(win_width / 2 - tile_size, win_height / 10, tile_size * 2, tile_size / 1.4)
    msg_crd_rect = create_rect_and_letter(msg_crd, WHITE, win_message, BLACK, msg_crd_font, 0, 4)[1]


    for index, tile in enumerate(curr_tiles): # translate each tile up and down to show that the game is won
        scale = 16
        init_height = tile.height
        letter, letter_rect = create_rect_and_letter(tile, GREEN, user_guess[index].upper(), WHITE, font, 0, 3)

        for i in range(init_height//scale):
            fill_tiles(tile)
            pygame.draw.rect(SCREEN, BG_BLACK, tile, 0)

            tile.y -= 10
            letter_rect.y -= 10
            pygame.draw.rect(SCREEN, GREEN, tile, 0)
            SCREEN.blit(letter, letter_rect)
            if i % 2 == 0:
                update_display()
                time.sleep(0.03)

        for i in range(init_height//scale):
            fill_tiles(tile)
            pygame.draw.rect(SCREEN, BG_BLACK, tile, 0)
            if len(tile_letters) >= 10: # if we are on the second row or lower
                prev_tile_colors = tile_colors[len(tile_letters) - 10: len(tile_letters) - 5]
                prev_tile_letters = tile_letters[len(tile_letters) - 10: len(tile_letters) - 5]
                prev_row_color = YELLOW if prev_tile_colors[index] == "Yellow" else GREEN if prev_tile_colors[index] == "Green" else TILE_GRAY
                prev_letter, prev_letter_rect = create_rect_and_letter(prev_tiles[index], prev_row_color, prev_tile_letters[index].upper(), WHITE, font, 0)
                fill_tiles(prev_tiles[index])
                pygame.draw.rect(SCREEN, prev_row_color, prev_tiles[index], 0)
                SCREEN.blit(prev_letter, prev_letter_rect)

            tile.y += 10
            letter_rect.y += 10
            pygame.draw.rect(SCREEN, GREEN, tile, 0)
            SCREEN.blit(letter, letter_rect)
            if i % 2 == 0:
                update_display()
                time.sleep(0.04)

    for i in range(WHITE[0], 17, -1):
        txt_color = abs(i - WHITE[0])
        pygame.draw.rect(SCREEN, (i, i, (i + 1 if i < WHITE[0] else WHITE[0])), msg_crd, 0, 3)
        txt_r = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_g = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_b = txt_color if txt_color < BG_BLACK[2] else BG_BLACK[2]
        txt = msg_crd_font.render(win_message, True, (txt_r, txt_g, txt_b))
        SCREEN.blit(txt, msg_crd_rect)
        if i % 2 == 0:
            update_display()



def game_lost(tiles, word): # render the actual word of the day, then let the rect fade out.
    win_width = pygame.display.get_surface().get_size()[0]
    win_height = pygame.display.get_surface().get_size()[1]

    tile_size = tiles[0].width
    wrd_crd_font_size = int(win_height / 65)
    wrd_crd_font = pygame.font.Font("NeueHelvetica-Bold.otf", wrd_crd_font_size)
    wrd_crd = pygame.Rect(win_width / 2 - tile_size, win_height / 10, tile_size * 2, tile_size / 1.4)
    wrd_txt = word.upper()
    wrd_txt_rect = create_rect_and_letter(wrd_crd, WHITE, wrd_txt, BLACK, wrd_crd_font, 0, 4)[1]


    for i in range(WHITE[0], 17, -1):
        txt_color = abs(i - WHITE[0])
        pygame.draw.rect(SCREEN, (i, i, (i+1 if i < WHITE[0] else WHITE[0])), wrd_crd, 0, 3)
        txt_r = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_g = txt_color if txt_color < BG_BLACK[0] else BG_BLACK[0]
        txt_b = txt_color if txt_color < BG_BLACK[2] else BG_BLACK[2]
        wrd_txt = wrd_crd_font.render(word.upper(), True, (txt_r, txt_g, txt_b))
        SCREEN.blit(wrd_txt, wrd_txt_rect)
        update_display()
        if WHITE[0] - 1 >= i >= WHITE[0] - 3:
            time.sleep(1)




def input_animation(tile, input_letter, offset=5): # blip each tile just slightly and change the color to a lighter gray
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


 # shrink and expand the tile on its y-axis, top and bottom, then reverse
def valid_word_animation(tiles, color_values, user_guess, height):
    colors = []

    if user_guess == "ezera":
        colors = [(149, 149, 213), (170, 170, 80), (255, 153, 153), (96, 155, 103), (100, 129, 155)]
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

        loops = int(height/12)  # 117 @ 875 window height
        rate = 1
        delay = 1/(height*0.1)  # the smaller the height the longer the delay

        for i in range(loops//2):
            pygame.draw.rect(SCREEN, BG_BLACK, top_rect, 0)
            pygame.draw.line(SCREEN, FULL_TILE_GRAY,
                             (top_rect.x, top_rect.y + top_rect.height),
                             (top_rect.x + top_rect.width-1, top_rect.y + top_rect.height))
            top_rect.height += rate
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
