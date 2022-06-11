import pygame

from settings import *
from states.state import *

class Game_over(State):
    def __init__(self, app):
        super().__init__(app)
        self.replay = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.change_state = "Menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.running = False
    
    def update(self):
        pass

    def draw(self):
        self.app.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACEBAR to TRY AGAIN"
        self.app.draw_text("GAME OVER", [WIDTH//2, 100], 42, RED, "arial", centered=True)
        self.app.draw_text(again_text, [WIDTH//2, HEIGHT//2], 40, WHITE, "arial", centered=True)
        self.app.draw_text(quit_text, [WIDTH//2, HEIGHT//1.5], 38, YELLOW, "arial", centered=True)
        pygame.display.update()