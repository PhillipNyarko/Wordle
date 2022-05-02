import pygame
# import time

# global variables
WIN_LENGTH = 1000
WIN_HEIGHT = 800
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

'''
needs:
return position in array and value(identify letter or empty space)
return correctness value(green, yellow or gray/ right_spot, wrong_spot, not_included)
animation
'''

# create game tile
tile_size = (62, 62)


class Tile:
    def __init__(self, x_pos, y_pos):
        self.color = GRAY1
        self.tile_size = tile_size
        self.boarder_thickness = 2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile = pygame.Rect((x_pos, y_pos), self.tile_size)
        self.tile_empty = True
        self.letter_x_pos = self.x_pos + (self.tile_size[0] // 2)
        self.letter_y_pos = (self.y_pos + (self.tile_size[1] // 2))

    def input(self):
        font_size = 43
        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)
        letters = {x: pygame.key.key_code(x) for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}  # StackOverFlow w lol
        touch = pygame.key.get_pressed()  # going to have to change the way that I ge t the key input a little because its looping iof you hold backspace down ill figure it out.
        for (character, value) in letters.items():
            if touch[value] and self.tile_empty:
                letter = font.render(character, True, WHITE)
                letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
                letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
                letter_surface.fill((0, 225, 0))
                # screen.blit(letter_surface, letter_rect)  # color letter area green for center testing
                screen.blit(letter, letter_rect)
                pygame.display.update()
                self.tile_empty = False
                print(f"(The letter {character} has been pressed) " + "Tile Empty: " + str(self.tile_empty))
            elif touch[pygame.K_BACKSPACE] and not self.tile_empty:
                letter = font.render("    ", True, BACKGROUND_BLACK)
                letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
                letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
                letter_surface.fill(BACKGROUND_BLACK)
                screen.blit(letter_surface, letter_rect)  # color letter area green for center testing
                screen.blit(letter, letter_rect)
                pygame.display.update()
                self.tile_empty = True
                print("backspace pressed " + "Tile Empty: " + str(self.tile_empty))
        return self.tile_empty

    def green(self):
        self.color = GREEN
        screen.fill(GREEN, rect=self.tile)

    def yellow(self):
        self.color = YELLOW
        screen.fill(YELLOW, rect=self.tile)

    def gray(self):
        screen.fill(GRAY1, rect=self.tile)

    def render(self):
        pygame.draw.rect(screen, self.color, self.tile, self.boarder_thickness)
        pygame.display.update()


rows = 6
cols = 5
box_space = 5
x_position = (WIN_LENGTH//2)-((tile_size[0]+box_space)*5)//2
y_position = (WIN_HEIGHT//2-((tile_size[0]+box_space)*6)//2)-50
board = []
for i in range(rows):
    for j in range(cols):
        tile = Tile((j * (tile_size[0] + box_space) + x_position), (i * (tile_size[1] + box_space)) + y_position)
        board.append(tile)


def render_board():
    for index, tiles in enumerate(board):
        tiles.render()


def accept_board_input():
    for index, tiles in enumerate(board):
        tiles.input()


# define objects outside the class so that the object state parameter doesn't reset
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        else:
            render_board()
            accept_board_input()
