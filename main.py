import json
import random
import pygame
import time
import animations
from win32api import GetSystemMetrics

pygame.init()

"""look @"""
# global variables
WIN_LENGTH = GetSystemMetrics(0)-GetSystemMetrics(0)//2
WIN_HEIGHT = GetSystemMetrics(0)-((GetSystemMetrics(0)//2)+150)
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))

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

# define tile size (x,y / length, height) and create game tile
tile_size = (61,61)

class Tile:
    def __init__(self, x_pos, y_pos, render=True):
        self.color = TILE_GRAY
        self.tile_thickness = 2
        self.position = x_pos, y_pos
        self.tile_size = (tile_size[0], tile_size[1])
        self.letter_x_pos = self.position[0] + (self.tile_size[0] / 2)
        self.letter_y_pos = self.position[1] + (self.tile_size[1] / 2)
        self.tile = pygame.Rect((self.position[0], self.position[1]), self.tile_size)
        self.font_size = WIN_HEIGHT//20
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)

        """look@"""
        self.render = render
        self.empty = True

        if self.render:
            pygame.draw.rect(SCREEN, self.color, self.tile, self.tile_thickness)
            update_display()

    def display_letter(self, key):
        letter = self.font.render(key, True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # move by center
        SCREEN.blit(letter, letter_rect)
        animations.display_letter(self.tile, self.tile_thickness, self.position, self.tile_size, tile_spacing)
        self.empty = False

    def backspace(self):
        letter = self.font.render("   ", True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
        letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
        letter_surface.fill(BG_BLACK) # fill tile with background color
        SCREEN.blit(letter_surface, letter_rect)
        pygame.draw.rect(SCREEN, self.color, self.tile, self.tile_thickness) #change tile color back
        update_display()
        self.empty = True

    def green(self, key):
       animations.green(key, self.letter_x_pos, self.letter_y_pos, self.position, self.tile_size, self.tile_thickness)

    def yellow(self, key):
        letter = self.font.render(key, True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))
        self.color = YELLOW
        SCREEN.fill(self.color, rect=self.tile)
        SCREEN.blit(letter, letter_rect)
        update_display()

    def gray(self, key):
        letter = self.font.render(key, True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))
        self.color = TILE_GRAY
        SCREEN.fill(self.color, rect=self.tile)
        SCREEN.blit(letter, letter_rect)
        update_display()


