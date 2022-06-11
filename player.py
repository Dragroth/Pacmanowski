from entity import *
import pygame

vector = pygame.math.Vector2

class Player(Entity):
    def __init__(self, app, init_position):
        super().__init__(app, init_position)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 1

    def update(self):
        if self.able_to_move:
            self.pixel_position += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction 
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix pos
        self.grid_position[0] = (self.pixel_position[0] - TOP_BOTTOM_MARGIN//2)//self.app.cell_width
        self.grid_position[1] = (self.pixel_position[1] - TOP_BOTTOM_MARGIN//2)//self.app.cell_height

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # Drawing player model
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pixel_position.x), int(self.pixel_position.y)), self.app.cell_width//2-2)


        # Drawing lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, (30 + 20*x, HEIGHT - 15), 7)


        # Drawing pix pos on a grid map
        if DEBUG_MODE:
            pygame.draw.rect(self.app.screen, RED, (self.grid_position[0]*self.app.cell_width+TOP_BOTTOM_MARGIN//2, self.grid_position[1] * self.app.cell_height + TOP_BOTTOM_MARGIN//2, self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_position in self.app.coins:
            if int(self.pixel_position.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width == 0:
                if self.direction == vec(STEP,0) or self.direction == vec(-STEP,0):
                    return True
            if int(self.pixel_position.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height == 0:
                if self.direction == vec(0,STEP) or self.direction == vec(0,-STEP):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_position)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def time_to_move(self):
        """"Checks whether it's okay to change direction, to stay in grid"""
        if int(self.pixel_position.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width == 0:
            if self.direction == vec(STEP,0) or self.direction == vec(-STEP,0) or self.direction == vec(0,0):
                return True
        if int(self.pixel_position.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height == 0:
            if self.direction == vec(0,STEP) or self.direction == vec(0,-STEP) or self.direction == vec(0,0):
                return True


    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_position + self.direction) == wall:
                return False
        return True