import json
import random
import pygame
import time
import render
import animations
from win32api import GetSystemMetrics

pygame.init()

'''
MAKE WINDOW RESIZING WORK
MAKE TILE and tile spacing CHANGE SIZE BASED ON WINDOW SIZE
MAKE WORD TEXT CHANGE TO THE RIGHT SIZE BASED ON TILE SIZ3E
set the minimum window size to the with of all the items in the title bar
fix when you change the window size you loose all the previous tile
fix if you type a little bit of the word and then move the window and then press enter it renders at the old position
clean exit
'''
# global variables
WIN_WIDTH = GetSystemMetrics(0)/1.1
WIN_HEIGHT = GetSystemMetrics(1)/1.1
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)

# colors
WHITE = (225, 225, 225)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)

# icon image
wordle_icon = pygame.image.load("wordle_icon.png")

# set caption and icon and background color
pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)
SCREEN.fill(BG_BLACK)


def update_display():
    pygame.display.update()


# define tile size (x,y / width, height) and create game board with child row and tile
class Board:
    def __init__(self):
        self.rows = 6
        self.cols = 5
        self.tile_size = WIN_HEIGHT/15
        self.tile_spacing = 6
        self.board_x_pos = WIN_WIDTH / 2
        self.board_y_pos = WIN_HEIGHT / 4
        self.board_width = (self.cols * self.tile_spacing + self.tile_size * self.cols) - self.tile_spacing
        self.board_height = (self.rows * self.tile_spacing + self.tile_size * self.rows) - self.tile_spacing
        self.board_rect = pygame.Rect((self.board_x_pos, self.board_y_pos), (self.board_width, self.board_height))
        self.board_rect.center = (WIN_WIDTH / 2, WIN_HEIGHT / 2.5)
        pygame.draw.rect(SCREEN, "yellow", self.board_rect, 1)


class Row(Board):
    def __init__(self):
        super(Row, self).__init__()
        for i in range(self.rows):
            self.row_rect = pygame.Rect((self.board_x_pos, self.board_y_pos), (self.board_width, self.board_height/self.rows))
        self.row_rect.x = self.board_rect.x
        pygame.draw.rect(SCREEN, "blue", self.row_rect, 1)



class Tile(Row):
    def __init__(self, x_pos, y_pos):
        self.color = TILE_GRAY
        self.empty = True
        self.tile_thickness = 2
        self.position = x_pos, y_pos
        self.tile_dimension = (x_pos, y_pos)
        self.letter_pos = (self.position[0] + (x_pos/2), self.position[1] + (y_pos/2))
        self.tile = pygame.Rect((self.position[0], self.position[1]), (x_pos, y_pos))
        self.font_size = int(WIN_HEIGHT/30)
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)

        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(SCREEN, self.color, self.tile, self.tile_thickness)
                update_display()

    def display_letter(self, key):
        letter = self.font.render(key, True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_pos[0], self.letter_pos[1]))  # move by center
        SCREEN.blit(letter, letter_rect)
        animations.display_letter(SCREEN, self.tile, self.tile_thickness, self.position, self.tile_dimension, self.tile_spacing)
        self.empty = False

    def backspace(self):
        letter = self.font.render("    ", True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_pos[0], self.letter_pos[1]))  # get the center of letter
        letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
        letter_surface.fill(BG_BLACK)  # fill tile with background color
        SCREEN.blit(letter_surface, letter_rect)
        pygame.draw.rect(SCREEN, self.color, self.tile, self.tile_thickness)  # change tile color back
        update_display()
        self.empty = True

    def green(self, key):
        animations.animate_tile(SCREEN, key, self.letter_pos, self.position, self.tile_dimension, self.tile_thickness, GREEN)

    def yellow(self, key):
        animations.animate_tile(SCREEN, key, self.letter_pos, self.position, self.tile_dimension, self.tile_thickness, YELLOW)

    def gray(self, key):
        animations.animate_tile(SCREEN, key, self.letter_pos, self.position, self.tile_dimension, self.tile_thickness, TILE_GRAY)


def title_bar():
    return render.render_title_bar(SCREEN, WIN_WIDTH)


def evaluate_row(letters, tiles, word):
    inc = 0
    guess = ''.join(letters)

    if guess.lower() in acceptable_words or guess.lower() in word_list:

        for x in range(5):
            if guess[inc] == word[inc]:
                tiles[inc].green(guess[inc])
            if guess[inc] != word[inc] and guess[inc] in word:
                tiles[inc].yellow(guess[inc])
            if guess[inc] not in word:
                tiles[inc].gray(guess[inc])
            inc += 1
        in_word_list = True
        return in_word_list
    else:
        display_word("not in word list")
        print("not in word list")
        in_word_list = False
        return in_word_list


def display_word(word):
    render.show_word(word, SCREEN, WIN_WIDTH)


with open("word_list.json", "r") as file:
    data = json.load(file)
    word_list = data["word_list"]
    acceptable_words = data["acceptable_input_list"]


def word_of_the_day():
    word = word_list[random.randint(0, len(word_list))].upper()
    return word


# define objects outside the class so that the object state parameter doesn't reset
running = True
alphabet = "abcdefghijklmnopqrstuvwxyz"
word_of_the_day = word_of_the_day()
board = Board()
r = Row()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            WIN_WIDTH = pygame.display.get_surface().get_size()[0]
            WIN_HEIGHT = pygame.display.get_surface().get_size()[1]
            SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
            SCREEN.fill(BG_BLACK)
            board.__init__()
            r.__init__()

    pygame.display.update()

