import math
import time

import pygame
import game_state
import text
from game_state import GameState
from button import ButtonLabel, ButtonIcon


class MenuState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()
        self.buttons += [
            ButtonLabel("Jouer", window_bounds[0] / 2 - 50, window_bounds[1] / 2 + 60, 100, 48, command=lambda: game_state.set_state(game_state.INGAME)),
            ButtonLabel("Scoreboard", window_bounds[0]/2 - 90, window_bounds[1] / 2 + 148, 180, 48, command=lambda: game_state.set_state(game_state.SCOREBOARD)),
            ButtonIcon(4, 4, 64, pygame.image.load("res/profile.png"), command=lambda: game_state.set_state(game_state.PROFILE))
        ]
        # self.titlelogo = pygame.image.load("res/logo.png")

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        # screen.blit(self.titlelogo, (screen.get_width()/2 - self.titlelogo.get_width()/2, 24 + (math.sin(time.time()*2)-0.5)*8))
        text.draw_text(game_state.profile_name, 4, 4+64+4, screen, text.GLOBAL_FONTS[0])

    def input(self, event: pygame.event.Event):
        super().input(event)
