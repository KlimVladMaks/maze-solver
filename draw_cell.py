import pygame
from config import config
from constants import Colors

def draw_cell(surface, grid, x, y):
    rect = pygame.Rect(
        x * config.CELL_SIZE,
        y * config.CELL_SIZE,
        config.CELL_SIZE,
        config.CELL_SIZE
    )
    
    color_map = {
        0: Colors.BLACK,
        1: Colors.GRAY,
        2: Colors.YELLOW,
        3: Colors.GREEN
    }
    
    pygame.draw.rect(surface, color_map[grid[y][x]], rect)
    pygame.draw.rect(surface, Colors.LIGHT_GREY, rect, 1)
