import pygame
import button
import snake_grid

# Holds the current state ID of the game
state = 0
update_pending = False

load_custom_ingame = False
grid_width = snake_grid.GRID_WIDTH
grid_height = snake_grid.GRID_HEIGHT
speed = 0.15
fruit_type = 0
ia_active = False


MENU = 0
INGAME = 1
PROFILE = 2
SCOREBOARD = 3
CUSTOMIZE = 4


profile_name = "joueur"


def set_state(newstate):
    global state
    global update_pending
    state = newstate
    update_pending = True


def set_custom_ingame_state(grid_width_in, grid_height_in, speed_in, fruit_type_in, ia_active_in):
    global load_custom_ingame
    global grid_width
    global grid_height
    global speed
    global fruit_type
    global ia_active
    load_custom_ingame = True
    grid_width = grid_width_in
    grid_height = grid_height_in
    speed = speed_in
    fruit_type = fruit_type_in
    ia_active = ia_active_in
    set_state(INGAME)


# base class for states with basic button support
class GameState:
    def __init__(self):
        self.buttons: list[button.BaseButton] = []

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            button.render(screen)

    def input(self, event: pygame.event.Event):
        for button in self.buttons:
            button.mouse_input(event)
