from settings import *
import pygame

vec = pygame.math.Vector2

class Player:
    def __init__(self, app,  pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(STEP,0)
        self.stored_direction = None
        

    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move():
                if self.stored_direction != None:
                    self.direction = self.stored_direction 

        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_MARGIN//2)//self.app.cell_width
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_MARGIN//2)//self.app.cell_height

    def draw(self):
        # Drawing player model
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width//2-2)


        # Drawing pix pos on a grid map
        pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_MARGIN//2, self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_MARGIN//2, self.app.cell_width, self.app.cell_height), 1)

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        """Gets pixel position based on initial grid position, passed when creating new instance"""
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_MARGIN//2+self.app.cell_width/2, (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_MARGIN//2 + self.app.cell_height//2)

    def time_to_move(self):
        """"Checks whether it's okay to change direction, to stay in grid"""
        if int(self.pix_pos.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width == 0:
            if self.direction == vec(STEP,0) or self.direction == vec(-STEP,0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height == 0:
            if self.direction == vec(0,STEP) or self.direction == vec(0,-STEP):
                return True