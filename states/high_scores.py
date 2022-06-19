import pygame

from settings import *
from states.menus import *

class High_scores(Menus):
    def __init__(self, app):
        super().__init__(app)
        self.selected = 0
        self.buttons = ["go back"]
        self.functions = [self.go_back]
        self.high_scores_list = []

        with open("scores.txt", "r") as fr:
            self.high_scores_list = fr.read().splitlines()
            for i in range(0, len(self.high_scores_list)):
                self.high_scores_list[i] = int(self.high_scores_list[i])
            self.high_scores_list.sort(reverse=True)

    def draw(self):
        super().draw()

        self.draw_text(self.app.screen, "HIGH SCORES", [WIDTH//2, 50], 48, WHITE, START_FONT, True)
        for idx, button_text in enumerate(self.buttons):
            # Creating tuple that will be used to initiate new rect object
            button = (WIDTH//2-self.button_width//2, 80*idx+120, self.button_width, self.button_height)
            # Setting color based on current selection
            if idx == self.selected:
                color = LIGHTGREY
            else:
                color = GREY
            # Drawing rectangle based on created tuple
            pygame.draw.rect(self.app.screen, color, button)
            # Drawing text inside of the rectangle
            self.draw_text(self.app.screen, button_text.upper(), [WIDTH//2, 80*idx+120 + self.button_height//2], 24, WHITE, START_FONT, True)

        for idx, score in enumerate(self.high_scores_list[:10]):
                self.draw_text(self.app.screen, str(idx+1) + ": " + str(score) + " POINTS", [WIDTH//2, 40*idx+180 + self.button_height//2], 18, WHITE, START_FONT, True)

        pygame.display.update()
