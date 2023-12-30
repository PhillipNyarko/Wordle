import sys
import time
import json
import pygame
import random
import svgwrite
import pyautogui
import animations
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
pygame.init()

# global variables
WIN_WIDTH = pyautogui.size()[0] / 1.2
WIN_HEIGHT = pyautogui.size()[1] / 1.2
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
wordle_icon = pygame.image.load("wordle_icon.ico")

# set caption and icon and background color
pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)
SCREEN.fill(BG_BLACK)


def update_display():
    pygame.display.update()


def svg_to_surface(svg_filename):
    try:
        drawing = svgwrite.Drawing(size=('100%', '100%'))
        drawing.add(svgwrite.image.Image(href=svg_filename, size=('100%', '100%')))
        drawing.saveas("temp.svg")

        svg_image = pygame.image.load("temp.svg")
        pygame.image.save(svg_image, "temp.png")  # Convert to PNG

        return pygame.image.load("temp.png")

    except Exception as e:
        print(f"Error loading SVG: {e}")
        return None


def convert_svg_to_png(input_svg, output_png):
    drawing = svg2rlg(input_svg)
    renderPM.drawToFile(drawing, output_png, fmt="PNG")


def render_title_bar():
    input_svg_file = "gear-solid.svg"
    output_png_file = "gear-solid.png"
    convert_svg_to_png(input_svg_file, output_png_file)

    """
    convert_svg_to_png(input_svg_file, output_png_file)
    svg_filename = 'gear-solid.svg'
    icon_surface = svg_to_surface(svg_filename)
    """
    SCREEN.blit(output_png_file, (WIN_WIDTH / 4, WIN_HEIGHT / 2))
    update_display()
    time.sleep(5)


    line_height = WIN_HEIGHT / 19.4
    pygame.draw.line(SCREEN, FULL_TILE_GRAY, (0, line_height), (WIN_WIDTH, line_height))  # render line for bar

    font_size = int(WIN_HEIGHT / 25)
    font = pygame.font.Font("KarnakPro-CondensedBlack.otf", font_size)
    wordle_title = font.render("Wordle", True, WHITE)
    wordle_rect = wordle_title.get_rect(center=(WIN_WIDTH / 2, int(WIN_HEIGHT / 38.04)))  # move by center
    SCREEN.blit(wordle_title, wordle_rect)  # draw wordle title


# define tile size (x,y / width, height) and create game board with child row and tile
class Board:  # Main class that will have a subclass of rows and tiles as child objects
    def __init__(self):  # constructor to initialize the board with its size and location
        self.rows = 6
        self.cols = 5
        self.tile_size = WIN_HEIGHT / 15  # tile size changes based on screen size
        self.tile_spacing = int(
            WIN_HEIGHT / 233.333)  # set spacing between each tile and consider this number when calculating board width
        self.board_x_pos = WIN_WIDTH / 2
        self.board_y_pos = WIN_HEIGHT / 4
        self.board_width = (self.cols * self.tile_spacing + self.tile_size * self.cols) - self.tile_spacing
        self.board_height = (self.rows * self.tile_spacing + self.tile_size * self.rows) - self.tile_spacing
        self.board_rect = pygame.Rect((self.board_x_pos, self.board_y_pos), (self.board_width, self.board_height))
        self.board_rect.center = (WIN_WIDTH / 2, WIN_HEIGHT / 2.5)  # position board in upper center of the screen


class Rows(Board):  # subclass of board class that treats each row of tiles as a singular object
    def __init__(self):
        super(Rows, self).__init__()  # super call to give access to  properties from parent class
        self.row_width = self.board_width
        self.row_height = self.board_height / self.rows
        self.row_x_pos = self.board_rect.x
        self.row_y_pos = self.board_rect.y
        self.row_list = []  # list to hold all the rows

        for i in range(self.rows):  # create row pygame Rect, add to the row list, set y position for each row
            self.row_list.append(pygame.Rect((self.row_x_pos, self.row_y_pos), (self.row_width, self.row_height)))
            self.row_y_pos += self.row_height

        for i in self.row_list:
            i.x = self.board_rect.x  # set the  x position of each row in the row list to match that of the board


