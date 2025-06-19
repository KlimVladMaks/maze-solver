import pygame
from find_shortest_path import find_shortest_path

pygame.init()

CELL_SIZE = 20
ROWS = 35
COLS = 35
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Решатель лабиринтов")

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

running = True
drawing_walls = True
number_of_key_points = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if drawing_walls:
                        print("Переход к выбору входа/выхода")
                        drawing_walls = False
                    else:
                        print("Ввод завершён")
                        grid = find_shortest_path(grid)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                x = pos[0] // CELL_SIZE
                y = pos[1] // CELL_SIZE
                if drawing_walls:
                    grid[y][x] = 1
                elif number_of_key_points < 2:
                    grid[y][x] = 2
                    number_of_key_points += 1
    
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            color = BLACK
            if grid[y][x] == 1:
                color = GRAY
            elif grid[y][x] == 2:
                color = YELLOW
            elif grid[y][x] == 3:
                color = GREEN
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (50, 50, 50), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    
    pygame.display.flip()

pygame.quit()
