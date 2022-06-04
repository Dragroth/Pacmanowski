import pygame

from settings import *

pygame.init()

vector = pygame.math.Vector2

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def __del__(self):
        pygame.quit()