MAX_COUNT = 32767


# V3
def ia(nodes: list[list], inputs: list[str], fruit_pos: tuple[int, int]):
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

    def is_tile_in_bounds(direction):
        return is_tile_in_bounds_from_pos(direction, head_pos)

    def is_tile_in_bounds_from_pos(direction, pos: tuple[int, int]):
        tile_x = pos[0]
        tile_y = pos[1]
        if direction == "right":
            return 0 <= tile_x + 1 < grid_width and 0 <= tile_y < grid_height
        elif direction == "left":
            return 0 <= tile_x - 1 < grid_width and 0 <= tile_y < grid_height
        elif direction == "up":
            return 0 <= tile_x < grid_width and 0 <= tile_y - 1 < grid_height
        elif direction == "down":
            return 0 <= tile_x < grid_width and 0 <= tile_y + 1 < grid_height
        return False

    def is_tile_free(direction):
        return is_tile_free_from_pos(direction, head_pos)

    def is_tile_free_from_pos(direction, pos: tuple[int, int]):
        tile_x = pos[0]
        tile_y = pos[1]
        if direction == "right":
            return is_tile_in_bounds_from_pos(direction, pos) and (nodes[tile_x + 1][tile_y] == -1 or (tile_x + 1, tile_y) == last_node_pos)
        elif direction == "left":
            return is_tile_in_bounds_from_pos(direction, pos) and (nodes[tile_x - 1][tile_y] == -1 or (tile_x - 1, tile_y) == last_node_pos)
        elif direction == "up":
            return is_tile_in_bounds_from_pos(direction, pos) and (nodes[tile_x][tile_y - 1] == -1 or (tile_x, tile_y - 1) == last_node_pos)
        elif direction == "down":
            return is_tile_in_bounds_from_pos(direction, pos) and (nodes[tile_x][tile_y + 1] == -1 or (tile_x, tile_y + 1) == last_node_pos)
        return False

    def get_num_tiles_free(direction):
        count = 0
        tile_x = head_pos[0]
        tile_y = head_pos[1]
        if direction == "right":
            for i in range(grid_width-tile_x):
                if tile_x+i == grid_width and head_pos[0] != grid_height-1:
                    count = MAX_COUNT - count
                    break
                if is_tile_free_from_pos("right", (tile_x+i, tile_y)):
                    count += 1
                else:
                    break
        elif direction == "left":
            for i in range(tile_x):
                if tile_x-i == 0 and head_pos[0] != 0:
                    count = MAX_COUNT - count
                    break
                if is_tile_free_from_pos("left", (tile_x - i, tile_y)):
                    count += 1
                else:
                    break
        elif direction == "up":
            for i in range(tile_y):
                if tile_y-i == 0 and head_pos[1] != 0:
                    count = MAX_COUNT - count
                    break
                if is_tile_free_from_pos("up", (tile_x, tile_y-i)):
                    count += 1
                else:
                    break
        elif direction == "down":
            for i in range(grid_height - tile_y):
                if tile_y+i == grid_height and head_pos[1] != grid_height-1:
                    count = MAX_COUNT - count
                    break
                if is_tile_free_from_pos("down", (tile_x, tile_y + i)):
                    count += 1
                else:
                    break
        print(direction, count)
        return count

    def choose_direction(dir1, dir2, direction):
        if is_tile_free(dir1) and is_tile_in_bounds(dir1):
            if get_num_tiles_free(dir1) < get_num_tiles_free(dir2) and is_tile_free(dir2):
                return dir2
            else:
                return dir1
        elif is_tile_free(dir2) and is_tile_in_bounds(dir2):
            if get_num_tiles_free(dir2) < get_num_tiles_free(dir1) and is_tile_free(dir1):
                return dir1
            else:
                return dir2

        return direction

    head_pos = (-1, -1)
    last_node_pos = (-1, -1)
    prev_id = -1
    for col in range(grid_width):
        for row in range(grid_height):
            if nodes[col][row] == 0:
                head_pos = (col, row)
            if nodes[col][row] > prev_id:
                prev_id = nodes[col][row]
                last_node_pos = (col, row)

    # check straight directions
    if fruit_is_right() and head_pos[1] == fruit_pos[1]:
        next_direction = "right"
        if inputs[0] == "left":
            next_direction = choose_direction("down", "up", next_direction)
        if next_direction == "right":
            if not is_tile_free("right"):
                next_direction = choose_direction("down", "up", next_direction)
    elif fruit_is_left() and head_pos[1] == fruit_pos[1]:
        next_direction = "left"
        if inputs[0] == "right":
            next_direction = choose_direction("down", "up", next_direction)
        if next_direction == "left":
            if not is_tile_free("left"):
                next_direction = choose_direction("down", "up", next_direction)
    elif fruit_is_up() and head_pos[0] == fruit_pos[0]:
        next_direction = "up"
        if inputs[0] == "down":
            next_direction = choose_direction("left", "right", next_direction)
        if next_direction == "up":
            if not is_tile_free("up"):
                next_direction = choose_direction("left", "right", next_direction)
    elif fruit_is_down() and head_pos[0] == fruit_pos[0]:
        next_direction = "down"
        if inputs[0] == "up":
            next_direction = choose_direction("left", "right", next_direction)
        if next_direction == "down":
            if not is_tile_free("down"):
                next_direction = choose_direction("left", "right", next_direction)
    else:
        if fruit_is_right():
            next_direction = "right"
            # add check here
            if not is_tile_free("right"):
                if get_num_tiles_free("down") > get_num_tiles_free("up"):
                    next_direction = choose_direction("down", "up", next_direction)
                else:
                    next_direction = choose_direction("up", "down", next_direction)

        elif fruit_is_left():
            next_direction = "left"
            # add check here
            if not is_tile_free("left"):
                if get_num_tiles_free("down") > get_num_tiles_free("up"):
                    next_direction = choose_direction("down", "up", next_direction)
                else:
                    next_direction = choose_direction("up", "down", next_direction)

        elif fruit_is_down():
            next_direction = "down"
            # add check here
            if not is_tile_free("down"):
                if get_num_tiles_free("left") > get_num_tiles_free("right"):
                    next_direction = choose_direction("left", "right", next_direction)
                else:
                    next_direction = choose_direction("right", "left", next_direction)

        elif fruit_is_up():
            next_direction = "up"
            # add check here
            if not is_tile_free("up"):
                if get_num_tiles_free("left") > get_num_tiles_free("right"):
                    next_direction = choose_direction("left", "right", next_direction)
                else:
                    next_direction = choose_direction("right", "left", next_direction)

    # correct direction
    if not is_tile_free(next_direction):
        if next_direction == "right":
            if inputs[0] == "left":
                next_direction = "left"
            # elif no space is available
            elif not is_tile_free("up") and not is_tile_free("down"):
                next_direction = "left"

        elif next_direction == "left":
            if inputs[0] == "right":
                next_direction = "right"
            elif not is_tile_free("up") and not is_tile_free("down"):
                next_direction = "right"

        elif next_direction == "up":
            if inputs[0] == "down":
                next_direction = "down"
            elif not is_tile_free("left") and not is_tile_free("right"):
                next_direction = "down"

        elif next_direction == "down":
            if inputs[0] == "up":
                next_direction = "up"
            elif not is_tile_free("left") and not is_tile_free("right"):
                next_direction = "up"

        # after fix
        if next_direction == "right":
            if not is_tile_free("right"):
                if is_tile_free("up") and is_tile_free("down"):
                    if get_num_tiles_free("up") > get_num_tiles_free("down"):
                        next_direction = "up"
                    else:
                        next_direction = "down"
                else:
                    if is_tile_free("up"):
                        next_direction = "up"
                    elif is_tile_free("down"):
                        next_direction = "down"

        elif next_direction == "left":
            if not is_tile_free("left"):
                if is_tile_free("up") and is_tile_free("down"):
                    if get_num_tiles_free("up") > get_num_tiles_free("down"):
                        next_direction = "up"
                    else:
                        next_direction = "down"
                else:
                    if is_tile_free("up"):
                        next_direction = "up"
                    elif is_tile_free("down"):
                        next_direction = "down"

        elif next_direction == "up":
            if not is_tile_free("up"):
                if is_tile_free("left") and is_tile_free("right"):
                    if get_num_tiles_free("left") > get_num_tiles_free("right"):
                        next_direction = "left"
                    else:
                        next_direction = "right"
                else:
                    if is_tile_free("left"):
                        next_direction = "left"
                    elif is_tile_free("right"):
                        next_direction = "right"

        elif next_direction == "down":
            if not is_tile_free("down"):
                if is_tile_free("left") and is_tile_free("right"):
                    if get_num_tiles_free("left") > get_num_tiles_free("right"):
                        next_direction = "left"
                    else:
                        next_direction = "right"
                else:
                    if is_tile_free("left"):
                        next_direction = "left"
                    elif is_tile_free("right"):
                        next_direction = "right"

    return next_direction
