import pygame, sys, copy
from settings import *
from player_class import *
from enemy_class import *

pygame.init()
# vector is used to calculate acceleration and other cool stuff
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'

        
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS

        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None

        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            # states
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == "game over":
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


######### HELP FUNCTIONS #########

    def draw_text(self, message, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(message, True, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        self.screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file and creating collision map
        with open("walls.txt", "r") as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = vec(xidx, yidx)
                    elif char in ("2", "3", "4", "5"):
                        self.e_pos.append([xidx,yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height, self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))


    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))

        for wall in self.walls:
            pygame.draw.rect(self.background, RED, (wall.x * self.cell_width, wall.y * self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos =  vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", "r") as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

######### START FUNCTIONS #########

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass


    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("PRESS SPACEBAR", [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, ORANGE, START_FONT, True)
        self.draw_text("GABRIEL KRÓL", [WIDTH//2, HEIGHT//2+60], START_TEXT_SIZE, AQUAMARINE, START_FONT, True)
        self.draw_text("HIGH SCORE", [4, 4], START_TEXT_SIZE, WHITE, START_FONT)
        pygame.display.update()




######### PLAYING FUNCTIONS #########

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-STEP,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(STEP,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-STEP))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,STEP))


    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()



    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_MARGIN//2, TOP_BOTTOM_MARGIN//2))
        self.draw_coins()
        if DEBUG_MODE:
            self.draw_grid()
        self.draw_text(f"CURRENT SCORE: {self.player.current_score}", [60, 0], 18, WHITE, START_FONT)
        self.draw_text(f"HIGH SCORE: {0}", [WIDTH//2+60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            # pygame.draw.rect(self.background, RED, (coin.x * self.cell_width, coin.y * self.cell_height, self.cell_width, self.cell_height))
            pygame.draw.circle(self.screen, WHITE, (int(coin.x * self.cell_width+ self.cell_width//2 + TOP_BOTTOM_MARGIN//2), int(coin.y * self.cell_height  + self.cell_height//2 + TOP_BOTTOM_MARGIN//2)), 5)


######### GAME OVER FUNCTIONS #########

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = 'false'
    
    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACEBAR to TRY AGAIN"
        self.draw_text("GAME OVER", [WIDTH//2, 100], 42, RED, "arial", centered=True)
        self.draw_text(again_text, [WIDTH//2, HEIGHT//2], 40, WHITE, "arial", centered=True)
        self.draw_text(quit_text, [WIDTH//2, HEIGHT//1.5], 38, YELLOW, "arial", centered=True)
        pygame.display.update()
