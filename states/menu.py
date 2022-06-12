import enum
import pygame

from settings import *
from states.state import *

class Menu(State):

    def __init__(self, app):
        super().__init__(app)
        self.button_width = 200
        self.button_height = 50
        self.buttons = ("start", "options", "exit")
        self.functions = (self.start, self.options, self.exit)
        self.selected = 0
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.functions[self.selected]()
                # self.change_state = "Level"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)

    def update(self):
        ...

    def draw(self):
        self.app.screen.fill(BLACK)

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
            self.app.draw_text(button_text.upper(), [WIDTH//2, 80*idx+120 + self.button_height//2], 26, WHITE, START_FONT, True)

        pygame.display.update()


    def start(self):
        self.change_state = "Level"

    def options(self):
        print("options")

    def exit(self):
        self.app.running = False