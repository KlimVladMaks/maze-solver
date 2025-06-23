import pygame
from find_shortest_path import find_shortest_path

pygame.init()

CELL_SIZE = 10
ROWS = 60
COLS = 120
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Решатель лабиринтов")

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GREY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

running = True
drawing_walls = True
number_of_key_points = 0

# Для отслеживания положения мыши
left_mouse_pressed = False
last_cell = None  # Последняя изменённая клетка, чтобы не повторяться

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if drawing_walls:
                    print("Переход к выбору входа/выхода")
                    drawing_walls = False
                else:
                    print("Ввод завершён")
                    answer = find_shortest_path(grid)
                    if grid is not None:
                        grid = answer
                    else:
                        print("Решения не найдено")
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши нажата
                left_mouse_pressed = True
                pos = pygame.mouse.get_pos()
                x = pos[0] // CELL_SIZE
                y = pos[1] // CELL_SIZE
                if drawing_walls:
                    grid[y][x] = 1
                    last_cell = (x, y)
                elif number_of_key_points < 2:
                    grid[y][x] = 2
                    number_of_key_points += 1
                    last_cell = (x, y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка отпущена
                left_mouse_pressed = False
                last_cell = None

    # Если зажата левая кнопка мыши
    if left_mouse_pressed:
        pos = pygame.mouse.get_pos()
        x = pos[0] // CELL_SIZE
        y = pos[1] // CELL_SIZE
        # Проверяем, что координаты в пределах сетки
        if 0 <= x < COLS and 0 <= y < ROWS:
            # Избегаем повторной закраски одной и той же клетки
            if (x, y) != last_cell:
                if drawing_walls:
                    if grid[y][x] != 2:  # Не затираем точки
                        grid[y][x] = 1
                last_cell = (x, y)

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
            pygame.draw.rect(screen, LIGHT_GREY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    
    pygame.display.flip()

pygame.quit()
