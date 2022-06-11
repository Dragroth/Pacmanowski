import pygame

from settings import *


vector = pygame.math.Vector2

class Entity(pygame.sprite.Sprite):
    """Entities are all the moving instances of an object on a map"""
    def __init__(self, app, init_position):
        super().__init__()
        # Passing app to access it's properties
        self.app = app
        # We store position of entities in two different ways
        # Grid position is used to simplyfy collisions and allow grid movement, it's based on [x, y] list
        self.grid_position = init_position
        # Pixel position is used to allow smooth movement, it's stored in vector(x, y)
        self.pixel_position = self.get_pixel_position()
        self.starting_position = [init_position.x, init_position.y]
        self.direction = vector(0,0)


    def update(self):
        # Setting grid position in reference to pixel position
        self.grid_position[0] = (self.pixel_position[0] - TOP_BOTTOM_MARGIN//2)//self.app.cell_width
        self.grid_position[1] = (self.pixel_position[1] - TOP_BOTTOM_MARGIN//2)//self.app.cell_height
        

    def get_pixel_position(self):
        """Gets pixel position based on initial grid position, passed when creating new instance"""
        return vector((self.grid_position.x * self.app.cell_width) + TOP_BOTTOM_MARGIN//2 + self.app.cell_width/2, (self.grid_position.y * self.app.cell_height) + TOP_BOTTOM_MARGIN//2 + self.app.cell_height//2)

    def stay_in_grid(self):
        """"Checks whether it's okay to change direction, to stay in grid"""
        # If the entity is moving in the x axis, or standing still
        if self.direction == vector(1,0) or self.direction == vector(-1,0) or self.direction == vector(0,0):
        # If the entity is in the middle of a cell in x axis
            if int(self.pixel_position.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width == 0:
                # It's okay to move
                return True
        # If the entity is moving in the y axis, or standing still
        if self.direction == vector(0,1) or self.direction == vector(0,-1) or self.direction == vector(0,0):
            # If the entity is in the middle of a cell in y axis
            if int(self.pixel_position.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height == 0:
                # It's okay to move
                return True

