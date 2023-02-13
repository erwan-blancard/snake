import pygame
import text
import game_state


class ProfileState(game_state.GameState):

    def __init__(self):
        super().__init__()

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if key_name == "escape":
                game_state.set_state(game_state.MENU)
