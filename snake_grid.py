import pygame
from node import *
import random

GRID_WIDTH = 15
GRID_HEIGHT = 15

K_RIGHT = "right"
K_LEFT = "left"
K_UP = "up"
K_DOWN = "down"

VALID_INPUTS = [K_RIGHT, K_LEFT, K_UP, K_DOWN]
# KEYS_PRESSED = [False, False, False, False]


class SnakeGrid:

    def __init__(self, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.nodes: list[list] = []
        self.fruit_pos = (-1, -1)

        # fill grid with "empty" slots
        for row in range(self.grid_width):
            self.nodes.append([])
            for col in range(self.grid_height):
                self.nodes[row].append(None)

        # create the snake
        for i in range(3):
            self.create_snake_node(3-i, int(self.grid_height/2)-1)

        self.place_fruit()

        self.grid_surface = pygame.Surface((TILE_SIZE*self.grid_width, TILE_SIZE*self.grid_height))

        self.colided = False

        self.pending_input = ""
        self.last_input = "right"
        self.inputs = [self.last_input] * 4

    def create_snake_node(self, tile_x, tile_y):
        self.nodes[tile_x][tile_y] = Node(self.get_number_of_snake_nodes())

    def place_fruit(self):
        empty_coords: list[tuple] = []
        for row in range(self.grid_width):
            for col in range(self.grid_height):
                if self.nodes[row][col] is None:
                    empty_coords.append((row, col))
        self.fruit_pos = empty_coords[random.randint(0, len(empty_coords)-1)]

    def is_fruit_valid(self):
        if 0 <= self.fruit_pos[0] < self.grid_width and 0 <= self.fruit_pos[0] < self.grid_height:
            return True
        return False

    def get_number_of_snake_nodes(self):
        count = 0
        for row in range(self.grid_width):
            for col in range(self.grid_height):
                if self.nodes[row][col] is not None:
                    count += 1
        return count

    def get_rendered_grid(self):
        self.grid_surface.fill((30, 30, 30))
        for row in range(self.grid_width):
            for col in range(self.grid_height):
                if self.nodes[row][col] is not None:
                    self.nodes[row][col].render(self.grid_surface, row, col)
        if self.is_fruit_valid():
            self.grid_surface.blit(FRUIT_IMG, (self.fruit_pos[0]*TILE_SIZE, self.fruit_pos[1]*TILE_SIZE))
        return self.grid_surface

    def update(self):
        if self.pending_input not in VALID_INPUTS:
            self.pending_input = self.last_input

        self.inputs.insert(0, self.pending_input)
        self.inputs = self.inputs[:self.get_number_of_snake_nodes() + 1]

        new_nodes: list[list] = []
        for row in range(self.grid_width):
            new_nodes.append([])
            for col in range(self.grid_height):
                new_nodes[row].append(None)

        for row in range(self.grid_width):
            for col in range(self.grid_height):
                if self.nodes[row][col] is not None:
                    node = self.nodes[row][col]
                    if not self.colided:
                        if self.inputs[node.get_ID()] == K_RIGHT:
                            if node.get_ID() == 0 and row + 1 < self.grid_width and type(self.nodes[row + 1][col]) is Node:
                                self.inputs[node.get_ID()] = K_LEFT
                                self.pending_input = K_LEFT
                                self.move_node_left(new_nodes, node, row, col)
                            else:
                                self.move_node_right(new_nodes, node, row, col)
                        elif self.inputs[node.get_ID()] == K_LEFT:
                            if node.get_ID() == 0 and row - 1 >= 0 and type(self.nodes[row - 1][col]) is Node:
                                self.inputs[node.get_ID()] = K_RIGHT
                                self.pending_input = K_RIGHT
                                self.move_node_right(new_nodes, node, row, col)
                            else:
                                self.move_node_left(new_nodes, node, row, col)
                        elif self.inputs[node.get_ID()] == K_UP:
                            if node.get_ID() == 0 and col - 1 >= 0 and type(self.nodes[row][col - 1]) is Node:
                                self.inputs[node.get_ID()] = K_DOWN
                                self.pending_input = K_DOWN
                                self.move_node_down(new_nodes, node, row, col)
                            else:
                                self.move_node_up(new_nodes, node, row, col)
                        elif self.inputs[node.get_ID()] == K_DOWN:
                            if node.get_ID() == 0 and col + 1 < self.grid_height and type(self.nodes[row][col + 1]) is Node:
                                self.inputs[node.get_ID()] = K_UP
                                self.pending_input = K_UP
                                self.move_node_up(new_nodes, node, row, col)
                            else:
                                self.move_node_down(new_nodes, node, row, col)

        if not self.colided:
            self.nodes = new_nodes

        self.last_input = self.pending_input
        self.pending_input = ""

    def move_node_right(self, new_nodes, node, row, col):
        if row + 1 < self.grid_width:
            new_nodes[row + 1][col] = node
        else:
            self.colided = True

    def move_node_left(self, new_nodes, node, row, col):
        if row - 1 >= 0:
            new_nodes[row - 1][col] = node
        else:
            self.colided = True

    def move_node_up(self, new_nodes, node, row, col):
        if col - 1 >= 0:
            new_nodes[row][col - 1] = node
        else:
            self.colided = True

    def move_node_down(self, new_nodes, node, row, col):
        if col + 1 < self.grid_height:
            new_nodes[row][col + 1] = node
        else:
            self.colided = True

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in VALID_INPUTS:
                self.pending_input = pygame.key.name(event.key)
