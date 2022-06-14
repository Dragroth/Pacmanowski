from entities.entity import *
import pygame, os

vector = pygame.math.Vector2

class Player(Entity):
    """"A player is a special kind of entity that is controlled and allows collecting points"""
    def __init__(self, app, level, init_position):
        super().__init__(app, level, init_position)
        self.stored_direction = None
        self.direction = vector(0,1)

        self.eat_sound = pygame.mixer.Sound("assets/sounds/eat.wav")
        self.eat_sound.set_volume(self.app.volume)
        
        self.image = PLAYER_STAND_LIST
        self._count = 0

        self.able_to_move = False
        self.speed = 2
        self.lives = 3

    def update(self):
        # If everything is fine, we move the player in direction it's facing in pixels
        if self.able_to_move:
            self.pixel_position += self.direction * self.speed
        else:
            self._count = 0
            self.image = PLAYER_STAND_LIST
        # If we're in a middle of a grid, we can try to change direction
        if self.stay_in_grid():
            # But only, if the player wants it
            if self.stored_direction != None:
                if self.stored_direction == (1,0):
                    self.image = PLAYER_WALK_LIST_R
                elif self.stored_direction == (-1,0):
                    self.image = PLAYER_WALK_LIST_L
                elif self.stored_direction == (0,1):
                    self.image = PLAYER_WALK_LIST_B
                elif self.stored_direction == (0,-1):
                    self.image = PLAYER_WALK_LIST_T

                self.direction = self.stored_direction

                self.stored_direction = None
            # It's also a good time to check, if the player can keep going it this direction
            self.able_to_move = self.can_move(self.direction)

        super().update()

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # Drawing player model
        # pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pixel_position.x), int(self.pixel_position.y)), CELL_WIDTH//2-2)
    
        temp = self.image[self._count//(2*len(self.image))]
        self._count = (self._count + 1) % (8*len(self.image))
        
        self.app.screen.blit(temp, (int(self.pixel_position.x) - CELL_WIDTH//2+2, int(self.pixel_position.y) - CELL_HEIGHT//2+2))
        

        # Drawing lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, (30 + 20*x, HEIGHT - 15), 7)

        # Drawing pixel position on a grid map
        if DEBUG_MODE:
            pygame.draw.rect(self.app.screen, RED, (self.grid_position[0]*CELL_WIDTH+TOP_BOTTOM_MARGIN//2, self.grid_position[1] * CELL_HEIGHT + TOP_BOTTOM_MARGIN//2, CELL_WIDTH, CELL_HEIGHT), 1)

    def on_coin(self):
        if self.grid_position in self.level.coins:
            if int(self.pixel_position.x+TOP_BOTTOM_MARGIN//2) % CELL_WIDTH == 0:
                if self.direction == vector(STEP,0) or self.direction == vector(-STEP,0):
                    return True
            if int(self.pixel_position.y+TOP_BOTTOM_MARGIN//2) % CELL_HEIGHT == 0:
                if self.direction == vector(0,STEP) or self.direction == vector(0,-STEP):
                    return True
        return False

    def eat_coin(self):
        self.level.coins.remove(self.grid_position)
        self.app.current_score += 1
        self.eat_sound.play()

    def can_move(self, direction):
        """Check if there is wall in the passed direction"""
        for wall in self.level.walls:
            if vector(self.grid_position + direction) == wall:
                return False
        return True

    def move(self, my_direction):
        """Informs the game that the player wants to change directions (and that's it)"""
        self.stored_direction = my_direction