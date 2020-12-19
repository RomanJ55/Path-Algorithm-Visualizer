from queue import PriorityQueue


def bfs_algorithm(draw, grid, start, end):
    cleanup_grid(grid)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    visited = {start}

    while not open_set.empty():
        current = open_set.get()[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                count += 1
                weighted_dist = (
                    heuristics(neighbor.get_pos(), end.get_pos())) + neighbor.weight_penalty
                came_from[neighbor] = current
                open_set.put(
                    (weighted_dist, count, neighbor))
                visited.add(neighbor)
                if not neighbor.is_weight():
                    neighbor.make_open()
                else:
                    neighbor.make_weight()
        draw()

        if current != start:
            current.make_closed()
    return False


def dijkstra_algorithm(draw, grid, start, end):
    cleanup_grid(grid)

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 + current.weight_penalty

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    weighted_dist = (g_score[neighbor]) + \
                        neighbor.weight_penalty
                    open_set.put((weighted_dist, count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_weight():
                        neighbor.make_open()
                    else:
                        neighbor.make_weight()
        draw()

        if current != start:
            current.make_closed()
    return False


def astar_algorithm(draw, grid, start, end):
    cleanup_grid(grid)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristics(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 + current.weight_penalty

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    heuristics(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    weighted_dist = (f_score[neighbor]) + \
                        neighbor.weight_penalty
                    open_set.put((weighted_dist, count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_weight():
                        neighbor.make_open()
                    else:
                        neighbor.make_weight()
        draw()

        if current != start:
            current.make_closed()
    return False


def heuristics(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs((y1-y2))


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current.weight_penalty > 0:
            current.make_weightedpath()
        elif not current.is_start():
            current.make_path()
        draw()


def cleanup_grid(grid):
    # removes all green, red and purple
    # leftovers from previous algorithms
    for row in grid:
        for spot in row:
            if spot.weight_penalty > 0:
                spot.make_weight()
            elif spot.is_start():
                spot.make_start()
            else:
                if spot.is_open() or spot.is_closed() or spot.is_path():
                    spot.reset()
