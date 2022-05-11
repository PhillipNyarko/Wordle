import json
import random

import pygame
import time
from win32api import GetSystemMetrics

# global variables
WIN_LENGTH = GetSystemMetrics(0)-GetSystemMetrics(0)//2
WIN_HEIGHT = GetSystemMetrics(0)-((GetSystemMetrics(0)//2)+150)
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))

# colors
WHITE = (225, 225, 225)
BACKGROUND_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY1 = (58, 58, 60)
GRAY2 = (86, 87, 88)
GRAY3 = (129, 131, 132)
# images
wordle_icon = pygame.image.load("wordle_icon.png")

# initialize and rename
pygame.init()
pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)
screen.fill(BACKGROUND_BLACK)
pygame.display.update()

# create game tile
tile_size_x = 54.39
tile_size_y = 54.39


class Tile:
    def __init__(self, x_pos, y_pos):
        self.color = GRAY1
        self.tile_size = (tile_size_x, tile_size_y)
        self.boarder_thickness = 2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile = pygame.Rect((self.x_pos, self.y_pos), self.tile_size)
        self.empty = True
        self.font_size = WIN_HEIGHT//20
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)
        self.letter_x_pos = self.x_pos + (self.tile_size[0] // 2)
        self.letter_y_pos = (self.y_pos + (self.tile_size[1] // 2))
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y

        pygame.draw.rect(screen, self.color, self.tile, self.boarder_thickness)
        pygame.display.update()

    def display_letter(self, key):
        letter = self.font.render(key, True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
        screen.blit(letter, letter_rect)
        """ animate the letter by making the tile size slightly bigger and then return to normal"""
        pygame.draw.rect(screen, BACKGROUND_BLACK, self.tile, self.boarder_thickness)
        pygame.display.update()
        self.tile = pygame.Rect((self.x_pos, self.y_pos), (tile_size_x + box_space, tile_size_y + box_space))
        self.tile.center = self.x_pos+(tile_size_x//2), self.y_pos+(tile_size_y//2)
        pygame.draw.rect(screen, self.color, self.tile, self.boarder_thickness)
        pygame.display.update()
        time.sleep(0.05)
        pygame.draw.rect(screen, BACKGROUND_BLACK, self.tile, self.boarder_thickness)
        pygame.display.update()
        self.tile = pygame.Rect((self.x_pos, self.y_pos), self.tile_size)
        pygame.draw.rect(screen, GRAY2, self.tile, self.boarder_thickness)
        pygame.display.update()
        self.empty = False
        # print(f"(The letter {character} has been pressed) " + "Tile Empty: " + str(self.empty))

    def backspace(self):
        letter = self.font.render("    ", True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
        letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
        letter_surface.fill(BACKGROUND_BLACK)
        screen.blit(letter_surface, letter_rect)  # color letter area green for center testing
        screen.blit(letter, letter_rect)
        pygame.draw.rect(screen, self.color, self.tile, self.boarder_thickness)
        pygame.display.update()
        self.empty = True

    def green(self):
        self.color = GREEN
        screen.fill(GREEN, rect=self.tile)
        pygame.display.update()

    def yellow(self):
        self.color = YELLOW
        screen.fill(YELLOW, rect=self.tile)
        pygame.display.update()

    def gray(self):
        screen.fill(GRAY1, rect=self.tile)
        pygame.display.update()

    def animate(self):
        pass


def word_of_the_day():
    with open("word_list.json", "r") as file:
        data = json.load(file)
        word_list = data["word_list"]
        word = word_list[random.randint(0, len(word_list))]
        return word


def evaluate_row(letters):
    print(letter_list)
    if letters[0] == word_of_the_day()[0]:
        pass


def title_bar():
    title_name = "Wordle"
    font_size = 40
    font = pygame.font.Font("KarnakPro-CondensedBlack.otf", font_size)

    bar_line_thickness = 1
    bar_line_height = 50
    line_start_position = (0, bar_line_height)
    line_end_position = (WIN_LENGTH, bar_line_height)

    title_bar_rect = pygame.Rect((0, 0), (WIN_LENGTH, bar_line_height))
    title_bar_rect_center = (title_bar_rect.width//2, title_bar_rect.height//2)

    """render title"""
    title = font.render(title_name, True, WHITE)
    title_rect = title.get_rect(center=title_bar_rect_center)  # get the center of letter
    screen.blit(title, title_rect)

    """render menu button"""
    menu_btn = pygame.image.load("menu_icon.png")
    menu_btn_pos = 60
    menu_btn_rect = pygame.Rect((0, 0), (menu_btn_pos, title_bar_rect.height))
    menu_btn_rect_center_pos = (menu_btn_rect.width//2, menu_btn_rect.height//2)
    menu_btn_center = menu_btn.get_rect(center=menu_btn_rect_center_pos)
    screen.blit(menu_btn, menu_btn_center)

    """render help button"""
    help_btn = pygame.image.load("help_icon.png")
    help_btn_rect = pygame.Rect((0, 0), (menu_btn_pos + 65, title_bar_rect.height))
    help_btn_rect_center_pos = (help_btn_rect.width // 2, help_btn_rect.height // 2)
    help_btn_center = menu_btn.get_rect(center=help_btn_rect_center_pos)
    screen.blit(help_btn, help_btn_center)

    """render settings button"""
    settings_btn = pygame.image.load("settings_icon.png")
    settings_btn_rect = pygame.Rect((0, 0), (menu_btn_pos + 1700, title_bar_rect.height))
    settings_btn_rect_center_pos = (settings_btn_rect.width // 2, settings_btn_rect.height // 2)
    settings_btn_center = menu_btn.get_rect(center=settings_btn_rect_center_pos)
    screen.blit(settings_btn, settings_btn_center)

    """render leaderboard button"""
    leaderboard_btn = pygame.image.load("leaderboard_icon.png")
    leaderboard_btn_rect = pygame.Rect((0, 0), (menu_btn_pos + 1630, title_bar_rect.height))
    leaderboard_btn_rect_center_pos = (leaderboard_btn_rect.width // 2, leaderboard_btn_rect.height // 2)
    leaderboard_btn_center = menu_btn.get_rect(center=leaderboard_btn_rect_center_pos)
    screen.blit(leaderboard_btn, leaderboard_btn_center)

    """title bar is the container for the entire bar but the line is the bar that actually is displayed"""
    # pygame.draw.rect(screen, GREEN, title_bar_rect, bar_line_thickness)
    pygame.draw.line(screen, GRAY1, line_start_position, line_end_position, bar_line_thickness)
    pygame.display.update()

    def tile_bar_menu_pressed():
        pass
    def tile_bar_help_pressed():
        pass
    def tile_bar_data_pressed():
        pass
    def tile_bar_settings_pressed():
        pass
    return bar_line_height


rows = 6
cols = 5
box_space = 6
title_bar_and_board_space = 14
board_height = title_bar() + title_bar_and_board_space
x_position = (WIN_LENGTH//2)-((tile_size_x+box_space)*5)//2
y_position = board_height
board = []
for i in range(rows):
    for j in range(cols):
        tile = Tile((j*(tile_size_x+box_space) + x_position), (i*(tile_size_y+box_space)) + y_position)
        board.append(tile)


# define objects outside the class so that the object state parameter doesn't reset
running = True
alphabet = "abcdefghijklmnopqrstuvwxyz"
curr_tile_index = 0
curr_row = []
index_of_last_in_row = 4
row_len = 4
letter_list = []

title_bar() # init title bar

while running:
    curr_tile = board[curr_tile_index]
    previous_tile = board[curr_tile_index - 1]
    next_tile = board[curr_tile_index + 1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in alphabet and curr_tile_index <= index_of_last_in_row and curr_tile.empty:
                key_pressed = pygame.key.name(event.key).upper()
                curr_tile.display_letter(key_pressed)
                letter_list.append(key_pressed)
                if curr_tile_index != 29:
                    curr_tile_index += 1
                    curr_row.append(curr_tile)
            elif pygame.key.get_pressed()[pygame.K_BACKSPACE] and curr_tile_index != index_of_last_in_row - row_len:
                if curr_tile_index != 29:
                    curr_tile_index -= 1
                    previous_tile.backspace()
                    del curr_row[-1]
                    del letter_list[-1]
                else:
                    pass
            elif len(curr_row)-1 == index_of_last_in_row and pygame.key.get_pressed()[pygame.K_RETURN]:
                evaluate_row(letter_list)
                index_of_last_in_row += row_len + 1
                letter_list.clear()
