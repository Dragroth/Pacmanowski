import pygame, sys
from settings import *
from entities.player import *
from entities.enemy import *
from states.menu import *
from states.level import *
from states.game_over import *

pygame.init()

states = {'Menu': Menu, 'Level': Level, 'Game_over': Game_over}
vector = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        # The game is based on states, to decide which fragment of code should be run
        self.running = True
        self.state = Menu(self)
        
    def run(self):
        while self.running:
            # states
            if isinstance(self.state, State):
                if self.state.change_state in states:
                    self.state = states[self.state.change_state](self)
                self.state.events()
                self.state.update()
                self.state.draw()
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