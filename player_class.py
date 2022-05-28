from settings import *
import pygame

vec = pygame.math.Vector2

class Player:
    def __init__(self, app,  pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1,0)
        print(self.grid_pos, self.pix_pos)
        

    def update(self):
        self.pix_pos += self.direction

        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_MARGIN//2)//self.app.cell_width
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_MARGIN//2)//self.app.cell_height

    def draw(self):
        # Drawing player model
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width//2-2)


        # Drawing pix pos on a grid map
        pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_MARGIN//2, self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_MARGIN//2, self.app.cell_width, self.app.cell_height), 1)

    def move(self, direction):
        self.direction = direction

    def get_pix_pos(self):
        """Gets pixel position based on initial grid position, passed when creating new instance"""
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_MARGIN//2+self.app.cell_width/2, (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_MARGIN//2 + self.app.cell_height//2)