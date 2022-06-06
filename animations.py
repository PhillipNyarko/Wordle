import pygame
import time

pygame.init()

WHITE = (225, 225, 225)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)
font = pygame.font.Font("NeueHelvetica-Bold.otf", 30)


def update_display():
    pygame.display.update()


def fade_in(screen, word, word_rect, surface):
    inc = 18
    for x in range(237):
        color = pygame.Color(inc, inc, inc)
        pygame.draw.rect(screen, color, surface, 0, border_radius=3)
        screen.blit(word, word_rect)
        pygame.display.update()
        inc += 1


def fade_out(screen, word, word_rect, surface):
    inc = 255
    for x in range(238):
        color = pygame.Color(inc, inc, inc)
        pygame.draw.rect(screen, color, surface, 0, border_radius=3)
        screen.blit(word, word_rect)
        pygame.display.update()
        inc -= 1


def display_letter(screen, tile, tile_thickness, position, tile_size, box_space):
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


def animate_tile(screen, key, letter_pos, position, tile_size, tile_thickness, color):
    letter = font.render(key, True, WHITE)
    letter_rect = letter.get_rect(center=(letter_pos[0], letter_pos[1]))
    x_pos = position[0]
    y_pos = position[1]

    change_rate = 0
    speed = 0.0011
    for x in range(tile_size[0]):
        tile = pygame.Rect((x_pos, y_pos), tile_size)
        tile.inflate_ip(0, change_rate)
        pygame.draw.rect(screen, TILE_GRAY, tile, tile_thickness)
        update_display()
        time.sleep(speed)
        pygame.draw.rect(screen, BG_BLACK, tile, tile_thickness)
        update_display()
        change_rate -= 2
    for x in range(tile_size[0]):
        tile = pygame.Rect((x_pos, y_pos), tile_size)
        tile.inflate_ip(0, change_rate)
        pygame.draw.rect(screen, color, tile, tile_thickness)
        update_display()
        time.sleep(speed)
        change_rate += 2

    screen.blit(letter, letter_rect)
