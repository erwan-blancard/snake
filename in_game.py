import time

import pygame
import text
import game_state
from node import Node
from snake_grid import SnakeGrid, VALID_INPUTS


class InGameState(game_state.GameState):

    def __init__(self):
        super().__init__()
        # Time Before Update
        self.TBU = 0.15
        self.last_update: float = 0
        self.started = False

        self.snake_grid = SnakeGrid()

    def update(self):
        super().update()
        if self.started:
            if time.time() > self.last_update + self.TBU:
                self.last_update = time.time()
                self.snake_grid.update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        rendered_surface = self.snake_grid.get_rendered_grid()
        screen.blit(rendered_surface, (0, 0))
        if self.snake_grid.win:
            text.draw_text("won !", 200, 200, screen, pygame.font.Font(None, 24))
        if self.snake_grid.collided:
            text.draw_text("collided !", 200, 232, screen, pygame.font.Font(None, 24))

    def input(self, event: pygame.event.Event):
        super().input(event)
        if not self.started and event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in VALID_INPUTS:
                self.started = True
        if self.started:
            self.snake_grid.input(event)

