import pygame

from settings import *
from states.menus import *

class Options(Menus):
    def __init__(self, app):
        super().__init__(app)
        self.selected = 0
        self.buttons = ["go back", "volume", "mute/unmute"]
        self.functions = [self.go_back, self.change_volume, self.mute]


    def events(self):
        for event in pygame.event.get():
            # If the player clicks escape key we exit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.go_back()
            # If the player clicks space o enter we run currently selected option
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                self.functions[self.selected]()
            # Changing selected option
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)

            if self.buttons[self.selected] == "volume":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.change_volume(increase=-0.1)
                    if event.key == pygame.K_RIGHT:
                        self.change_volume(increase=0.1)

    def draw(self):
        super().draw()
        self.draw_text(self.app.screen, "OPTIONS", [WIDTH//2, 50], 48, WHITE, START_FONT, True)
        for idx, button_text in enumerate(self.buttons):
            button = (WIDTH//2-self.button_width//2, 80*idx+120, self.button_width, self.button_height)
            if idx == self.selected:
                color = LIGHTGREY
            else:
                color = GREY
            if self.buttons[idx] == "mute/unmute":
                if self.app.volume >= 0.1:
                    color = GREEN
                else:
                    color = RED
            if self.buttons[idx] == "volume":
                button_text = "Volume: " + str(round(self.app.volume * 100)) + "%"
            pygame.draw.rect(self.app.screen, color, button)
            # Drawing text inside of the rectangle
            self.draw_text(self.app.screen, button_text.upper(), [WIDTH//2, 80*idx+120 + self.button_height//2], 24, WHITE, START_FONT, True)
        
        pygame.display.update()

    def mute(self):
        if self.app.volume == 0:
            self.app.volume = 1
        else:
            self.app.volume = 0

        with open("settings.txt", "w") as fw:
            fw.write(str(self.app.volume))
        pygame.mixer.music.set_volume(self.app.volume)

    def change_volume(self, increase = 0):
        self.app.volume = round(self.app.volume + increase, 1)
        pygame.mixer.music.set_volume(self.app.volume)
        if self.app.volume > 1:
            self.app.volume = 1.0
        if self.app.volume < 0:
            self.app.volume = 0.0

        with open("settings.txt", "w") as fw:
            fw.write(str(self.app.volume))
