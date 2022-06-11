import pygame

from settings import *
from states.state import *
from states.level import *

class Menu(State):
    def __init__(self, app):
        super().__init__(app)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.app.state = Level(self.app)

    def update(self):
        pass


    def draw(self):
        self.app.screen.fill(BLACK)
        self.app.draw_text("PRESS SPACEBAR", [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, ORANGE, START_FONT, True)
        self.app.draw_text("GABRIEL KRÓL", [WIDTH//2, HEIGHT//2+60], START_TEXT_SIZE, AQUAMARINE, START_FONT, True)
        self.app.draw_text("HIGH SCORE", [4, 4], START_TEXT_SIZE, WHITE, START_FONT)
        pygame.display.update()