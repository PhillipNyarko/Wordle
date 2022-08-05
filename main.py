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
        pygame.draw.rect(SCREEN, "red", self.board_rect, 3)


class Rows(Board):
    def __init__(self):
        super(Rows, self).__init__()
        self.row_width = self.board_width
        self.row_height = self.board_height / self.rows
        self.row_x_pos = self.board_rect.x
        self.row_y_pos = self.board_rect.y
        self.row_list = []

        for i in range(self.rows):
            self.row_list.append(pygame.Rect((self.row_x_pos, self.row_y_pos), (self.row_width, self.row_height)))
            self.row_y_pos += self.row_height

        for i in self.row_list:
            i.x = self.board_rect.x

        for i in range(self.rows):
            pygame.draw.rect(SCREEN, "green", self.row_list[i], 1)

"""have 5 independent tiles show up in a selected row and inherit a relative x/y position based on the row position SPACING MUST ALSO BE RELATIVE TO THE ROW"""


class Tiles(Rows):
    def __init__(self):
        super(Tiles, self).__init__()

        x_pos_inc = 0
        self.tile_matrix = []

        for i in range(self.rows):
            for j in range(self.cols):
                self.x_pos = self.row_list[i].x + x_pos_inc
                self.y_pos = self.row_list[j].y
                self.tile_thickness = 2
                self.tile = pygame.Rect(self.x_pos, self.y_pos, self.tile_size, self.tile_size)
                self.tile.centery = self.row_list[i].centery
                self.tile_matrix.append(self.tile)
                x_pos_inc += self.tile_size + self.tile_spacing
            x_pos_inc = 0
        for i in self.tile_matrix:
            pygame.draw.rect(SCREEN, "blue", i, self.tile_thickness)

def title_bar():
    return render.render_title_bar(SCREEN, WIN_WIDTH)


def evaluate_row(letters, tiles, word):
    """ use list functions to help with coming up with the logic"""
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
rows = Rows()
tiles = Tiles()

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
            rows.__init__()
            tiles.__init__()

    update_display()
