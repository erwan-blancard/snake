import pygame

import text

TILE_SIZE = 8

# Node image
surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
surf.fill((100, 200, 0))
surf.fill((80, 165, 0), (1, 1, 6, 6))
SNAKE_IMG = surf

# Fruit image
surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
surf.fill((240, 40, 40))
surf.fill((200, 0, 0), (1, 1, 6, 6))
FRUIT_IMG = surf


class Node:

    def __init__(self, ID):
        self.ID = ID

    def render(self, surface: pygame.Surface, tile_x, tile_y):
        surface.blit(SNAKE_IMG, (tile_x * TILE_SIZE, tile_y * TILE_SIZE))
        text.draw_text(str(self.get_ID()), tile_x * TILE_SIZE, tile_y * TILE_SIZE, surface, text.GLOBAL_FONTS[0])

    def get_ID(self):
        return self.ID