def title_bar():

    bar_line_thickness = 1
    bar_line_height = 50
    line_start_position = (0, bar_line_height)
    line_end_position = (WIN_LENGTH, bar_line_height)

    title_bar_rect = pygame.Rect((0, 0), (WIN_LENGTH, bar_line_height))
    title_bar_rect_center = (title_bar_rect.width//2, title_bar_rect.height//2)

    """render title"""
    title = pygame.image.load("wordle_title.png")
    title_rect = title.get_rect(center=title_bar_rect_center)  # get the center of letter
    SCREEN.blit(title, title_rect)

    """render menu button"""
    menu_btn = pygame.image.load("menu_icon.png")
    menu_btn_pos = 60
    menu_btn_rect = pygame.Rect((0, 0), (menu_btn_pos, title_bar_rect.height))
    menu_btn_rect_center_pos = (menu_btn_rect.width//2, menu_btn_rect.height//2)
    menu_btn_center = menu_btn.get_rect(center=menu_btn_rect_center_pos)
    SCREEN.blit(menu_btn, menu_btn_center)

    """render help button"""
    help_btn = pygame.image.load("help_icon.png")
    help_btn_rect = pygame.Rect((0, 0), (menu_btn_pos + 65, title_bar_rect.height))
    help_btn_rect_center_pos = (help_btn_rect.width // 2, help_btn_rect.height // 2)
    help_btn_center = menu_btn.get_rect(center=help_btn_rect_center_pos)
    SCREEN.blit(help_btn, help_btn_center)

    """render settings button"""
    settings_btn = pygame.image.load("settings_icon.png")
    settings_btn_rect = pygame.Rect((0, 0), (WIN_LENGTH*2-50, title_bar_rect.height))
    settings_btn_rect_center_pos = (settings_btn_rect.width // 2, settings_btn_rect.height // 2)
    settings_btn_center = menu_btn.get_rect(center=settings_btn_rect_center_pos)
    SCREEN.blit(settings_btn, settings_btn_center)

    """render leaderboard button"""
    leaderboard_btn = pygame.image.load("leaderboard_icon.png")
    leaderboard_btn_rect = pygame.Rect((0, 0), (WIN_LENGTH*2-120, title_bar_rect.height))
    leaderboard_btn_rect_center_pos = (leaderboard_btn_rect.width // 2, leaderboard_btn_rect.height // 2)
    leaderboard_btn_center = menu_btn.get_rect(center=leaderboard_btn_rect_center_pos)
    SCREEN.blit(leaderboard_btn, leaderboard_btn_center)

    """title bar is the container for the entire bar but the line is the bar that actually is displayed"""
    # pygame.draw.rect(SCREEN, GREEN, title_bar_rect, bar_line_thickness)
    pygame.draw.line(SCREEN, TILE_GRAY, line_start_position, line_end_position, bar_line_thickness)
    update_display()

    def tile_bar_menu_pressed():
        pass

    def tile_bar_help_pressed():
        pass

    def tile_bar_data_pressed():
        pass

    def tile_bar_settings_pressed():
        pass

    tile_bar_menu_pressed()
    tile_bar_help_pressed()
    tile_bar_data_pressed()
    tile_bar_settings_pressed()
    return bar_line_height


with open("word_list.json", "r") as file:
    data = json.load(file)
    word_list = data["word_list"]
    acceptable_words = data["acceptable_input_list"]


def word_of_the_day():
    word = word_list[random.randint(0, len(word_list))].upper()
    return word


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
    inc = 0
    font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)
    final_word = font.render(word, True, "black")
    final_word_rect = final_word.get_rect(center=(WIN_LENGTH // 2, 78))
    bg_rect = pygame.Rect(WIN_LENGTH // 2 - 75, 57, 150, 45)
    animations.fade_in(final_word, final_word_rect, bg_rect)
    animations.fade_out(final_word,final_word_rect, bg_rect)


def end_card(win_num, loss_num):
    inc = 0
    SCREEN.fill((8, 8, 8))
    for x in range(255):
        SCREEN.set_alpha(0)
        inc += 1
        time.sleep(0.09)

    card_length = WIN_LENGTH/2
    card_height = WIN_HEIGHT/2

    end_card_rect = pygame.Rect(card_length-card_length//2, card_height//2.7, card_length, card_height*1.3)
    pygame.draw.rect(SCREEN, BG_BLACK, end_card_rect, 0, border_radius=3)
    local_legnth = end_card_rect.width
    local_height = end_card_rect.height

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 25)

    stats = font.render("Statistics", True, WHITE)
    SCREEN.blit(stats, (local_legnth-stats.get_width()/2, local_height//3.3))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    wins = font.render("Wins", True, WHITE)
    SCREEN.blit(wins, (local_legnth - wins.get_width() / .32, local_height // 2.1))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)

    wins_num = font.render(str(win_num), True, WHITE)
    SCREEN.blit(wins_num, (local_legnth-wins.get_width()/0.35, local_height//2.5))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    losses = font.render("Losses", True, WHITE)
    SCREEN.blit(losses, (local_legnth - losses.get_width() / 2, local_height // 2.1))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)

    losses_num = font.render(str(loss_num), True, WHITE)
    SCREEN.blit(losses_num, (local_legnth-losses_num.get_width()/2, local_height//2.5))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    percent = font.render("Win %", True, WHITE)
    SCREEN.blit(percent, (WIN_LENGTH/1.76, local_height//2.1))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)

    percent_num = font.render(str(round((win_num/(win_num + loss_num)*10), 1)), True, WHITE)
    SCREEN.blit(percent_num, (WIN_LENGTH/1.75, local_height//2.5))

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 12)

    font = pygame.font.Font("NeueHelvetica-Bold.otf", 23)
    nxt_wordle = font.render("NEXT WORDLE", True, WHITE)
    SCREEN.blit(nxt_wordle, (0,0))
    update_display()


num_wins = 8
num_losses = 5
rows = 6
cols = 5
tile_spacing = 6
title_bar_and_board_space = 60
board_height = title_bar() + title_bar_and_board_space # THIS IS INITIALIZING THE TITLE BAR
x_position = (WIN_LENGTH//2)-((tile_size[0]+tile_spacing)*5)//2
y_position = board_height
board = []
for i in range(rows):
    for j in range(cols):
        tile = Tile((j*(tile_size[0]+tile_spacing) + x_position), (i*(tile_size[1]+tile_spacing)) + y_position,)
        board.append(tile)

"render hidden tile and add to the last of the list to avoid index out of bounds error with curr_tile_index += 1"
hidden_last_tile = Tile(588, 399, False)
board.append(hidden_last_tile)

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
    #end_card(num_wins, num_losses)
    curr_tile = board[curr_tile_index]
    previous_tile = board[curr_tile_index - 1]

    if not game_playing:
        end_card(num_wins, num_losses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in alphabet and curr_tile_index <= index_of_last_in_row and curr_tile.empty:
                if game_playing:
                    key_pressed = pygame.key.name(event.key).upper()
                    curr_tile.display_letter(key_pressed)
                    letter_list.append(key_pressed)
                    curr_tile_index += 1
                    curr_row.append(curr_tile)

            elif pygame.key.get_pressed()[pygame.K_BACKSPACE] and curr_tile_index != index_of_last_in_row - row_len:
                if game_playing:
                    previous_tile.backspace()
                    curr_tile_index -= 1
                    del curr_row[-1]
                    del letter_list[-1]

            elif len(curr_row)-1 == index_of_last_in_row and pygame.key.get_pressed()[pygame.K_RETURN]:
                last_five_tiles = curr_row[-5:]
                if evaluate_row(letter_list, last_five_tiles, word_of_the_day) and ''.join(letter_list) == word_of_the_day:
                    """animate right word selected"""
                    time.sleep(1)
                    game_playing = False

                if curr_tile_index != len(board)-1:  # if we are not on the last tile of the entire board
                    if evaluate_row(letter_list, last_five_tiles, word_of_the_day):
                        index_of_last_in_row += row_len + 1  # go to the first tile ond the next line
                        letter_list.clear()  # clear the letter list to keep the list with one word
                        """ animate word inputed"""
                    elif not evaluate_row(letter_list, last_five_tiles, word_of_the_day):
                        pass
                        """ create rects that hold each row and shake the rects"""

                elif curr_tile_index == len(board)-1:  # if we are on the last tile of the board
                    evaluate_row(letter_list, last_five_tiles, word_of_the_day)
                    if evaluate_row(letter_list, last_five_tiles, word_of_the_day) and ''.join(letter_list) != word_of_the_day:
                        print(word_of_the_day)
                        display_word(word_of_the_day)
                        time.sleep(1)
                        game_playing = False
            print(word_of_the_day)
            print(letter_list)




