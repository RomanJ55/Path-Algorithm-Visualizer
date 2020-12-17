import random
import pygame
import algorithms as algo
from colors import RED, WHITE, BLACK, GREY, GREEN, PURPLE, LPURPLE, ORANGE, TURQUOISE, BLUE, BUTTON_FILL_COLOR, BUTTON_HOVERFILL_COLOR, BUTTON_OULINE_COLOR
from Spot import Spot

WIDTH = 800

WIN = pygame.display.set_mode((WIDTH+150, WIDTH+100))
pygame.display.set_caption("Pathfinder Algorithm Visualizer")
pygame.font.init()
myfont = pygame.font.SysFont("Britannic", 40)
myfont2 = pygame.font.SysFont("Britannic", 25)
clock = pygame.time.Clock()


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
        "Disclaimer: The speed of the animations DOES NOT represent the speed of the algorithms!", True, RED)
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
            # 'padding' the grid with random walls and weights
            if i % random.randint(1, 4) and j % random.randint(2, 4):
                rint = random.randint(1, 6)
                if rint < 6:
                    spot.make_barrier()
                else:
                    spot.make_weight()
            grid[i].append(spot)
    return grid


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
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    start_screen = True

    # pygame start screen
    while start_screen:
        nlabel = myfont.render(
            "How to use:", 1, WHITE)
        nlabel1 = myfont.render(
            "* First LEFT-Click will set the starting position", 1, WHITE)
        nlabel2 = myfont.render(
            "* Second LEFT-Click will set the End-Position", 1, WHITE)
        nlabel3 = myfont.render(
            "* After that, LEFT-Click will draw walls", 1, WHITE)
        nlabel4 = myfont.render(
            "MIDDLE-Click will draw weights", 1, WHITE)
        nlabel5 = myfont.render(
            "* RIGHT-Click will clear spots", 1, WHITE)
        nlabel6 = myfont.render(
            "Press any key to continue...", 1, WHITE)
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
            if event.type == pygame.QUIT:
                start_screen = False
                run = False
            if event.type == pygame.KEYDOWN:
                start_screen = False
    # pygame mainloop
    while run and not start_screen:
        clock.tick(60)
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # mouse events
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
                            algo.astar_algorithm(lambda: draw(win, grid, ROWS, width),
                                                 grid, start, end)
                    # BFS start button-pos
                    elif (pos[0] >= 192 and pos[0] <= 380) and (pos[1] >= 848 and pos[1] <= 880):
                        if start and end:
                            for row in grid:
                                for spot in row:
                                    spot.update_neigthbors(grid)
                            algo.bfs_algorithm(lambda: draw(win, grid, ROWS, width),
                                               grid, start, end)
                    # Dijkstra start button-pos
                    elif (pos[0] >= 395 and pos[0] <= 620) and (pos[1] >= 848 and pos[1] <= 880):
                        if start and end:
                            for row in grid:
                                for spot in row:
                                    spot.update_neigthbors(grid)
                            algo.dijkstra_algorithm(lambda: draw(win, grid, ROWS, width),
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