class Tiles(Rows):  # subclass object of Rows class
    def __init__(self):
        super(Tiles, self).__init__()

        x_pos_inc = 0
        self.tile_matrix = []

        for i in range(self.rows):  # create a 2d array of tile objects and add them to the tile matrix list
            for j in range(self.cols):
                self.x_pos = self.row_list[i].x + x_pos_inc
                self.y_pos = self.row_list[j].y
                self.tile_thickness = 2  # set tile thickness
                self.tile = pygame.Rect(self.x_pos, self.y_pos, self.tile_size, self.tile_size)  # create tile rect
                self.tile.centery = self.row_list[i].centery
                self.tile_matrix.append(self.tile)
                x_pos_inc += self.tile_size + self.tile_spacing
            x_pos_inc = 0

        for i in self.tile_matrix:
            pygame.draw.rect(SCREEN, TILE_GRAY, i, self.tile_thickness)  # draw the tiles of the grid


class Letters(Tiles):  # subclass of tile class
    def __init__(self):
        super(Letters, self).__init__()
        self.letter_list = []  # list to hold all the letters in the grid

        # initialize letter variables
        self.font_size = int(WIN_HEIGHT / 30)
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)
        self.letter_x = 0
        self.letter_y = 0
        self.letter = None
        self.letter_rect = None

    def render(self):
        super(Letters, self).__init__()

        self.font_size = int(WIN_HEIGHT / 30)
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)

        for index, value in enumerate(self.letter_list):
            self.letter_x = self.tile_matrix[index].x + (self.tile_matrix[index].width / 2)
            self.letter_y = self.tile_matrix[index].y + (self.tile_matrix[index].height / 2)
            self.letter = self.font.render(self.letter_list[index].upper(), True, WHITE)
            self.letter_rect = self.letter.get_rect(center=(self.letter_x, self.letter_y))  # move by center

            if tile_color_values[index] == "Unevaluated":
                SCREEN.fill(BG_BLACK, rect=self.tile_matrix[index])
                pygame.draw.rect(SCREEN, FULL_TILE_GRAY, self.tile_matrix[index], self.tile_thickness)
            elif tile_color_values[index] == "Green":
                SCREEN.fill(GREEN, rect=self.tile_matrix[index])
            elif tile_color_values[index] == "Yellow":
                SCREEN.fill(YELLOW, rect=self.tile_matrix[index])
            elif tile_color_values[index] == "Gray":
                SCREEN.fill(TILE_GRAY, rect=self.tile_matrix[index])

            SCREEN.blit(self.letter, self.letter_rect)  # draw letter

    def clear(self):  # clear the letter in the current tile
        SCREEN.fill(BG_BLACK, rect=self.tile_matrix[len(self.letter_list)])
        pygame.draw.rect(SCREEN, TILE_GRAY, self.tile_matrix[len(self.letter_list)], self.tile_thickness)


with open("word_list.json", "r") as file:  # get the word list from the json file
    data = json.load(file)
    word_list = data["word_list"]


def word_of_the_day():  # function to pick a random word from the word list
    word = word_list[random.randint(0, 2306)]  # word of the day can only be one of the first 2,309 words
    return word


def reset():  # reset all the game elements
    SCREEN.fill(BG_BLACK)
    render_title_bar()
    board.__init__()
    rows.__init__()
    tiles.__init__()
    letters.render()
    update_display()


tile_color_values = ["Unevaluated"] * 30  # list to store the current color values of the tiles. "Unevaluated" = empty


