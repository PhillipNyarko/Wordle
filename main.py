import pygame
import time

# global variables
WIN_LENGTH = 1000
WIN_HEIGHT = 800
screen = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))

# colors
WHITE = (225, 225, 225)
GRAY1 = (58, 58, 60)
GRAY2 = (86, 87, 88)
GRAY3 = (129, 131, 132)
# images
wordle_icon = pygame.image.load("wordle_icon.png")

# initialize and rename
pygame.init()
pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)

'''
needs:
return position in array and value(identify letter or empty space)
return correctness value(green, yellow or gray/ right_spot, wrong_spot, not_included)
animation
'''

# create game tile


class Tile:
    def __init__(self, x_pos, y_pos):
        self.color = (58, 58, 60)
        self.tile_size = (62, 62)
        self.boarder_thickness = 2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile = pygame.Rect((x_pos, y_pos), self.tile_size)
        self.tile_empty = True

    def input(self):
        font_size = 43
        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)
        letters = {x: pygame.key.key_code(x) for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}  # StackOverFlow w lol
        touch = pygame.key.get_pressed()
        for (letter, value) in letters.items():
            if touch[value]:
                print(f"(The letter {letter} has been pressed)")
                letter = font.render(letter, True, WHITE)
                letter_x_pos = self.x_pos+(self.tile_size[0]//2)
                letter_y_pos = (self.y_pos+(self.tile_size[1]//2))
                letter_rect = letter.get_rect(center=(letter_x_pos, letter_y_pos))  # get the center of letter
                letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
                letter_surface.fill((0, 225, 0))  # color area green for center testing
                screen.blit(letter_surface, letter_rect)
                screen.blit(letter, letter_rect)
                pygame.display.update()
            elif touch[pygame.K_BACKSPACE]:
                print("backspace pressed")
                screen.fill("black")
                pygame.display.update()

    def render(self):
        pygame.draw.rect(screen, self.color, self.tile, self.boarder_thickness)
        pygame.display.update()


class Wordle:
    def __init__(self):
        self.character = " "
        self.correctness = 0
        self.rows = 5
        self.cols = 6
        self.board = []

    def create_board(self):
        x_pos = 100
        y_pos = 140
        self.rows, self.cols = (6, 5)
        for x in range(self.cols):
            board = [(x_pos, y_pos) * self.rows] * self.cols
            x_pos += 80
            y_pos += 80
            print(board)
            test_tile = Tile(x_pos, y_pos)
            test_tile.input()
            test_tile.render()
            time.sleep(1)
"""
w = Wordle()
w.create_board()
"""
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        else:
            test_tile = Tile(400, 400)
            test_tile.input()
            test_tile.render()
