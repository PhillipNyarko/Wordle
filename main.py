import pygame
import time

# global variables
WIN_LENGTH = 1000
WIN_HEIGHT = 800
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

    def input(self):
        font_size = 43
        font = pygame.font.Font("NeueHelvetica-Bold.otf", font_size)
        letters = {x: pygame.key.key_code(x) for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}  # StackOverFlow w lol
        touch = pygame.key.get_pressed()
        for (character, value) in letters.items():
            if touch[value] and self.tile_empty:
                letter = font.render(character, True, WHITE)
                letter_x_pos = self.x_pos+(self.tile_size[0]//2)
                letter_y_pos = (self.y_pos+(self.tile_size[1]//2))
                letter_rect = letter.get_rect(center=(letter_x_pos, letter_y_pos))  # get the center of letter
                letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
                letter_surface.fill((0, 225, 0))
                # screen.blit(letter_surface, letter_rect)  # color letter area green for center testing
                screen.blit(letter, letter_rect)
                pygame.display.update()
                self.tile_empty = False
                print(f"(The letter {character} has been pressed) " + "Tile Empty: " + str(self.tile_empty))
            elif touch[pygame.K_BACKSPACE]:
                letter = font.render("    ", True, WHITE)
                letter_x_pos = self.x_pos + (self.tile_size[0] // 2)
                letter_y_pos = (self.y_pos + (self.tile_size[1] // 2))
                letter_rect = letter.get_rect(center=(letter_x_pos, letter_y_pos))  # get the center of letter
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


class Wordle:
    def __init__(self):
        self.character = " "
        self.correctness = 0
        self.rows = 5
        self.cols = 6
        self.board = []

    def create_grid(self):
        box_space = 5
        x_pos = (WIN_LENGTH//2)-((tile_size[0]+box_space)*5)//2
        y_pos = (WIN_HEIGHT//2-((tile_size[0]+box_space)*6)//2)-50
        for x in range(self.rows):
            for y in range(self.cols):
                tile = Tile((x*(tile_size[0]+box_space) + x_pos), (y*(tile_size[1]+box_space)) + y_pos)

    def render_grid(self):  # need to get the tile object from the function above
        tile.render()
        tile.input()


# define objects outside the class so that the object state parameter doesn't reset
running = True
wordle = Wordle()
wordle.create_grid()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        else:
            wordle.render_grid()
            pygame.display.update()
