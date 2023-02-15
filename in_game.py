import time
import pygame
import score_utils
import text
import game_state
from node import TILE_SIZE
from snake_grid import SnakeGrid, VALID_INPUTS, GRID_WIDTH, GRID_HEIGHT
from button import ButtonLabel


def render_overlay(screen: pygame.Surface):
    rect_over = pygame.Surface((screen.get_width(), screen.get_height()))
    rect_over.set_alpha(150)
    rect_over.fill((40, 40, 40))
    screen.blit(rect_over, (0, 0))


class InGameState(game_state.GameState):

    def __init__(self, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT, TBU=0.15, custom_fruits=False):
        super().__init__()
        # Time Before Update
        self.TBU = TBU
        self.last_update: float = 0
        self.started = False

        self.paused = False

        self.snake_grid = SnakeGrid(grid_width, grid_height, custom_fruits)

        window_bounds = pygame.display.get_window_size()
        self.buttons = [
            ButtonLabel("Continuer", window_bounds[0] / 2 - 109, window_bounds[1] / 2, 218, 24, font=text.get_font(24), command=lambda: self.close_pause_menu()),
            ButtonLabel("Recommencer", window_bounds[0] / 2 - 132, window_bounds[1] / 2 + 84, 264, 24, font=text.get_font(24), command=lambda: game_state.set_custom_ingame_state(self.snake_grid.grid_width, self.snake_grid.grid_height, self.TBU, self.snake_grid.custom_fruits)),
            ButtonLabel("Quitter", window_bounds[0] / 2 - 86, window_bounds[1] / 2 + 168, 172, 24, font=text.get_font(24), command=lambda: game_state.set_state(game_state.MENU))
        ]

        self.gameover_button = ButtonLabel("Recommencer", window_bounds[0]/2 - 132, window_bounds[1]/2 + 128, 264, 24, font=text.get_font(24), command=lambda: game_state.set_custom_ingame_state(self.snake_grid.grid_width, self.snake_grid.grid_height, self.TBU, self.snake_grid.custom_fruits))

    def update(self):
        super().update()
        if self.started and not self.paused:
            if time.time() > self.last_update + self.TBU:
                self.last_update = time.time()
                self.snake_grid.update()

    def render(self, screen: pygame.Surface):
        rendered_surface = self.snake_grid.get_rendered_grid()
        stroke = 4
        pygame.draw.rect(screen, (0, 0, 0), (screen.get_width()/2 - rendered_surface.get_width()/2-stroke, screen.get_height()/2 - rendered_surface.get_height()/2 + TILE_SIZE-stroke, rendered_surface.get_width()+(stroke*2), rendered_surface.get_height()+(stroke*2)), width=stroke)
        screen.blit(rendered_surface, (screen.get_width()/2 - rendered_surface.get_width()/2, screen.get_height()/2 - rendered_surface.get_height()/2 + TILE_SIZE))
        text.draw_centered_text("Score : " + str(self.snake_grid.get_number_of_snake_nodes()-1), screen.get_width()/2, (screen.get_height()/2 - rendered_surface.get_height()/2 + TILE_SIZE)/2, screen, text.get_font(24))

        if self.paused:
            render_overlay(screen)
            text.draw_centered_text("Pause", screen.get_width()/2, 92, screen, text.get_font(48))
            super().render(screen)

        if self.snake_grid.win or self.snake_grid.collided:
            render_overlay(screen)
            if self.snake_grid.win:
                text.draw_centered_text("Victoire!", screen.get_width()/2, 128, screen, text.get_font(48), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=6)
            else:
                text.draw_centered_text("Game Over!", screen.get_width() / 2, 128, screen, text.get_font(48), color=(0, 190, 255), shadow_color=(0, 100, 255), shadow_offset=6)
            self.gameover_button.render(screen)
            text.draw_centered_text("Votre score: "+str(self.snake_grid.get_number_of_snake_nodes()-1), screen.get_width() / 2, screen.get_height()/2+32, screen, text.get_font(24))

    def input(self, event: pygame.event.Event):
        if not self.started and event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in VALID_INPUTS:
                self.started = True
        if self.started and not self.paused:
            self.snake_grid.input(event)

        if event.type == pygame.KEYDOWN:
            if (not self.snake_grid.win and not self.snake_grid.collided) and pygame.key.name(event.key) == "escape":
                if self.paused:
                    self.paused = False
                else:
                    self.paused = True
            if self.snake_grid.win or self.snake_grid.collided:
                if pygame.key.name(event.key) == "return":
                    if score_utils.get_score(game_state.profile_name) < self.snake_grid.get_number_of_snake_nodes()-1:
                        score_utils.add_score(game_state.profile_name, self.snake_grid.get_number_of_snake_nodes()-1)
                    game_state.set_custom_ingame_state(self.snake_grid.grid_width, self.snake_grid.grid_height, self.TBU, self.snake_grid.custom_fruits)

        if self.snake_grid.win or self.snake_grid.collided:
            self.gameover_button.mouse_input(event)

        if self.paused:
            super().input(event)

    def close_pause_menu(self):
        self.paused = False