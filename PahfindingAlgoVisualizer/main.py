import pygame
import math
import random
from queue import PriorityQueue

WIDTH = 800

# some colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
LPURPLE = (136, 55, 250)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
BLUE = (0, 0, 255)

BUTTON_OULINE_COLOR = (94, 95, 97)
BUTTON_FILL_COLOR = (89, 148, 240)
BUTTON_HOVERFILL_COLOR = (26, 107, 232)

# we make a square, so height == width
WIN = pygame.display.set_mode((WIDTH+150, WIDTH+100))
pygame.display.set_caption("Path Algorithm Visualizer")
pygame.font.init()
myfont = pygame.font.SysFont("Britannic", 40)
myfont2 = pygame.font.SysFont("Britannic", 25)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight_penalty = 0

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_path(self):
        return self.color == PURPLE

    def is_weightedpath(self):
        return self.color == LPURPLE

    def is_weight(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def make_weightedpath(self):
        self.color = LPURPLE

    def make_weight(self):
        self.weight_penalty = 15
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neigthbors(self, grid):
        self.neighbors = []
        # down
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row-1][self.col])

        # right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():  # left
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False


def h(p1, p2):
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
                    h(neighbor.get_pos(), end.get_pos())) + neighbor.weight_penalty
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
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + 0
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


def astar_algorithm(draw, grid, start, end):
    cleanup_grid(grid)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
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


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))


def draw_button_shapes(win, dimensions):
    position = pygame.mouse.get_pos()
    x, y, width, height = dimensions

    # mouse hover
    if (position[0] >= (x-2) and position[0] <= (x+width+2)) and (position[1] >= (y-2) and position[1] <= (y+height+2)):
        pygame.draw.rect(win, BUTTON_OULINE_COLOR, (x-2, y-2, width+4, height+4),
                         width=2, border_radius=4)
        pygame.draw.rect(win, BUTTON_HOVERFILL_COLOR,
                         (x, y, width, height), border_radius=4)
    # mouse is somewhere else
    else:
        pygame.draw.rect(win, BUTTON_OULINE_COLOR, (x-2, y-2, width+4, height+4),
                         width=2, border_radius=4)
        pygame.draw.rect(win, BUTTON_FILL_COLOR,
                         (x, y, width, height), border_radius=4)


def draw_sidearea(win, width):
    pygame.draw.line(win, BLACK, (801, 0), (801, width))
    pygame.draw.rect(win, (247, 230, 190), (803, 1, width+150, width))

    # map keys
    pygame.draw.rect(win, ORANGE, (810, 10, 40, 40))
    pygame.draw.rect(win, TURQUOISE, (810, 80, 40, 40))
    pygame.draw.rect(win, BLACK, (810, 150, 40, 40))
    pygame.draw.rect(win, BLUE, (810, 220, 40, 40))

    pygame.draw.rect(win, GREEN, (810, 320, 40, 40))
    pygame.draw.rect(win, RED, (810, 390, 40, 40))
    pygame.draw.rect(win, PURPLE, (810, 460, 40, 40))
    pygame.draw.rect(win, LPURPLE, (810, 530, 40, 40))
    # map text
    start_key = myfont2.render('Start node', True, BLACK)
    end_key = myfont2.render('End node', True, BLACK)
    wall_key = myfont2.render('Wall', True, BLACK)
    weight_key = myfont2.render('Weight', True, BLACK)

    open_key = myfont2.render('Opened', True, BLACK)
    closed_key = myfont2.render('Visited', True, BLACK)
    path_key = myfont2.render('Path', True, BLACK)
    weightedpath_key = myfont2.render('Weightpath', True, BLACK)

    win.blit(start_key, (855, 20))
    win.blit(end_key, (855, 90))
    win.blit(wall_key, (855, 160))
    win.blit(weight_key, (855, 230))

    win.blit(open_key, (855, 330))
    win.blit(closed_key, (855, 400))
    win.blit(path_key, (855, 470))
    win.blit(weightedpath_key, (855, 540))


def draw_bottomarea(win, width):
    # info area
    info_text = myfont2.render(
        "Disclaimer: The speed of the animations DOES NOT represent the speed of the algorythms!", True, RED)
    pygame.draw.rect(win, (152, 226, 245), (0, 801, width+150, 200))
    pygame.draw.line(win, BLACK, (0, 801), (width+150, 801))
    pygame.draw.line(win, BLACK, (0, 838), (width+150, 838))
    win.blit(info_text, (120, 812))

    # Buttons area
    draw_button_shapes(win, (15, 850, 165, 28))
    draw_button_shapes(win, (192, 850, 190, 28))
    draw_button_shapes(win, (393, 850, 225, 28))
    draw_button_shapes(win, (632, 850, 195, 28))
    draw_button_shapes(win, (840, 850, 85, 28))
    # text for the buttons
    start_astar_button = myfont.render('Start A* Alg', True, BLACK)
    start_bfs_button = myfont.render('Start BFS Alg', True, BLACK)
    start_dijkstra_button = myfont.render('Start Dijkstra Alg', True, BLACK)
    walls_button = myfont.render('Random walls', True, BLACK)
    cleargrid_button = myfont.render('Clear', True, BLACK)
    win.blit(start_astar_button, (17, 850))
    win.blit(start_bfs_button, (194, 850))
    win.blit(start_dijkstra_button, (393, 850))
    win.blit(walls_button, (634, 850))
    win.blit(cleargrid_button, (842, 850))


