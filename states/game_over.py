import pygame

from settings import *
from states.state import *

class Game_over(State):
    def __init__(self, app):
        super().__init__(app)
        self.fail_sound = pygame.mixer.Sound("assets/sounds/fail.wav")
        self.fail_sound.play()
        with open("scores.txt", "a") as fa:
            fa.write(str(self.app.current_score) + "\n")
            

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.fail_sound.stop()
                self.change_state = "Menu"
    
    def update(self):
        ...

    def draw(self):
        self.app.screen.fill(BLACK)
        quit_text = "Press the ESCAPE to QUIT"
        score_text = "YOUR SCORE: " + str(self.app.current_score)
        again_text = "Press SPACEBAR to go back to main MENU"
        self.app.draw_text("GAME OVER", [WIDTH//2, 100], 84, RED, "arial bold", centered=True)
        self.app.draw_text(score_text, [WIDTH//2, 180], 42, WHITE, "arial", centered=True)
        self.app.draw_text(again_text, [WIDTH//2, HEIGHT-150], 20, AQUAMARINE, "arial", centered=True)
        self.app.draw_text(quit_text, [WIDTH//2, HEIGHT-50], 20, AQUAMARINE, "arial", centered=True)
        pygame.display.update()