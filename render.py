import time
import pygame
from win32api import GetSystemMetrics

WIN_LENGTH = GetSystemMetrics(0)-GetSystemMetrics(0)//2
WIN_HEIGHT = GetSystemMetrics(0)-((GetSystemMetrics(0)//2)+150)
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))

pygame.init()
wordle_icon = pygame.image.load("wordle_icon.png")

BACKGROUND_BLACK = (18, 18, 19)

pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)
screen.fill(BACKGROUND_BLACK)
pygame.display.update()
font = pygame.font.Font("NeueHelvetica-Bold.otf", 30)

test_word = font.render("word", True, "black")
test_word_rect = test_word.get_rect(center=(WIN_LENGTH // 2, 78))
bg_rect = pygame.Rect(WIN_LENGTH//2 - 75, 57, 150, 45)


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
