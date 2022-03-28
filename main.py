import pygame

# global variables
WIN_LENGTH = 1000
WIN_HEIGHT = 800
screen = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))

# images
wordle_logo = pygame.image.load("wordle_icon.png")

# initialize and rename
pygame.init()
pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_logo)

# game tile  parameters
rect_length = 62
rect_height = 62
rect_thickness = 1
rect_color = "gray"

# game_tile = pygame.rect(400, 400, rect_length, rect_height)
'''
needs:
return position in array and value(identify letter or empty space)
return correctness value(green, yellow or gray/ right_spot, wrong_spot, not_included)
animation
'''
# create game tile


class GameTile:
    def __init__(self, length, height, thickness, color, position, value, surface):
        self.length = rect_length
        self.height = rect_height
        self.thickness = rect_thickness
        self.color = rect_color
        self.position = 0
        self.value = 0

    def create_game_tile(self):
        pass

    def right_spot(self):
        pass

    def wrong_spot(self):
        pass

    def not_included(self):
        pass

print("hello world.")
# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # results in clean exit
            pygame.quit()
