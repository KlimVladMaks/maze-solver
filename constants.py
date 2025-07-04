from enum import Enum, auto
import pygame

class MouseState(Enum):
    LEFT_BUTTON_PRESSED = auto()
    RIGHT_BUTTON_PRESSED = auto()
    NOT_PRESSED = auto()

class Colors:
    BLACK = pygame.Color(0, 0, 0)
    GRAY = pygame.Color(100, 100, 100)
    LIGHT_GREY = pygame.Color(50, 50, 50)
    YELLOW = pygame.Color(255, 255, 0)
    GREEN = pygame.Color(0, 255, 0)
