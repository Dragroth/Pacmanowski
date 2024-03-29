import pygame

from random import choice
from entities.enemy import *
from entities.player import *
from states.state import *


vector = pygame.math.Vector2

class Level(State):
    def __init__(self, app):
        super().__init__(app)
        pygame.mixer.music.stop()
        self.load_music()

        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.walls = []
        self.coins = []
        self.fruits = []
        self.enemies = []
        # Stores position of enemies
        self.e_pos = []
        # Stores position of a player
        self.p_pos = None

        self.load()
        self.player = Player(self.app, self, vector(self.p_pos))

        # Loading enemies
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self.app, self, vector(pos), idx))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if self.player.beast_mode > 0:
                    self.player.beast_mode -= 1
                    print(self.player.beast_mode)
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.load_music()
                self.change_state = 'Main_menu'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vector(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vector(1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vector(0,-1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vector(0,1))


    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        if self.player.beast_mode == 0:
            self.stop_beast_mode()

        
        # Collision occurs
        for enemy in self.enemies:
            if enemy.grid_position == self.player.grid_position:
                if self.player.beast_mode > 0 and enemy.color == BLUE:
                    enemy.get_eaten()
                    self.app.current_score += 5
                else:
                    self.remove_life()



    def draw(self):
        self.app.screen.fill(BLACK)
        self.app.screen.blit(self.background, (TOP_BOTTOM_MARGIN//2, TOP_BOTTOM_MARGIN//2))
        self.draw_coins()
        self.draw_fruits()
        if DEBUG_MODE:
            self.draw_grid()
        self.draw_text(self.app.screen, f"CURRENT SCORE: {self.app.current_score}", [60, 0], 18, WHITE, START_FONT)
        self.draw_text(self.app.screen, f"HIGH SCORE: {0}", [WIDTH//2+60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()


    def load(self):
        self.background = pygame.image.load('assets/images/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file and creating collision map
        with open("assets/walls.txt", "r") as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vector(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vector(xidx, yidx))
                    elif char == "P":
                        self.p_pos = vector(xidx, yidx)
                    elif char in ("2", "3", "4", "5"):
                        self.e_pos.append([xidx,yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*CELL_WIDTH, yidx*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                    elif char == "F":
                        self.fruits.append(vector(xidx, yidx))


    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.change_state = "Game_over"
        else:
            self.player.grid_position = vector(self.player.starting_position)
            self.player.pixel_position = self.player.get_pixel_position()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.get_eaten()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.app.screen, WHITE, (int(coin.x * CELL_WIDTH+ CELL_WIDTH//2 + TOP_BOTTOM_MARGIN//2), int(coin.y * CELL_HEIGHT  + CELL_HEIGHT//2 + TOP_BOTTOM_MARGIN//2)), 4)

    def draw_fruits(self):
        for fruit in self.fruits:
            pygame.draw.circle(self.app.screen, WHITE, (int(fruit.x * CELL_WIDTH+ CELL_WIDTH//2 + TOP_BOTTOM_MARGIN//2), int(fruit.y * CELL_HEIGHT  + CELL_HEIGHT//2 + TOP_BOTTOM_MARGIN//2)), 7)

    def draw_grid(self):
        for x in range(WIDTH//CELL_WIDTH):
            pygame.draw.line(self.background, GREY, (x*CELL_WIDTH, 0), (x*CELL_WIDTH, HEIGHT))
        
        for x in range(HEIGHT//CELL_HEIGHT):
            pygame.draw.line(self.background, GREY, (0, x*CELL_HEIGHT), (WIDTH, x*CELL_HEIGHT))

        if PRINT_WALLS:
            for wall in self.walls:
                pygame.draw.rect(self.background, RED, (wall.x * CELL_WIDTH, wall.y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    def load_music(self):
        pygame.mixer.music.load(choice(LEVEL_MUSIC))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.app.volume)

    def start_beast_mode(self):
        if self.player.beast_mode > 0:
            self.player.beast_mode += 3
        else:
            self.player.beast_mode = 5
        for enemy in self.enemies:
            enemy.set_personality(beast_mode=True)
            enemy.set_color(beast_mode=True)


    def stop_beast_mode(self):
        for enemy in self.enemies:
            enemy.set_personality(beast_mode=False)
            enemy.set_color(beast_mode=False)
