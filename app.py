import pygame, sys
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

        self.volume = 1
        pygame.mixer.music.load("assets/sounds/dziki_zachod.wav")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.volume)
        

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


######### HELP FUNCTIONS #########

    def draw_text(self, message, pos, size, color, font_name, centered=False) -> None:
        font = pygame.font.SysFont(font_name, size)
        text = font.render(message, True, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        self.screen.blit(text, pos)