import math


def next_input(nodes: list[list], inputs: list[str], fruit_pos: tuple[int, int]):
    next_direction = inputs[0]
    grid_width = len(nodes)
    grid_height = len(nodes[0])

    def fruit_is_right():
        return head_pos[0] - fruit_pos[0] < 0

    def fruit_is_left():
        return head_pos[0] - fruit_pos[0] > 0

    def fruit_is_up():
        return head_pos[1] - fruit_pos[1] > 0

    def fruit_is_down():
        return head_pos[1] - fruit_pos[1] < 0

    def is_tile_free(direction):
        tile_x = head_pos[0]
        tile_y = head_pos[1]
        if direction == "right":
            return 0 <= tile_x+1 < grid_width and 0 <= tile_y < grid_height and nodes[tile_x+1][tile_y] == -1
        elif direction == "left":
            return 0 <= tile_x-1 < grid_width and 0 <= tile_y < grid_height and nodes[tile_x-1][tile_y] == -1
        elif direction == "up":
            return 0 <= tile_x < grid_width and 0 <= tile_y-1 < grid_height and nodes[tile_x][tile_y-1] == -1
        elif direction == "down":
            return 0 <= tile_x < grid_width and 0 <= tile_y+1 < grid_height and nodes[tile_x][tile_y+1] == -1
        return False

    def is_tile_free_from_pos(direction, pos: tuple[int, int]):
        tile_x = pos[0]
        tile_y = pos[1]
        if direction == "right":
            return 0 <= tile_x + 1 < grid_width and 0 <= tile_y < grid_height and nodes[tile_x + 1][tile_y] == -1
        elif direction == "left":
            return 0 <= tile_x - 1 < grid_width and 0 <= tile_y < grid_height and nodes[tile_x - 1][tile_y] == -1
        elif direction == "up":
            return 0 <= tile_x < grid_width and 0 <= tile_y - 1 < grid_height and nodes[tile_x][tile_y - 1] == -1
        elif direction == "down":
            return 0 <= tile_x < grid_width and 0 <= tile_y + 1 < grid_height and nodes[tile_x][tile_y + 1] == -1
        return False

    def get_num_tiles_free(direction):
        count = 0
        tile_x = head_pos[0]
        tile_y = head_pos[1]
        if direction == "right":
            for i in range(1, grid_width-tile_x):
                if tile_x+i == grid_width and head_pos[0] != grid_height-1:
                    count = int(math.inf)
                    print(direction, count)
                    break
                if is_tile_free_from_pos("right", (tile_x+i, tile_y)):
                    count += 1
                else:
                    break
        elif direction == "left":
            for i in range(1, tile_x):
                if tile_x-i == 0 and head_pos[0] != 0:
                    count = int(math.inf)
                    print(direction, count)
                    break
                if is_tile_free_from_pos("left", (tile_x - i, tile_y)):
                    count += 1
                else:
                    break
        elif direction == "up":
            for i in range(1, tile_y):
                if tile_y-i == 0 and head_pos[1] != 0:
                    count = int(math.inf)
                    print(direction, count)
                    break
                if is_tile_free_from_pos("up", (tile_x, tile_y-i)):
                    count += 1
                else:
                    break
        elif direction == "down":
            for i in range(1, grid_height - tile_y):
                if tile_y+i == grid_height and head_pos[1] != grid_height-1:
                    count = int(math.inf)
                    print(direction, count)
                    break
                if is_tile_free_from_pos("down", (tile_x, tile_y + i)):
                    count += 1
                else:
                    break
        return count

    head_pos = (-1, -1)
    for col in range(grid_width):
        if not head_pos == (-1, -1):
            break
        for row in range(grid_height):
            if nodes[col][row] == 0:
                head_pos = (col, row)
                break

    # check straight directions
    if fruit_is_right() and head_pos[1] == fruit_pos[1]:
        next_direction = "right"
        if inputs[0] == "left":
            if is_tile_free("down"):
                next_direction = "down"
            elif is_tile_free("up"):
                next_direction = "up"
        if next_direction == "right":
            if not is_tile_free("right"):
                if is_tile_free("down"):
                    next_direction = "down"
                elif is_tile_free("up"):
                    next_direction = "up"
    elif fruit_is_left() and head_pos[1] == fruit_pos[1]:
        next_direction = "left"
        if inputs[0] == "right":
            if is_tile_free("down"):
                next_direction = "down"
            elif is_tile_free("up"):
                next_direction = "up"
        if next_direction == "left":
            if not is_tile_free("left"):
                if is_tile_free("down"):
                    next_direction = "down"
                elif is_tile_free("up"):
                    next_direction = "up"
    elif fruit_is_up() and head_pos[0] == fruit_pos[0]:
        next_direction = "up"
        if inputs[0] == "down":
            if is_tile_free("left"):
                next_direction = "left"
            elif is_tile_free("right"):
                next_direction = "right"
        if next_direction == "up":
            if not is_tile_free("up"):
                if is_tile_free("left"):
                    next_direction = "left"
                elif is_tile_free("right"):
                    next_direction = "right"
    elif fruit_is_down() and head_pos[0] == fruit_pos[0]:
        next_direction = "down"
        if inputs[0] == "up":
            if is_tile_free("left"):
                next_direction = "left"
            elif is_tile_free("right"):
                next_direction = "right"
        if next_direction == "down":
            if not is_tile_free("down"):
                if is_tile_free("left"):
                    next_direction = "left"
                elif is_tile_free("right"):
                    next_direction = "right"
    else:
        if fruit_is_right():
            next_direction = "right"
            if not is_tile_free("right"):
                if get_num_tiles_free("down") > get_num_tiles_free("up"):
                    if is_tile_free("down"):
                        next_direction = "down"
                    elif is_tile_free("up"):
                        next_direction = "up"
                else:
                    if is_tile_free("up"):
                        next_direction = "up"
                    elif is_tile_free("down"):
                        next_direction = "down"

        elif fruit_is_left():
            next_direction = "left"
            if not is_tile_free("left"):
                if get_num_tiles_free("down") > get_num_tiles_free("up"):
                    if is_tile_free("down"):
                        next_direction = "down"
                    elif is_tile_free("up"):
                        next_direction = "up"
                else:
                    if is_tile_free("up"):
                        next_direction = "up"
                    elif is_tile_free("down"):
                        next_direction = "down"

        elif fruit_is_down():
            next_direction = "down"
            if not is_tile_free("down"):
                if get_num_tiles_free("left") > get_num_tiles_free("right"):
                    if is_tile_free("left"):
                        next_direction = "left"
                    elif is_tile_free("right"):
                        next_direction = "right"
                else:
                    if is_tile_free("right"):
                        next_direction = "right"
                    elif is_tile_free("left"):
                        next_direction = "left"

        elif fruit_is_up():
            next_direction = "up"
            if not is_tile_free("up"):
                if get_num_tiles_free("left") > get_num_tiles_free("right"):
                    if is_tile_free("left"):
                        next_direction = "left"
                    elif is_tile_free("right"):
                        next_direction = "right"
                else:
                    if is_tile_free("right"):
                        next_direction = "right"
                    elif is_tile_free("left"):
                        next_direction = "left"



    return next_direction
