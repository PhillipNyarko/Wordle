import time

import pygame
from win32api import GetSystemMetrics

# global variables
WIN_LENGTH = GetSystemMetrics(0)-GetSystemMetrics(0)//3
WIN_HEIGHT = GetSystemMetrics(0)-((GetSystemMetrics(0)//2)+50)
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
tile_size_x = WIN_HEIGHT//12
tile_size_y = WIN_HEIGHT//12


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
        letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
        letter_surface.fill((0, 225, 0))
        screen.blit(letter_surface, letter_rect)  # color letter area green for center testing
        screen.blit(letter, letter_rect)

        pygame.draw.rect(screen, BACKGROUND_BLACK, self.tile, self.boarder_thickness)
        pygame.display.update()

        self.tile = pygame.Rect((self.x_pos, self.y_pos), (tile_size_x + box_space, tile_size_y + box_space))
        self.tile.center = self.x_pos+(tile_size_x//2), self.y_pos+(tile_size_y//2)
        pygame.draw.rect(screen, self.color, self.tile, self.boarder_thickness)
        pygame.display.update()
        time.sleep(0.1)

        pygame.draw.rect(screen, BACKGROUND_BLACK, self.tile, self.boarder_thickness)
        pygame.display.update()

        self.tile = pygame.Rect((self.x_pos, self.y_pos), self.tile_size)
        pygame.draw.rect(screen, self.color, self.tile, self.boarder_thickness)
        pygame.display.update()
        self.empty = False
        return key
        # print(f"(The letter {character} has been pressed) " + "Tile Empty: " + str(self.empty))

    def backspace(self):
        letter = self.font.render("    ", True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
        letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
        letter_surface.fill("red")
        screen.blit(letter_surface, letter_rect)  # color letter area green for center testing
        screen.blit(letter, letter_rect)
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


rows = 6
cols = 5
box_space = 5
x_position = (WIN_LENGTH//2)-((tile_size_x+box_space)*5)//2
y_position = (WIN_HEIGHT//2-((tile_size_y+box_space)*6)//2)-50
board = []
for i in range(rows):
    for j in range(cols):
        tile = Tile((j*(tile_size_x+box_space) + x_position), (i*(tile_size_y+box_space)) + y_position)
        board.append(tile)


def evaluate_row(tile_list):
    word = "weary"
    """
    for _ in tile_list:
        if tile.display_letter() in word.lower() and rightspot():
            tile.green()
    """


# define objects outside the class so that the object state parameter doesn't reset
running = True
alphabet = "abcdefghijklmnopqrstuvwxyz"
current_tile_index = 0
curr_row = []
index_of_last_in_row = 4
row_len = 4

while running:
    current_tile = board[current_tile_index]
    previous_tile = board[current_tile_index-1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in alphabet and current_tile_index <= index_of_last_in_row:
                key_pressed = pygame.key.name(event.key).upper()
                current_tile.display_letter(key_pressed)
                current_tile_index += 1
                curr_row.append(current_tile)
            elif pygame.key.get_pressed()[pygame.K_BACKSPACE] and current_tile_index != index_of_last_in_row - row_len:
                current_tile_index -= 1
                previous_tile.backspace()
                del curr_row[-1]
            elif len(curr_row)-1 == index_of_last_in_row and pygame.key.get_pressed()[pygame.K_RETURN]:
                last_five = curr_row[-5:]
                evaluate_row(last_five)
                index_of_last_in_row += row_len + 1
