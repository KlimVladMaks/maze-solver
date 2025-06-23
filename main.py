import pygame
from dataclasses import dataclass
from find_shortest_path import find_shortest_path

pygame.init()

@dataclass
class Config:
    CELL_SIZE: int = 10
    ROWS: int = 60
    COLS: int = 120
    WIDTH: int = COLS * CELL_SIZE
    HEIGHT: int = ROWS * CELL_SIZE
config = Config()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Решатель лабиринтов")

@dataclass
class Colors:
    BLACK = pygame.Color(0, 0, 0)
    GRAY = pygame.Color(100, 100, 100)
    LIGHT_GREY = pygame.Color(50, 50, 50)
    YELLOW = pygame.Color(255, 255, 0)
    GREEN = pygame.Color(0, 255, 0)
colors = Colors()

grid = [[0 for _ in range(config.COLS)] for _ in range(config.ROWS)]

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
                x = pos[0] // config.CELL_SIZE
                y = pos[1] // config.CELL_SIZE
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
        x = pos[0] // config.CELL_SIZE
        y = pos[1] // config.CELL_SIZE
        # Проверяем, что координаты в пределах сетки
        if 0 <= x < config.COLS and 0 <= y < config.ROWS:
            # Избегаем повторной закраски одной и той же клетки
            if (x, y) != last_cell:
                if drawing_walls:
                    if grid[y][x] != 2:  # Не затираем точки
                        grid[y][x] = 1
                last_cell = (x, y)

    screen.fill(colors.BLACK)
    for y in range(config.ROWS):
        for x in range(config.COLS):
            color = colors.BLACK
            if grid[y][x] == 1:
                color = colors.GRAY
            elif grid[y][x] == 2:
                color = colors.YELLOW
            elif grid[y][x] == 3:
                color = colors.GREEN
            pygame.draw.rect(screen, color,
                             (x * config.CELL_SIZE, y * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE))
            pygame.draw.rect(screen, colors.LIGHT_GREY,
                             (x * config.CELL_SIZE, y * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE), 1)
    
    pygame.display.flip()

pygame.quit()
