import pygame

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
        self.empty = True
        self.font_size = 43
        self.font = pygame.font.Font("NeueHelvetica-Bold.otf", self.font_size)
        self.letter_x_pos = self.x_pos + (self.tile_size[0] // 2)
        self.letter_y_pos = (self.y_pos + (self.tile_size[1] // 2))

    def display_letter(self, key):
        letter = self.font.render(key, True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
        letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
        letter_surface.fill((0, 225, 0))
        #screen.blit(letter_surface, letter_rect)  # color letter area green for center testing
        screen.blit(letter, letter_rect)
        pygame.display.update()
        self.empty = False
        # print(f"(The letter {character} has been pressed) " + "Tile Empty: " + str(self.empty))

    def backspace(self):
        letter = self.font.render("    ", True, WHITE)
        letter_rect = letter.get_rect(center=(self.letter_x_pos, self.letter_y_pos))  # get the center of letter
        letter_surface = pygame.Surface(letter.get_size())  # get full unseen area that letter takes up
        letter_surface.fill(BACKGROUND_BLACK)
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
        tile = Tile((j*(tile_size[0]+box_space) + x_position), (i*(tile_size[1]+box_space)) + y_position)
        board.append(tile)


def render_board():
    for index, tiles in enumerate(board):
        tiles.render()


render_board()
# define objects outside the class so that the object state parameter doesn't reset
running = True
alphabet = "abcdefghijklmnopqrstuvwxyz"
inc = 0

while running:
    current_tile = board[inc]
    previous_tile = board[inc-1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in alphabet and inc <= 4:
                key_pressed = pygame.key.name(event.key).upper()
                current_tile.display_letter(key_pressed)
                inc += 1
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                current_tile.green()

            elif pygame.key.get_pressed()[pygame.K_BACKSPACE] and inc != 0:
                inc -= 1
                previous_tile.backspace()
