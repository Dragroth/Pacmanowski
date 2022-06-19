import pygame, sys
from random import choice

from settings import *
from entities.player import *
from entities.enemy import *
from states.level import *
from states.game_over import *
from states.main_menu import *
from states.options import *
from states.high_scores import *

pygame.init()

# Used to change states in one place, instead of importing stuff and complicating things
states = {'Main_menu': Main_menu, 'Options': Options, "High_scores": High_scores , 'Level': Level, 'Game_over': Game_over}
vector = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        with open("settings.txt", "r") as fr:
            temp = fr.read()
            if temp == "":
                temp = 1
            self.volume = float(temp)

        self.load_music()

        # The game is based on states, to decide which fragment of code should be run
        self.running = True
        self.state = Main_menu(self)

        self.current_score = 0
        
    def run(self):
        while self.running:
            # states
            if isinstance(self.state, State):
                # Checks whether we want to change a state
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

    def load_music(self):
        pygame.mixer.music.load(choice(MAIN_MENU_MUSIC))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.volume)
        