def evaluate_row(user_guess, actual_word, current_row):  # current row returns the number corresponding to the row
    output = ["None"] * tiles.cols
    guess = ''.join(user_guess)
    prev_row_tiles = tiles.tile_matrix[len(letters.letter_list) - 10: len(letters.letter_list) - 5]
    current_row_tiles = tiles.tile_matrix[len(letters.letter_list) - 5: len(letters.letter_list)]
    actual_word_map = {}

    # use a for loop to count how many of each letter is in the word of the day. Keep track of these
    for index, value in enumerate(actual_word):
        if actual_word[index] in actual_word_map:
            actual_word_map[value] += 1
        else:
            actual_word_map[value] = 1
    unchecked = []
    # append the proper color value to the tile color values list based on the wordle game rules
    for index, value in enumerate(actual_word):
        if guess[index] == actual_word[index]:
            output[index] = "Green"
            actual_word_map[value] -= 1
        else:
            unchecked.append(index)
    for index, value in enumerate(unchecked):
        if guess[value] in actual_word_map and actual_word_map[guess[value]] > 0:
            output[value] = "Yellow"
            actual_word_map[guess[value]] -= 1
            unchecked[index] = None
    for index, value in enumerate(unchecked):
        if not unchecked[index] is None:
            output[value] = "Gray"
    del unchecked[:]

    if guess in word_list:  # surprise animation for when the user enters my sisters name.
        if guess == "ezera":
            animations.valid_word_animation(current_row_tiles, output, guess, WIN_HEIGHT)
        animations.valid_word_animation(current_row_tiles, output, user_guess, WIN_HEIGHT)
        for index, value in enumerate(output):  # map color values to grid
            tile_color_values[index + current_row] = output[index]
            letters.render()
        if guess == actual_word:  # animate row if user wins by entering the correct word
            animations.game_won(prev_row_tiles, current_row_tiles, user_guess, tile_color_values, letters.letter_list)
            return "win"
        return "valid"
    else:
        if animations.bad_input_animation(current_row_tiles, guess):  # show bad input animation if word isn't in list
            letters.letter_list.pop()  # backspace one letter if user interrupts animation by pressing backspace
            reset()
        else:
            SCREEN.fill(BG_BLACK)
            reset()


# define objects outside the class so that the object state parameter doesn't reset
running = True
board = Board()
rows = Rows()
tiles = Tiles()
letters = Letters()
last_index_of_row = 5  # holds the index value of the last tile in the row. Increased by 5 after every enter press
wrd_of_the_day = word_of_the_day()
alphabet = "abcdefghijklmnopqrstuvwxyz"

render_title_bar()

while running:
    CLOCK.tick(60)
    for event in pygame.event.get():

        if event.type == pygame.WINDOWSIZECHANGED:  # adjust variables if user decides to play in a different window size
            WIN_WIDTH = pygame.display.get_surface().get_size()[0]
            WIN_HEIGHT = pygame.display.get_surface().get_size()[1]
            SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
            SCREEN.fill(BG_BLACK)
            render_title_bar()
            board.__init__()
            rows.__init__()
            tiles.__init__()
            letters.render()

        if event.type == pygame.KEYDOWN:  # render letter with animations when user presses key
            if pygame.key.name(event.key) in alphabet and len(letters.letter_list) < 30:
                if len(letters.letter_list) < last_index_of_row:
                    letters.letter_list.append(pygame.key.name(event.key))
                    last_tile = tiles.tile_matrix[len(letters.letter_list) - 1]
                    animations.input_animation(last_tile, letters.letter_list[-1], tiles.tile_spacing - 2)
                    letters.render()
            elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:  # remove letter if user presses backspace
                if len(letters.letter_list) > 0 and len(letters.letter_list) > last_index_of_row - tiles.cols:
                    letters.letter_list.pop()
                    letters.clear()
            # evaluate the row and color it correspondingly if user presses enter and the row is filled
            elif pygame.key.get_pressed()[pygame.K_RETURN] and len(letters.letter_list) % 5 == 0:
                if len(letters.letter_list) == last_index_of_row:
                    eval_row = evaluate_row(letters.letter_list[-5:], wrd_of_the_day, last_index_of_row - 5)
                    if eval_row == "win":  # game won
                        time.sleep(1)
                        # Reset the game state
                        letters.letter_list.clear()
                        tile_color_values = ["Unevaluated"] * 30
                        last_index_of_row = 5
                        wrd_of_the_day = word_of_the_day()
                        reset()
                    if eval_row == "valid" and len(letters.letter_list) != 30:  # valid guess
                        last_index_of_row += 5  # go to next row
                    elif eval_row == "valid":  # valid guess but on last row == game over
                        animations.game_lost(tiles.tile_matrix[0:1], wrd_of_the_day)
                        letters.letter_list.clear()
                        tile_color_values = ["Unevaluated"] * 30
                        last_index_of_row = 5
                        wrd_of_the_day = word_of_the_day()
                        reset()
                    # if nothing returned it will stay on this row
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    update_display()
