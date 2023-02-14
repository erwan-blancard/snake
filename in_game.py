import time

import pygame
import text
import game_state
from node import Node
from snake_grid import SnakeGrid


class InGameState(game_state.GameState):

    def __init__(self):
        super().__init__()
        # Time Before Update
        self.TBU = 0.15
        self.last_update: float = 0

        self.snake_grid = SnakeGrid()

    def update(self):
        super().update()
        if time.time() > self.last_update + self.TBU:
            self.last_update = time.time()
            self.snake_grid.update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        rendered_surface = self.snake_grid.get_rendered_grid()
        screen.blit(rendered_surface, (0, 0))

    def input(self, event: pygame.event.Event):
        super().input(event)
        self.snake_grid.input(event)

