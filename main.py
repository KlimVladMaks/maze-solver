import pygame
from find_shortest_path import find_shortest_path
from config import config
from constants import MouseState, Colors
from draw_cell import draw_cell


class MazeSolverApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Решатель лабиринтов: OFF")

        self.grid = [[0 for _ in range(config.COLS)]
                     for _ in range(config.ROWS)]
        self.mouse_state = MouseState.NOT_PRESSED
        self.last_cell = None
        self.key_points_placed = 0
        self.show_solution = False
        self.clock = pygame.time.Clock()
        self.running = True
        self.need_redraw = True
    
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
        
        if self.handle_mouse_drag():
            self.need_redraw = True
    
    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            if not self.show_solution:
                self.show_solution = True
                pygame.display.set_caption("Решатель лабиринтов: ON")
            else:
                self.delete_solution()
                self.show_solution = False
                pygame.display.set_caption("Решатель лабиринтов: OFF")
            self.need_redraw = True
    
    def delete_solution(self):
        for x in range(config.COLS):
            for y in range(config.ROWS):
                if self.grid[y][x] == 3:
                    self.grid[y][x] = 0
    
    def handle_mousebuttondown(self, event):
        if event.button == 1:
            self.mouse_state = MouseState.LEFT_BUTTON_PRESSED
            x, y = self.get_cell_coords(pygame.mouse.get_pos())
            if self.grid[y][x] != 1:
                self.grid[y][x] = 1
                self.need_redraw = True
        
        elif event.button == 2:
            if self.key_points_placed < 2:
                x, y = self.get_cell_coords(pygame.mouse.get_pos())
                if self.grid[y][x] != 2:
                    self.grid[y][x] = 2
                    self.key_points_placed += 1
                    self.need_redraw = True
        
        elif event.button == 3:
            self.mouse_state = MouseState.RIGHT_BUTTON_PRESSED
            x, y = self.get_cell_coords(pygame.mouse.get_pos())
            if self.grid[y][x] != 0 and self.grid[y][x] != 3:
                if self.grid[y][x] == 2:
                    self.key_points_placed -= 1
                self.grid[y][x] = 0
                self.last_cell = (x, y)
                self.need_redraw = True
    
    def handle_mousebuttonup(self, event):
        if event.button == 1 or event.button == 3:
            self.mouse_state = MouseState.NOT_PRESSED
            self.last_cell = None
    
    def handle_mouse_drag(self):
        changed = False
        if self.mouse_state == MouseState.LEFT_BUTTON_PRESSED:
            x, y = self.get_cell_coords(pygame.mouse.get_pos())
            if 0 <= x < config.COLS and 0 <= y < config.ROWS and (x, y) != self.last_cell:
                if self.grid[y][x] != 1:
                    self.grid[y][x] = 1
                    changed = True
                self.last_cell = (x, y)
        elif self.mouse_state == MouseState.RIGHT_BUTTON_PRESSED:
            x, y = self.get_cell_coords(pygame.mouse.get_pos())
            if 0 <= x < config.COLS and 0 <= y < config.ROWS and (x, y) != self.last_cell:
                if self.grid[y][x] != 0 and self.grid[y][x] != 3:
                    if self.grid[y][x] == 2:
                        self.key_points_placed -= 1
                    self.grid[y][x] = 0
                    changed = True
                self.last_cell = (x, y)
        return changed
    
    def get_cell_coords(self, pos):
        return pos[0] // config.CELL_SIZE, pos[1] // config.CELL_SIZE
    
    def render(self):
        if not self.need_redraw:
            return
        
        if self.show_solution:
            self.delete_solution()
            if self.key_points_placed == 2:
                answer = find_shortest_path(self.grid)
                if answer:
                    self.grid = answer
        
        self.screen.fill(Colors.BLACK)
        for y in range(config.ROWS):
            for x in range(config.COLS):
                draw_cell(self.screen, self.grid, x, y)
        
        pygame.display.flip()
        self.need_redraw = False
    
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.render()
        
        pygame.quit()

if __name__ == "__main__":
    app = MazeSolverApp()
    app.run()
