import game_state
import node
import snake_grid
import text
from game_state import GameState
from button import *
import pygame


SPEEDS = [0.3, 0.15, 0.08]
SPEEDS_NAME = ["Facile", "Normal", "Difficile"]


class CustomizeState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()
        self.grid_width = snake_grid.GRID_WIDTH
        self.grid_height = snake_grid.GRID_HEIGHT
        self.speed = SPEEDS[1]

        self.fruit_normal = pygame.transform.scale(node.FRUIT_IMG, (32, 32))
        self.fruit_pacman = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.fruit_pacman.blit(pygame.image.load("res/fruits.png"), (0, 0))
        self.fruit_pacman = pygame.transform.scale(self.fruit_pacman, (32, 32))
        self.fruit_smw = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.fruit_smw.blit(pygame.image.load("res/smw.png"), (-32, 0))
        self.fruit_smw = pygame.transform.scale(self.fruit_smw, (32, 32))

        self.fruit_type = 0

        self.ia_active = False

        self.buttons = [
            ButtonLabel("-", window_bounds[0]/4-32-32, window_bounds[1]/3+16, 32, 32, text.get_font(32), command=lambda: self.decr_width()),
            ButtonLabel("+", window_bounds[0]/4+56-32, window_bounds[1]/3+16, 32, 32, text.get_font(32), command=lambda: self.incr_width()),
            ButtonLabel("-", window_bounds[0]/2+window_bounds[0]/4-32, window_bounds[1]/3+16, 32, 32, text.get_font(32), command=lambda: self.decr_height()),
            ButtonLabel("+", window_bounds[0]/2+window_bounds[0]/4+56, window_bounds[1]/3+16, 32, 32, text.get_font(32), command=lambda: self.incr_height()),
            ButtonLabel("<", window_bounds[0]/2 - 24-32-92, window_bounds[1]/2+32, 32, 32, text.get_font(32), command=lambda: self.decr_speed()),
            ButtonLabel(">", window_bounds[0]/2 + 24+92, window_bounds[1]/2+32, 32, 32, text.get_font(32), command=lambda: self.incr_speed()),
            ButtonLabel("Commencer", window_bounds[0]/2 - (284/2), window_bounds[1] - 72, 284, 32, text.get_font(32), command=lambda: self.set_ingame_state()),
            ButtonLabel("<", window_bounds[0] - 24 - 32 - 92, window_bounds[1]/2+108, 32, 32, text.get_font(32), command=lambda: self.decr_fruit_type()),
            ButtonLabel(">", window_bounds[0] - 92+24, window_bounds[1]/2+108, 32, 32, text.get_font(32), command=lambda: self.incr_fruit_type()),
            TrueFalseButton(72, window_bounds[1]/2+108, 32, pygame.image.load("res/checkbox.png"), pygame.image.load("res/checkbox_checked.png"), false_command=lambda: self.deselect_ia(), true_command=lambda: self.select_ia())
        ]

    def select_ia(self):
        self.ia_active = True

    def deselect_ia(self):
        self.ia_active = False

    def decr_fruit_type(self):
        if self.fruit_type > 0:
            self.fruit_type -= 1
        else:
            self.fruit_type = 2

    def incr_fruit_type(self):
        if self.fruit_type < 2:
            self.fruit_type += 1
        else:
            self.fruit_type = 0

    def set_ingame_state(self):
        game_state.set_custom_ingame_state(self.grid_width, self.grid_height, self.speed, self.fruit_type, self.ia_active)

    def incr_width(self):
        if self.grid_width < snake_grid.MAX_GRID_WIDTH:
            self.grid_width += 1

    def decr_width(self):
        if self.grid_width > snake_grid.MIN_GRID_WIDTH:
            self.grid_width -= 1

    def incr_height(self):
        if self.grid_height < snake_grid.MAX_GRID_HEIGHT:
            self.grid_height += 1

    def decr_height(self):
        if self.grid_height > snake_grid.MIN_GRID_HEIGHT:
            self.grid_height -= 1

    def incr_speed(self):
        i = SPEEDS.index(self.speed)
        if i < len(SPEEDS)-1:
            self.speed = SPEEDS[i+1]

    def decr_speed(self):
        i = SPEEDS.index(self.speed)
        if i > 0:
            self.speed = SPEEDS[i - 1]

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_aligned_text("Jouer", screen.get_width()/2, 24, screen, text.get_font(64), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=8)
        text.draw_aligned_text("Longueur", screen.get_width() / 4 - 4, screen.get_height() / 3 -24, screen, text.get_font(24))
        text.draw_aligned_text("Largeur", screen.get_width()/2+screen.get_width()/4+28, screen.get_height() / 3 - 24, screen, text.get_font(24))
        text.draw_aligned_text(str(self.grid_width), screen.get_width()/4-4, screen.get_height()/3+4+16, screen, text.get_font(24))
        text.draw_aligned_text(str(self.grid_height), screen.get_width()/2+screen.get_width()/4+28, screen.get_height()/3+4+16, screen, text.get_font(24))
        text.draw_aligned_text(SPEEDS_NAME[SPEEDS.index(self.speed)], screen.get_width()/2, screen.get_height() / 2+36, screen, text.get_font(24))
        text.draw_aligned_text("Fruits", screen.get_width() - 92, screen.get_height() / 2+72, screen, text.get_font(16), color=(0, 190, 255), shadow_color=(0, 100, 255), shadow_offset=2)
        text.draw_aligned_text("IA", 88, screen.get_height()/2+108-32, screen, text.get_font(16), color=(100, 200, 0), shadow_color=(80, 165, 0), shadow_offset=2)
        img_x = screen.get_width() - 18 - 92
        img_y = screen.get_height()/2 + 108
        if self.fruit_type == snake_grid.FRUIT_NORMAL:
            screen.blit(self.fruit_normal, (img_x, img_y))
        elif self.fruit_type == snake_grid.FRUIT_PACMAN:
            screen.blit(self.fruit_pacman, (img_x, img_y))
        elif self.fruit_type == snake_grid.FRUIT_SMW:
            screen.blit(self.fruit_smw, (img_x, img_y))

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape":
                game_state.set_state(game_state.MENU)
