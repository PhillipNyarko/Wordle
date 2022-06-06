import json
import random
import pygame
import time
import render
import animations
from win32api import GetSystemMetrics

pygame.init()

'''
MAKE BOARD RENDER IN THE MIDDLE
MAKE WINDOW RESIZING WORK
MAKE TILE CHANGE SIZE BASED ON WINDOW SIZE
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


# define tile size (x,y / width, height) and create game tile MY PRIDE AND JOY
tile_size = 62
tile_x = WIN_WIDTH/tile_size
tile_y = WIN_HEIGHT/tile_size
tile_spacing = 40
tile_dimension = (int(WIN_WIDTH/tile_x), int(WIN_HEIGHT/tile_y))
print(tile_dimension)

rows = 6
cols = 5


class Board:
    board_x = WIN_WIDTH/2
    board_y = WIN_HEIGHT/4
    board_rect = pygame.Rect((board_x, board_y), ((cols*tile_spacing+tile_size*cols)-tile_spacing, (rows*tile_spacing+tile_size*rows)-tile_spacing))
    board_rect.center = WIN_WIDTH/2, WIN_HEIGHT/2.5
    pygame.draw.rect(SCREEN, "yellow", board_rect, 1)
    pygame.display.update()

    class Row:
        row_x = WIN_WIDTH / 2
        row_y = WIN_HEIGHT / 4
        row_rect = pygame.Rect((100,100), ((cols*tile_spacing+tile_size*cols)-tile_spacing, tile_size))
        row_rect.center = WIN_WIDTH / 2, 125
        pygame.draw.rect(SCREEN, "pink", row_rect, 3)
        pygame.display.update()

        class Tile:
            def __init__(self, board_x, board_y):
                self.color = TILE_GRAY
                self.empty = True
                self.tile_thickness = 2
                self.position = board_x, board_y
                self.tile_dimension = (tile_dimension[0], tile_dimension[1])
                self.letter_pos = (self.position[0] + (self.tile_dimension[0]/2), self.position[1] + (self.tile_dimension[1]/2))
                self.tile = pygame.Rect((self.position[0], self.position[1]), self.tile_dimension)
                self.font_size = int(WIN_HEIGHT/30)
                self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)

                pygame.draw.rect(SCREEN, self.color, self.tile, self.tile_thickness)
                pygame.draw.line(SCREEN, "green", (self.position[0]+tile_size/2, self.position[1]+tile_size), (self.position[0]+tile_size/2, 0))
                update_display()

            def display_letter(self, key):
                letter = self.font.render(key, True, WHITE)
                letter_rect = letter.get_rect(center=(self.letter_pos[0], self.letter_pos[1]))  # move by center
                SCREEN.blit(letter, letter_rect)
                animations.display_letter(SCREEN, self.tile, self.tile_thickness, self.position, self.tile_dimension, tile_spacing)
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


board = []
for i in range(rows):
    for j in range(cols):
        tile = Board.Row.Tile((j*(tile_size+tile_spacing) + Board.board_rect.topleft[0]), (i*(tile_size+tile_spacing)) + Board.board_rect.topleft[1])
        board.append(tile)

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


def end_card(win_num, loss_num):
    inc = 0
    SCREEN.fill((8, 8, 8))
    for x in range(255):
        SCREEN.set_alpha(0)
        inc += 1
        time.sleep(0.09)

    card_width = WIN_WIDTH/2
    card_height = WIN_HEIGHT/2

    end_card_rect = pygame.Rect(card_width-card_width/2, card_height/2.7, card_width, card_height*1.3)
    pygame.draw.rect(SCREEN, BG_BLACK, end_card_rect, 0, border_radius=3)
    local_width = end_card_rect.width
    local_height = end_card_rect.height

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 25)

    stats = font.render("Statistics", True, WHITE)
    SCREEN.blit(stats, (local_width-stats.get_width()/2, local_height/3.3))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    wins = font.render("Wins", True, WHITE)
    SCREEN.blit(wins, (local_width - wins.get_width() / .32, local_height / 2.1))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)

    wins_num = font.render(str(win_num), True, WHITE)
    SCREEN.blit(wins_num, (local_width-wins.get_width()/0.35, local_height/2.5))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    losses = font.render("Losses", True, WHITE)
    SCREEN.blit(losses, (local_width - losses.get_width() / 2, local_height / 2.1))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)

    losses_num = font.render(str(loss_num), True, WHITE)
    SCREEN.blit(losses_num, (local_width-losses_num.get_width()/2, local_height/2.5))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    percent = font.render("Win %", True, WHITE)
    SCREEN.blit(percent, (WIN_WIDTH/1.76, local_height/2.1))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)

    percent_num = font.render(str(round((win_num/(win_num + loss_num)*10), 1)), True, WHITE)
    SCREEN.blit(percent_num, (WIN_WIDTH/1.75, local_height/2.5))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 23)
    nxt_wordle = font.render("NEXT WORDLE", True, WHITE)
    SCREEN.blit(nxt_wordle, (0,0))
    update_display()


with open("word_list.json", "r") as file:
    data = json.load(file)
    word_list = data["word_list"]
    acceptable_words = data["acceptable_input_list"]


def word_of_the_day():
    word = word_list[random.randint(0, len(word_list))].upper()
    return word


num_wins = 8
num_losses = 5

# define objects outside the class so that the object state parameter doesn't reset
running = True
alphabet = "abcdefghijklmnopqrstuvwxyz"
curr_tile_index = 0
curr_row = []
index_of_last_in_row = 4
row_len = 4
letter_list = []
last_tile = len(board)-1
word_of_the_day = word_of_the_day()
game_playing = True

while running:
    # end_card(num_wins, num_losses)
    curr_tile = board[curr_tile_index]
    previous_tile = board[curr_tile_index - 1]
    title_bar()
    if not game_playing:
        end_card(num_wins, num_losses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in alphabet and curr_tile_index <= index_of_last_in_row and curr_tile.empty:
                if game_playing:
                    if curr_tile != board[-1]:
                        key_pressed = pygame.key.name(event.key).upper()
                        curr_tile.display_letter(key_pressed)
                        letter_list.append(key_pressed)
                        curr_tile_index += 1
                        curr_row.append(curr_tile)
                    else:
                        key_pressed = pygame.key.name(event.key).upper()
                        curr_tile.display_letter(key_pressed)
                        letter_list.append(key_pressed)
                        curr_row.append(curr_tile)
            elif pygame.key.get_pressed()[pygame.K_BACKSPACE] and curr_tile_index != index_of_last_in_row - row_len:
                if game_playing:
                    if curr_tile != board[-1]:
                        previous_tile.backspace()
                        curr_tile_index -= 1
                        del curr_row[-1]
                        del letter_list[-1]
                    else:
                        previous_tile.backspace()
                        del curr_row[-1]
                        del letter_list[-1]

            elif len(curr_row)-1 == index_of_last_in_row and pygame.key.get_pressed()[pygame.K_RETURN]:
                last_five_tiles = curr_row[-5:]
                row_value = evaluate_row(letter_list, last_five_tiles, word_of_the_day)
                if row_value and ''.join(letter_list) == word_of_the_day:
                    """animate right word selected"""
                    time.sleep(1)
                    game_playing = False

                if curr_tile_index != len(board)-1:  # if we are not on the last tile of the entire board
                    if row_value:
                        index_of_last_in_row += row_len + 1  # go to the first tile ond the next line
                        letter_list.clear()  # clear the letter list to keep the list with one word
                        """ animate word inputed"""
                    elif not row_value:
                        pass
                        """ create rects that hold each row and shake the rects"""

                elif curr_tile_index == len(board)-1:  # if we are on the last tile of the board
                    if row_value and ''.join(letter_list) != word_of_the_day:
                        display_word(word_of_the_day)
                        time.sleep(1)
                        game_playing = False
            print(word_of_the_day)
            print(letter_list)
        pygame.draw.line(SCREEN, "red", (WIN_WIDTH / 2, 0), (WIN_WIDTH / 2, WIN_HEIGHT))
        pygame.draw.line(SCREEN, "red", (0, WIN_HEIGHT / 2), (WIN_WIDTH, WIN_HEIGHT / 2))
        pygame.display.update()

