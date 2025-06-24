import pygame
from dataclasses import dataclass
from enum import Enum, auto
from find_shortest_path import find_shortest_path
from config import config
from constants import AppState, Colors
from draw_cell import draw_cell

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Решатель лабиринтов")

grid = [[0 for _ in range(config.COLS)] for _ in range(config.ROWS)]
state = AppState.DRAWING_WALLS
left_mouse_pressed = False
last_cell = None
key_points_placed = 0

dirty_rects = []
full_redraw = True

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if state == AppState.DRAWING_WALLS:
                    print("Переход к выбору входа/выхода")
                    state = AppState.PLACING_POINTS
                elif state == AppState.PLACING_POINTS:
                    print("Ввод завершён")
                    state = AppState.SOLVING
                    answer = find_shortest_path(grid)
                    if answer:
                        grid = answer
                        full_redraw = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_mouse_pressed = True
                pos = pygame.mouse.get_pos()
                x = pos[0] // config.CELL_SIZE
                y = pos[1] // config.CELL_SIZE
                if state == AppState.DRAWING_WALLS:
                    grid[y][x] = 1
                    dirty_rects.append(pygame.Rect(
                        x * config.CELL_SIZE,
                        y * config.CELL_SIZE,
                        config.CELL_SIZE,
                        config.CELL_SIZE
                    ))
                    last_cell = (x, y)
                elif state == AppState.PLACING_POINTS:
                    if key_points_placed < 2:
                        grid[y][x] = 2
                        dirty_rects.append(pygame.Rect(
                            x * config.CELL_SIZE,
                            y * config.CELL_SIZE,
                            config.CELL_SIZE,
                            config.CELL_SIZE
                        ))
                        key_points_placed += 1
                        last_cell = (x, y)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_mouse_pressed = False
                last_cell = None
        
    if left_mouse_pressed:
        pos = pygame.mouse.get_pos()
        x = pos[0] // config.CELL_SIZE
        y = pos[1] // config.CELL_SIZE
        if 0 <= x < config.COLS and 0 <= y < config.ROWS:
            if (x, y) != last_cell:
                if state == AppState.DRAWING_WALLS:
                    if grid[y][x] != 2:
                        grid[y][x] = 1
                        dirty_rects.append(pygame.Rect(
                            x * config.CELL_SIZE,
                            y * config.CELL_SIZE,
                            config.CELL_SIZE,
                            config.CELL_SIZE
                        ))
                last_cell = (x, y)
    
    if full_redraw:
        screen.fill(Colors.BLACK)
        dirty_rects = []
        for y in range(config.ROWS):
            for x in range(config.COLS):
                dirty_rects.append(draw_cell(screen, grid, x, y))
        full_redraw = False
        pygame.display.flip()
    else:
        for rect in dirty_rects:
            x = rect.x // config.CELL_SIZE
            y = rect.y // config.CELL_SIZE
            draw_cell(screen, grid, x, y)
        pygame.display.update(dirty_rects)
        dirty_rects = []

pygame.quit()
