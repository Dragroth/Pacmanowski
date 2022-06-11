import pygame

from settings import *


vector = pygame.math.Vector2

class Entity(pygame.sprite.Sprite):
    """Entities are all the moving instances of an object on a map"""
    def __init__(self, app, init_position):
        super().__init__()
        self.app = app
        self.grid_position = init_position
        self.pixel_position = self.get_pixel_position()
        self.starting_position = [init_position.x, init_position.y]
        self.direction = vector(0,0)


    def get_pixel_position(self):
        """Gets pixel position based on initial grid position, passed when creating new instance"""
        return vector((self.grid_position.x * self.app.cell_width) + TOP_BOTTOM_MARGIN//2 + self.app.cell_width/2, (self.grid_position.y * self.app.cell_height) + TOP_BOTTOM_MARGIN//2 + self.app.cell_height//2)

    def time_to_move(self):
        """"Checks whether it's okay to change direction, to stay in grid"""
        if int(self.pixel_position.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width == 0:
            if self.direction == vector(1,0) or self.direction == vector(-1,0) or self.direction == vector(0,0):
                return True
        if int(self.pixel_position.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height == 0:
            if self.direction == vector(0,1) or self.direction == vector(0,-1) or self.direction == vector(0,0):
                return True