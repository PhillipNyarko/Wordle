import pygame
import time
from math import*
from win32api import GetSystemMetrics


pygame.init()

# global variables
CLOCK = pygame.time.Clock()
WIN_WIDTH = 800  # GetSystemMetrics(0)/1.1
WIN_HEIGHT = 800  # GetSystemMetrics(1)/1.1
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
tile_thickness = 2

# colors
WHITE = (225, 225, 225)
BG_BLACK = (18, 18, 19)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
TILE_GRAY = (58, 58, 60)
FULL_TILE_GRAY = (86, 87, 88)


def update_display():
    pygame.display.update()


def fade_rect_in():
    pass


def fade_rect_out():
    pass


def animate_not_in_word_list():
    pass


def game_won():
    pass


""" ANIMATE ROW """

projection_matrix = [[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 0]]

cube_points = [n for n in range(8)]

cube_points[0] = [[-1], [-1], [1]]
cube_points[1] = [[1], [-1], [1]]
cube_points[2] = [[1], [1], [1]]
cube_points[3] = [[-1], [1], [1]]
cube_points[4] = [[-1], [-1], [-1]]
cube_points[5] = [[1], [-1], [-1]]
cube_points[6] = [[1], [1], [-1]]
cube_points[7] = [[-1], [1], [-1]]


def multiply_matrix(a, b):
    a_rows = len(a)
    a_cols = len(a[0])

    b_rows = len(b)
    b_cols = len(b[0])

    product = [[0 for _ in range(b_cols)]for _ in range(a_rows)]

    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        print("INCOMPATIBLE MATRIX SIZES")
    return product


def connect_points(i, j, points):
    pygame.draw.line(SCREEN, (255, 255, 255), (points[i][0], points[i][1]), (points[j][0], points[j][1]))


running = True

SCALE = 100
angle_x = angle_y = angle_z = 0

while running:
    CLOCK.tick(60)
    SCREEN.fill((0, 0, 0))

    rotation_x = [[1, 0, 0],
                  [0, cos(angle_x), -sin(angle_x)],
                  [0, sin(angle_x), cos(angle_x)]]

    rotation_y = [[cos(angle_y), 0, sin(angle_y)],
                  [0, 1, 0],
                  [-sin(angle_y), 0, cos(angle_y)]]

    rotation_z = [[cos(angle_z), -sin(angle_z), 0],
                  [sin(angle_z), cos(angle_z), 0],
                  [0, 0, 1]]
    angle_x += 0.01
    angle_y += 0.01
    angle_z += 0.01

    points = [0 for _ in range(len(cube_points))]
    i = 0
    for point in cube_points:
        rotate_x = multiply_matrix(rotation_x, point)
        rotate_y = multiply_matrix(rotation_y, rotate_x)
        rotate_z = multiply_matrix(rotation_z, rotate_y)
        point_2d = multiply_matrix(projection_matrix, rotate_z)

        x = point_2d[0][0] * SCALE + WIN_WIDTH/2
        y = point_2d[1][0] * SCALE + WIN_HEIGHT/2

        points[i] = (x, y)
        i += 1
        pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), 5)

    connect_points(0, 1, points)
    connect_points(0, 3, points)
    connect_points(0, 4, points)
    connect_points(1, 2, points)
    connect_points(1, 5, points)
    connect_points(2, 6, points)
    connect_points(2, 3, points)
    connect_points(3, 7, points)
    connect_points(4, 5, points)
    connect_points(4, 7, points)
    connect_points(6, 5, points)
    connect_points(6, 7, points)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

    update_display()
