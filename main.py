import pygame
from find_shortest_path import find_shortest_path
from config import config
from constants import AppState, MouseState, Colors
from draw_cell import draw_cell


class MazeSolverApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Решатель лабиринтов")

        self.grid = [[0 for _ in range(config.COLS)]
                     for _ in range(config.ROWS)]
        self.app_state = AppState.DRAWING_WALLS
        self.mouse_state = MouseState.NOT_PRESSED
        self.last_cell = None
        self.key_points_placed = 0
        self.dirty_rects = []
        self.full_redraw = True
        self.clock = pygame.time.Clock()
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mousebuttondown(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mousebuttonup(event)
        
        self.handle_mouse_drag()
    
    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            if self.app_state == AppState.DRAWING_WALLS:
                print("Переход к выбору входа/выхода")
                self.app_state = AppState.PLACING_POINTS
            elif self.app_state == AppState.PLACING_POINTS:
                print("Ввод завершён")
                self.app_state = AppState.SOLVING
                answer = find_shortest_path(self.grid)
                if answer:
                    self.grid = answer
                    self.full_redraw = True
    
    def handle_mousebuttondown(self, event):
        if event.button == 1:
            self.mouse_state = MouseState.LEFT_BUTTON_PRESSED
            x, y = self.get_cell_coords(pygame.mouse.get_pos())
            
            if self.app_state == AppState.DRAWING_WALLS:
                self.set_cell_value(x, y, 1)
            elif self.app_state == AppState.PLACING_POINTS and self.key_points_placed < 2:
                self.set_cell_value(x, y, 2)
                self.key_points_placed += 1
            
            self.last_cell = (x, y)
    
    def handle_mousebuttonup(self, event):
        if event.button == 1:
            self.mouse_state = MouseState.NOT_PRESSED
            self.last_cell = None
    
    def handle_mouse_drag(self):
        if self.mouse_state == MouseState.LEFT_BUTTON_PRESSED:
            x, y = self.get_cell_coords(pygame.mouse.get_pos())
            if 0 <= x < config.COLS and 0 <= y < config.ROWS and (x, y) != self.last_cell:
                if self.app_state == AppState.DRAWING_WALLS and self.grid[y][x] != 2:
                    self.set_cell_value(x, y, 1)
                self.last_cell = (x, y)
    
    def get_cell_coords(self, pos):
        return pos[0] // config.CELL_SIZE, pos[1] // config.CELL_SIZE
    
    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value
        self.dirty_rects.append(pygame.Rect(
            x * config.CELL_SIZE,
            y * config.CELL_SIZE,
            config.CELL_SIZE,
            config.CELL_SIZE
        ))
    
    def render(self):
        if self.full_redraw:
            self.screen.fill(Colors.BLACK)
            self.dirty_rects = []
            for y in range(config.ROWS):
                for x in range(config.COLS):
                    self.dirty_rects.append(draw_cell(self.screen, self.grid, x, y))
            self.full_redraw = False
            pygame.display.flip()
        else:
            for rect in self.dirty_rects:
                x = rect.x // config.CELL_SIZE
                y = rect.y // config.CELL_SIZE
                draw_cell(self.screen, self.grid, x, y)
            pygame.display.update(self.dirty_rects)
            self.dirty_rects = []
    
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.render()
        
        pygame.quit()

if __name__ == "__main__":
    app = MazeSolverApp()
    app.run()
