import pygame
import game_state
from menu import MenuState
from in_game import InGameState
from scoreboard import ScoreBoardState
from profile import ProfileState
from customize import CustomizeState


pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption("Snake")

game_state.state = 0
state = MenuState()

running = True

while running:

    # Update state
    if game_state.update_pending:
        if game_state.load_custom_ingame:
            game_state.load_custom_ingame = False
            state = InGameState(game_state.grid_width, game_state.grid_height, game_state.speed, game_state.custom_fruits)
        elif game_state.state == game_state.MENU:
            state = MenuState()
        elif game_state.state == game_state.INGAME:
            state = InGameState()
        elif game_state.state == game_state.PROFILE:
            state = ProfileState()
        elif game_state.state == game_state.SCOREBOARD:
            state = ScoreBoardState()
        elif game_state.state == game_state.CUSTOMIZE:
            state = CustomizeState()
        else:
            print("Invalid state id:", game_state.state)
        game_state.update_pending = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        state.input(event)

    state.update()

    screen.fill((40, 40, 40))

    state.render(screen)

    pygame.display.flip()
