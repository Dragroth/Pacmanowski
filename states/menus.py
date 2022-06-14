import pygame

from states.state import *

class Menus(State):
    def __init__(self, app):
        super().__init__(app)

        self.button_width = 200
        self.button_height = 50

        self.buttons = []
        self.functions = []

        self.selected = 0

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

    def go_back(self):
        self.change_state = "Main_menu"