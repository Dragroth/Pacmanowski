import pygame

from states.menus import *

class Main_menu(Menus):
    def __init__(self, app):
        super().__init__(app)
        self.selected = 0
        self.buttons = ["start", "high scores" ,"options", "credits", "exit"]
        self.functions = [self.start, self.high_scores, self.options, self.credits, self.go_back]

    def draw(self):
        super().draw()
        # Drawing main menu's top texts
        self.draw_text(self.app.screen, "PACMANOWSKI", [WIDTH//2, 30], 48, ORANGE, START_FONT, True)
        self.draw_text(self.app.screen, "A simple Pac-Man game written in Python", [WIDTH//2, 58], 16, ORANGE, START_FONT, True)
        # Displaying buttons and their text
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

        pygame.display.update()


    def start(self):
        self.change_state = "Level"

    def options(self):
        self.change_state = "Options"

    def high_scores(self):
        self.change_state = "High_scores"

    def credits(self):
        print("credits")
    
    def go_back(self):
        self.app.running = False