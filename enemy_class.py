import pygame, random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = self.app.cell_width//2.3
        self.number = number
        self.color = self.set_color()
        self.direction = vec(1 ,0)
        self.personality = self.set_personality()

    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move:
            self.move()


    def draw(self):
        pygame.draw.circle(self.app.screen, self.color, (int(self.pix_pos.x), int(self.pix_pos.y)) , self.radius)

    def time_to_move(self):
        """"Checks whether it's okay to change direction, to stay in grid"""
        if int(self.pix_pos.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width == 0:
            if self.direction == vec(STEP,0) or self.direction == vec(-STEP,0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height == 0:
            if self.direction == vec(0,STEP) or self.direction == vec(0,-STEP):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            number = random.random()

    def get_pix_pos(self):
        """Gets pixel position based on initial grid position, passed when creating new instance"""
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_MARGIN//2+self.app.cell_width/2, (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_MARGIN//2 + self.app.cell_height//2)

    def set_color(self):
        if self.number == 0:
            return BLUE
        elif self.number == 1:
            return YELLOW
        elif self.number == 2:
            return RED
        elif self.number == 3:
            return ORANGE

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"

    