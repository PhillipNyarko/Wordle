import json
import random
import pygame
import time
import render
import animations
from win32api import GetSystemMetrics

pygame.init()

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
        self.tile_spacing = WIN_WIDTH/207.27
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
""" set up all the proper tile inputs evals and animations"""


class Letter(Tiles):
    def __init__(self):
        super(Letter, self).__init__()
        self.letter_list = []

        self.font_size = int(WIN_HEIGHT / 30)
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)
        self.letter_x = 0
        self.letter_y = 0
        self.letter = None
        self.letter_rect = None

    def render(self):
        super(Letter, self).__init__()
        self.font_size = int(WIN_HEIGHT / 30)
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)
        for index, value in enumerate(self.letter_list):
            self.letter_x = self.tile_matrix[index].x + (self.tile_matrix[index].width/2)
            self.letter_y = self.tile_matrix[index].y + (self.tile_matrix[index].height/2)
            self.letter = self.font.render(self.letter_list[index].upper(), True, WHITE)
            self.letter_rect = self.letter.get_rect(center=(self.letter_x, self.letter_y))  # move by center
            SCREEN.blit(self.letter, self.letter_rect)

    def clear(self):
        pygame.draw.rect(SCREEN, "red", self.tile_matrix[len(self.letter_list)], width=0)

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
letters = Letter()
last_index_of_row = 5  # holds the index value of the last tile in the row. Increased by 5 after every enter press

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
            letters.render()

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in alphabet and len(letters.letter_list) < 30:
                if len(letters.letter_list) < last_index_of_row:
                    letters.letter_list.append(pygame.key.name(event.key))
                    letters.render()

            if pygame.key.get_pressed()[pygame.K_RETURN] and len(letters.letter_list) % 5 == 0:
                if len(letters.letter_list) < 30 and len(letters.letter_list) == last_index_of_row:
                    last_index_of_row += 5
                    print(last_index_of_row)

            if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                if len(letters.letter_list) > 0:
                    letters.letter_list.pop()
                    letters.clear()

            print(letters.letter_list)
    update_display()
