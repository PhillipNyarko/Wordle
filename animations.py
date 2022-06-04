import time
import pygame
from win32api import GetSystemMetrics

WIN_LENGTH = GetSystemMetrics(0)-GetSystemMetrics(0)//2
WIN_HEIGHT = GetSystemMetrics(0)-((GetSystemMetrics(0)//2)+150)
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))

pygame.init()

wordle_icon = pygame.image.load("wordle_icon.png")

WHITE = (225, 225, 225)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)

pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)
screen.fill(BG_BLACK)
pygame.display.update()
font = pygame.font.Font("NeueHelvetica-Bold.otf", 30)

test_word = font.render("word", True, "black")
test_word_rect = test_word.get_rect(center=(WIN_LENGTH // 2, 78))
bg_rect = pygame.Rect(WIN_LENGTH//2 - 75, 57, 150, 45)


def update_display():
    pygame.display.update()


def fade_in(word, word_rect, surface):
    inc = 18
    for x in range(237):
        color = pygame.Color(inc, inc, inc)
        pygame.draw.rect(screen, color, surface, 0, border_radius=3)
        screen.blit(word, word_rect)
        pygame.display.update()
        inc += 1


def fade_out(word, word_rect, surface):
    inc = 255
    for x in range(238):
        color = pygame.Color(inc, inc, inc)
        pygame.draw.rect(screen, color, surface, 0, border_radius=3)
        screen.blit(word, word_rect)
        pygame.display.update()
        inc -= 1


def display_letter(tile, tile_thickness, position, tile_size, box_space):
    """ animate the letter by making the tile size slightly bigger and then return to normal"""
    x_pos = position[0]
    y_pos = position[1]
    pygame.draw.rect(screen, BG_BLACK, tile, tile_thickness)
    update_display()

    tile = pygame.Rect((x_pos, y_pos), (tile_size[0] + box_space, tile_size[1] + box_space))
    tile.center = x_pos + (tile_size[0] // 2), y_pos + (tile_size[1] // 2)
    pygame.draw.rect(screen, TILE_GRAY, tile, tile_thickness)
    update_display()
    time.sleep(0.05)

    pygame.draw.rect(screen, BG_BLACK, tile, tile_thickness)
    update_display()

    tile = pygame.Rect((x_pos, y_pos), (tile_size[0], tile_size[1]))
    pygame.draw.rect(screen, FULL_TILE_GRAY, tile, tile_thickness)
    update_display()

