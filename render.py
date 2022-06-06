import pygame
import animations

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


def show_word(word, screen, win_width):
    word_font = pygame.font.Font("NeueHelvetica-Bold.otf", 20)
    final_word = word_font.render(word, True, "black")
    final_word_rect = final_word.get_rect(center=(win_width / 2, 78))
    bg_rect = pygame.Rect(win_width / 2 - 75, 57, 150, 45)
    animations.fade_in(screen, final_word, final_word_rect, bg_rect)
    animations.fade_out(screen, final_word, final_word_rect, bg_rect)
    return None


def render_title_bar(screen, win_width):
    bar_line_thickness = 1
    bar_line_height = 50
    line_start_position = (0, bar_line_height)
    line_end_position = (win_width, bar_line_height)

    title_bar_rect = pygame.Rect((0, 0), (win_width, bar_line_height))
    title_bar_rect_center = (title_bar_rect.width / 2, title_bar_rect.height / 2)

    """render title"""
    title = pygame.image.load("wordle_title.png")
    title_rect = title.get_rect(center=title_bar_rect_center)  # get the center of letter
    screen.blit(title, title_rect)

    """render menu button"""
    menu_btn = pygame.image.load("menu_icon.png")
    menu_btn_pos = 60
    menu_btn_rect = pygame.Rect((0, 0), (menu_btn_pos, title_bar_rect.height))
    menu_btn_rect_center_pos = (menu_btn_rect.width / 2, menu_btn_rect.height / 2)
    menu_btn_center = menu_btn.get_rect(center=menu_btn_rect_center_pos)
    screen.blit(menu_btn, menu_btn_center)

    """render help button"""
    help_btn = pygame.image.load("help_icon.png")
    help_btn_rect = pygame.Rect((0, 0), (menu_btn_pos + 65, title_bar_rect.height))
    help_btn_rect_center_pos = (help_btn_rect.width / 2, help_btn_rect.height / 2)
    help_btn_center = menu_btn.get_rect(center=help_btn_rect_center_pos)
    screen.blit(help_btn, help_btn_center)

    """render settings button"""
    settings_btn = pygame.image.load("settings_icon.png")
    settings_btn_rect = pygame.Rect((0, 0), (win_width * 2 - 50, title_bar_rect.height))
    settings_btn_rect_center_pos = (settings_btn_rect.width / 2, settings_btn_rect.height / 2)
    settings_btn_center = menu_btn.get_rect(center=settings_btn_rect_center_pos)
    screen.blit(settings_btn, settings_btn_center)

    """render leaderboard button"""
    leaderboard_btn = pygame.image.load("leaderboard_icon.png")
    leaderboard_btn_rect = pygame.Rect((0, 0), (win_width * 2 - 120, title_bar_rect.height))
    leaderboard_btn_rect_center_pos = (leaderboard_btn_rect.width / 2, leaderboard_btn_rect.height / 2)
    leaderboard_btn_center = menu_btn.get_rect(center=leaderboard_btn_rect_center_pos)
    screen.blit(leaderboard_btn, leaderboard_btn_center)

    """title bar is the container for the entire bar but the line is the bar that actually is displayed"""
    # pygame.draw.rect(screen, GREEN, title_bar_rect, bar_line_thickness)
    pygame.draw.line(screen, TILE_GRAY, line_start_position, line_end_position, bar_line_thickness)
    update_display()

    def tile_bar_menu_pressed():
        pass

    def tile_bar_help_pressed():
        pass

    def tile_bar_data_pressed():
        pass

    def tile_bar_settings_pressed():
        pass

    tile_bar_menu_pressed()
    tile_bar_help_pressed()
    tile_bar_data_pressed()
    tile_bar_settings_pressed()
    return bar_line_height
