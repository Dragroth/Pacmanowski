import pygame

from settings import *
from states.state import *

class Menu(State):

    def __init__(self, app):
        super().__init__(app)
        pygame.mixer.music.load("assets/sounds/dziki_zachod.wav")
        pygame.mixer.music.play(loops=-1)
        self.button_width = 200
        self.button_height = 50

        self.menu = "main_menu"
        self.buttons = []
        self.functions = []

        self.selected = 0

        self.main_menu()
        self.high_scores = []
        
        self.app.current_score = 0
    
    def events(self):
        for event in pygame.event.get():
            # If the player clicks escape key we exit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.go_back()
            # If the player clicks space we run currently selected option
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                self.functions[self.selected]()
            # Changing selected option
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)

    def update(self):
        ...

    def draw(self):
        self.app.screen.fill(BLACK)

        if self.menu == "high_scores":
            self.app.draw_text("HIGH SCORES", [WIDTH//2, 50], 48, WHITE, START_FONT, True)
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
                self.app.draw_text(button_text.upper(), [WIDTH//2, 80*idx+120 + self.button_height//2], 24, WHITE, START_FONT, True)


                for idx, score in enumerate(self.high_scores[:10]):
                    print(idx, score)


        else:    
            # Drawing main menu's top texts
            self.app.draw_text("PACMANOWSKI", [WIDTH//2, 30], 48, ORANGE, START_FONT, True)
            self.app.draw_text("A simple Pac-Man game written in Python", [WIDTH//2, 58], 16, ORANGE, START_FONT, True)

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
                self.app.draw_text(button_text.upper(), [WIDTH//2, 80*idx+120 + self.button_height//2], 24, WHITE, START_FONT, True)

        pygame.display.update()


    def start(self):
        self.change_state = "Level"

    def main_menu(self):
        self.selected = 0
        self.menu = "main_menu"
        self.buttons = ["start", "high scores" ,"options", "exit"]
        self.functions = [self.start, self.high_scores, self.options, self.go_back]

    def options(self):
        self.selected = 0
        self.menu = "options"
        self.buttons = ["go back"]
        self.functions = [self.go_back]

    def high_scores(self):
        self.selected = 0
        self.menu = "high_scores"
        self.buttons = ["go back"]
        self.functions = [self.go_back]

        with open("scores.txt", "r") as fr:
            high_scores = fr.read().splitlines()
            for i in range(0, len(self.high_scores)):
                self.high_scores[i] = int(self.high_scores[i])
            self.high_scores.sort(reverse=True)

        
    def go_back(self):
        self.selected = 0
        if self.menu == "main_menu":
            self.app.running = False
        self.main_menu()