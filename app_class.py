import pygame, sys
from settings import *
from player_class import *

pygame.init()
# vector is used to calculate acceleration and other cool stuff
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'

        
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30

        self.player = Player(self, PLAYER_START_POS)


        self.load()

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
        self.background = pygame.image.load('/home/gkk/Documents/Python/Pacmanowski/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))


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

    def playing_update(self):
        pass


    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_MARGIN//2, TOP_BOTTOM_MARGIN//2))
        self.draw_grid()
        self.draw_text(f"CURRENT SCORE: {0}", [60, 0], 18, WHITE, START_FONT)
        self.draw_text(f"HIGH SCORE: {0}", [WIDTH//2+60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        pygame.display.update()