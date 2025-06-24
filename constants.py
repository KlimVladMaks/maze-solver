from enum import Enum, auto
import pygame

class AppState(Enum):
    DRAWING_WALLS = auto()
    PLACING_POINTS = auto()
    SOLVING = auto()

class Colors:
    BLACK = pygame.Color(0, 0, 0)
    GRAY = pygame.Color(100, 100, 100)
    LIGHT_GREY = pygame.Color(50, 50, 50)
    YELLOW = pygame.Color(255, 255, 0)
    GREEN = pygame.Color(0, 255, 0)