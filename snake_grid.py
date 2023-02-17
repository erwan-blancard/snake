import os

import pygame
import random

GRID_WIDTH = 20
MIN_GRID_WIDTH = 16
MAX_GRID_WIDTH = 44
GRID_HEIGHT = 12
MIN_GRID_HEIGHT = 12
MAX_GRID_HEIGHT = 26

K_RIGHT = "right"
K_LEFT = "left"
K_UP = "up"
K_DOWN = "down"

VALID_INPUTS = [K_RIGHT, K_LEFT, K_UP, K_DOWN]

# Nodes
TILE_SIZE = 16

# default Node image
surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
surf.fill((100, 200, 0))
surf.fill((80, 165, 0), (1, 1, TILE_SIZE-2, TILE_SIZE-2))
DEFAULT_SNAKE_IMG = surf

# default Fruit image
surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
surf.fill((240, 40, 40))
surf.fill((200, 0, 0), (1, 1, TILE_SIZE-2, TILE_SIZE-2))
DEFAULT_FRUIT_IMG = surf


class SnakeGrid:

    def __init__(self, grid_width, grid_height, skin: str = None):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.nodes: list[list[int]] = []

        self.skin = skin
        self.fruit_spritesheet: pygame.Surface = DEFAULT_FRUIT_IMG
        self.fruit_index = 0

        self.snake_head: pygame.Surface = DEFAULT_SNAKE_IMG
        self.snake_body: pygame.Surface = DEFAULT_SNAKE_IMG

        # load skin
        if skin is not None:
            if os.path.exists("skins/"+self.skin):
                if os.path.exists("skins/"+self.skin+"/fruit.png"):
                    try:
                        self.fruit_spritesheet = pygame.image.load("skins/"+self.skin+"/fruit.png")
                    except Exception as e:
                        print("Could not load " + "skins/"+self.skin+"/fruit.png"+": "+str(e))
                        self.fruit_spritesheet: pygame.Surface = DEFAULT_FRUIT_IMG
                if os.path.exists("skins/"+self.skin+"/head.png"):
                    try:
                        self.snake_head = pygame.image.load("skins/"+self.skin+"/head.png")
                    except Exception as e:
                        print("Could not load " + "skins/" + self.skin + "/head.png"+": "+str(e))
                        self.snake_head: pygame.Surface = DEFAULT_SNAKE_IMG
                if os.path.exists("skins/"+self.skin+"/body.png"):
                    try:
                        self.snake_body = pygame.image.load("skins/"+self.skin+"/body.png")
                    except Exception as e:
                        print("Could not load " + "skins/"+self.skin+"/body.png"+": "+str(e))
                        self.snake_body: pygame.Surface = DEFAULT_SNAKE_IMG

        self.fruit_pos = (-1, -1)
        self.fruit_eaten = False

        # fill grid with "empty" slots
        for col in range(self.grid_width):
            self.nodes.append([])
            for row in range(self.grid_height):
                self.nodes[col].append(-1)

        # create the snake
        self.create_snake_node(self.nodes, int(self.grid_width/2)-1, int(self.grid_height/2)-1)

        self.place_fruit(self.nodes)

        self.grid_surface = pygame.Surface((TILE_SIZE*self.grid_width, TILE_SIZE*self.grid_height))

        self.collided = False
        self.win = False

        self.pending_input = ""
        self.last_input = "right"
        self.inputs = [self.last_input] * 2

    def create_snake_node(self, node_list, tile_x, tile_y):
        node_list[tile_x][tile_y] = self.get_number_of_snake_nodes()

    def place_fruit(self, node_list):
        empty_coords: list[tuple] = []
        for col in range(self.grid_width):
            for row in range(self.grid_height):
                if node_list[col][row] == -1:
                    empty_coords.append((col, row))
        if len(empty_coords)-1 < 0:
            self.win = True
        else:
            self.fruit_pos = empty_coords[random.randint(0, len(empty_coords)-1)]
            self.fruit_index = random.randint(0, int(self.fruit_spritesheet.get_width()/self.fruit_spritesheet.get_height())-1)

    def is_fruit_valid(self):
        if 0 <= self.fruit_pos[0] < self.grid_width and 0 <= self.fruit_pos[1] < self.grid_height:
            return True
        return False

    def get_number_of_snake_nodes(self):
        count = 0
        for col in range(self.grid_width):
            for row in range(self.grid_height):
                if self.nodes[col][row] != -1:
                    count += 1
        return count

    def get_rendered_grid(self):
        self.grid_surface.fill((30, 30, 30))
        for col in range(self.grid_width):
            for row in range(self.grid_height):
                if self.nodes[col][row] != -1:
                    if self.nodes[col][row] == 0:
                        self.grid_surface.blit(self.snake_head, (col * TILE_SIZE, row * TILE_SIZE))
                    else:
                        self.grid_surface.blit(self.snake_body, (col * TILE_SIZE, row * TILE_SIZE))
        if self.is_fruit_valid():
            img = pygame.Surface((16, 16), pygame.SRCALPHA)
            img.blit(self.fruit_spritesheet, (self.fruit_index*(-self.fruit_spritesheet.get_height()), 0))
            # img.blit(self.fruit_spritesheet, (0, 0), (self.fruit_index*self.fruit_spritesheet.get_height(), 0, self.fruit_spritesheet.get_height(), self.fruit_spritesheet.get_height()))
            self.grid_surface.blit(img, (self.fruit_pos[0]*TILE_SIZE, self.fruit_pos[1]*TILE_SIZE))
        return self.grid_surface

    def update(self):
        if self.pending_input not in VALID_INPUTS:
            self.pending_input = self.last_input

        self.inputs.insert(0, self.pending_input)
        self.inputs = self.inputs[:self.get_number_of_snake_nodes() + 1]

        new_nodes: list[list] = []
        for col in range(self.grid_width):
            new_nodes.append([])
            for row in range(self.grid_height):
                new_nodes[col].append(-1)

        for col in range(self.grid_width):
            for row in range(self.grid_height):
                if self.nodes[col][row] != -1:
                    node = self.nodes[col][row]
                    if not self.win and not self.collided:
                        if self.inputs[node] == K_RIGHT:
                            if node == 0 and col + 1 < self.grid_width and self.nodes[col + 1][row] == 1:
                                self.inputs[node] = K_LEFT
                                self.pending_input = K_LEFT
                                self.move_node_left(new_nodes, node, col, row)
                            else:
                                self.move_node_right(new_nodes, node, col, row)
                        elif self.inputs[node] == K_LEFT:
                            if node == 0 and col - 1 >= 0 and self.nodes[col - 1][row] == 1:
                                self.inputs[node] = K_RIGHT
                                self.pending_input = K_RIGHT
                                self.move_node_right(new_nodes, node, col, row)
                            else:
                                self.move_node_left(new_nodes, node, col, row)
                        elif self.inputs[node] == K_UP:
                            if node == 0 and row - 1 >= 0 and self.nodes[col][row - 1] == 1:
                                self.inputs[node] = K_DOWN
                                self.pending_input = K_DOWN
                                self.move_node_down(new_nodes, node, col, row)
                            else:
                                self.move_node_up(new_nodes, node, col, row)
                        elif self.inputs[node] == K_DOWN:
                            if node == 0 and row + 1 < self.grid_height and self.nodes[col][row + 1] == 1:
                                self.inputs[node] = K_UP
                                self.pending_input = K_UP
                                self.move_node_up(new_nodes, node, col, row)
                            else:
                                self.move_node_down(new_nodes, node, col, row)

        if not self.win and not self.collided:
            if self.fruit_eaten:
                for col in range(self.grid_width):
                    for row in range(self.grid_height):
                        if self.nodes[col][row] == self.get_number_of_snake_nodes()-1:
                            self.create_snake_node(new_nodes, col, row)
                self.fruit_pos = (-1, -1)
                self.place_fruit(new_nodes)
                self.fruit_eaten = False
            self.nodes = new_nodes

        self.last_input = self.pending_input
        self.pending_input = ""

    def move_node_right(self, new_nodes, node: int, col, row):
        if node == 0 and col + 1 < self.grid_width and self.nodes[col + 1][row] > 1 and not self.nodes[col + 1][row] == self.get_number_of_snake_nodes()-1:
            self.collided = True
        else:
            if col + 1 < self.grid_width:
                new_nodes[col + 1][row] = node
                self.check_fruit(col + 1, row)
            else:
                self.collided = True

    def move_node_left(self, new_nodes, node: int, col, row):
        if node == 0 and col - 1 >= 0 and self.nodes[col - 1][row] > 1 and not self.nodes[col - 1][row] == self.get_number_of_snake_nodes()-1:
            self.collided = True
        else:
            if col - 1 >= 0:
                new_nodes[col - 1][row] = node
                self.check_fruit(col - 1, row)
            else:
                self.collided = True

    def move_node_up(self, new_nodes, node: int, col, row):
        if node == 0 and row - 1 >= 0 and self.nodes[col][row - 1] > 1 and not self.nodes[col][row - 1] == self.get_number_of_snake_nodes()-1:
            self.collided = True
        else:
            if row - 1 >= 0:
                new_nodes[col][row - 1] = node
                self.check_fruit(col, row - 1)
            else:
                self.collided = True

    def move_node_down(self, new_nodes, node: int, col, row):
        if node == 0 and row + 1 < self.grid_height and self.nodes[col][row + 1] > 1 and not self.nodes[col][row + 1] == self.get_number_of_snake_nodes()-1:
            self.collided = True
        else:
            if row + 1 < self.grid_height:
                new_nodes[col][row + 1] = node
                self.check_fruit(col, row + 1)
            else:
                self.collided = True

    def check_fruit(self, col, row):
        if self.fruit_pos == (col, row):
            self.fruit_eaten = True

    def input(self, key_input: str):
        if key_input in VALID_INPUTS:
            self.pending_input = key_input