def random_walls(win, grid, rows, width):
    # creating a fresh grid
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            # padding the grid with random walls and weights
            if i % random.randint(1, 4) and j % random.randint(2, 4):
                rint = random.randint(1, 6)
                if rint < 6:
                    spot.make_barrier()
                else:
                    spot.make_weight()
            grid[i].append(spot)
    return grid


def cleanup_grid(grid):
    for row in grid:
        for spot in row:
            if spot.weight_penalty > 0:
                spot.make_weight()
            elif spot.is_start():
                spot.make_start()
            else:
                if spot.is_open() or spot.is_closed() or spot.is_path():
                    spot.reset()


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    draw_sidearea(win, width)
    draw_bottomarea(win, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    start_screen = True

    while (start_screen):
        nlabel = myfont.render(
            "How to use:", 1, (255, 255, 255))
        nlabel1 = myfont.render(
            "* First LEFT-Click will set the starting position", 1, (255, 255, 255))
        nlabel2 = myfont.render(
            "* Second LEFT-Click will set the End-Position", 1, (255, 255, 255))
        nlabel3 = myfont.render(
            "* After that LEFT-Click will draw walls", 1, (255, 255, 255))
        nlabel4 = myfont.render(
            "MIDDLE-Click will draw weights", 1, (255, 255, 255))
        nlabel5 = myfont.render(
            "* RIGHT-Click will clear spots", 1, (255, 255, 255))
        nlabel6 = myfont.render(
            "Press any key to continue...", 1, (255, 255, 255))
        win.fill((84, 84, 84))
        win.blit(nlabel, (370, 100))
        win.blit(nlabel1, (170, 150))
        win.blit(nlabel2, (170, 200))
        win.blit(nlabel3, (170, 300))
        win.blit(nlabel4, (190, 350))
        win.blit(nlabel5, (170, 400))
        win.blit(nlabel6, (250, 650))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                start_screen = False
    # pygame mainloop
    while run and not start_screen:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # left mousebutton
                pos = pygame.mouse.get_pos()
                # if the mouse-pos is within the grid
                if pos[0] < width and pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()
                # if the mouse-pos is in the bottom area
                else:
                    # A* start button-pos
                    if (pos[0] >= 15 and pos[0] <= 178) and (pos[1] >= 848 and pos[1] <= 880):
                        if start and end:
                            for row in grid:
                                for spot in row:
                                    spot.update_neigthbors(grid)
                            astar_algorithm(lambda: draw(win, grid, ROWS, width),
                                            grid, start, end)
                    # BFS start button-pos
                    elif (pos[0] >= 192 and pos[0] <= 380) and (pos[1] >= 848 and pos[1] <= 880):
                        if start and end:
                            for row in grid:
                                for spot in row:
                                    spot.update_neigthbors(grid)
                            bfs_algorithm(lambda: draw(win, grid, ROWS, width),
                                          grid, start, end)
                    # Dijkstra start button-pos
                    elif (pos[0] >= 395 and pos[0] <= 620) and (pos[1] >= 848 and pos[1] <= 880):
                        if start and end:
                            for row in grid:
                                for spot in row:
                                    spot.update_neigthbors(grid)
                            dijkstra_algorithm(lambda: draw(win, grid, ROWS, width),
                                               grid, start, end)
                    # random walls button-pos
                    elif (pos[0] >= 63 and pos[0] <= 827) and (pos[1] >= 848 and pos[1] <= 880):
                        grid = random_walls(win, grid, ROWS, width)
                    # clear grid button-pos
                    elif (pos[0] >= 840 and pos[0] <= 925) and (pos[1] >= 848 and pos[1] <= 880):
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)
            elif pygame.mouse.get_pressed()[2]:  # right mousebutton
                pos = pygame.mouse.get_pos()
                # if the mouse-pos is within the grid
                if pos[0] < width and pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None
                # if the mouse-pos is in the bottom area
                else:
                    pass
            elif pygame.mouse.get_pressed()[1]:  # middle mousebutton
                pos = pygame.mouse.get_pos()
                # if the mouse-pos is within the grid
                if pos[0] < width and pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if spot != start and spot != end:
                        spot.make_weight()
    pygame.quit()


main(WIN, WIDTH)
