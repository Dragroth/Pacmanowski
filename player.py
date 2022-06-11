from entity import *
import pygame

vector = pygame.math.Vector2

class Player(Entity):
    """"A player is a special kind of entity that is controlled and allows collecting points"""
    def __init__(self, app, init_position):
        super().__init__(app, init_position)
        self.stored_direction = None
        self.stored_stored_direction = None

        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 1

    def update(self):
        # If everything is fine, we move the player in direction it's facing in pixels
        if self.able_to_move:
            self.pixel_position += self.direction * self.speed
        # If we're in a middle of a grid, we can try to change direction
        if self.stay_in_grid():
            # But only, if the player wants it
            if self.stored_direction != None:
                self.direction = self.stored_direction
            # It's also a good time to check, if the player can keep going it this direction
            self.able_to_move = self.can_move(self.direction)
        super().update()

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # Drawing player model
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pixel_position.x), int(self.pixel_position.y)), self.app.cell_width//2-2)


        # Drawing lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, (30 + 20*x, HEIGHT - 15), 7)

        # Drawing pixel position on a grid map
        if DEBUG_MODE:
            pygame.draw.rect(self.app.screen, RED, (self.grid_position[0]*self.app.cell_width+TOP_BOTTOM_MARGIN//2, self.grid_position[1] * self.app.cell_height + TOP_BOTTOM_MARGIN//2, self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_position in self.app.coins:
            if int(self.pixel_position.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width == 0:
                if self.direction == vector(STEP,0) or self.direction == vector(-STEP,0):
                    return True
            if int(self.pixel_position.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height == 0:
                if self.direction == vector(0,STEP) or self.direction == vector(0,-STEP):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_position)
        self.current_score += 1

    def can_move(self, direction):
        """Check if there is wall in the passed direction"""
        for wall in self.app.walls:
            if vector(self.grid_position + direction) == wall:
                return False
        return True

    def move(self, direction):
        """Informs the game that the player wants to change directions (and that's it)"""
        self.stored_direction = direction