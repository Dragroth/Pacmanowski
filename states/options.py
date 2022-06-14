import pygame

from states.menus import *

class Options(Menus):
    def __init__(self, app):
        super().__init__(app)
        self.selected = 0
        self.buttons = ["go back", "mute/unmute"]
        self.functions = [self.go_back, self.mute]

    def draw(self):
        super().draw()
        self.app.draw_text("OPTIONS", [WIDTH//2, 50], 48, WHITE, START_FONT, True)
        for idx, button_text in enumerate(self.buttons):
            button = (WIDTH//2-self.button_width//2, 80*idx+120, self.button_width, self.button_height)
            if idx == self.selected:
                color = LIGHTGREY
            else:
                color = GREY
            if idx == 1:
                if self.app.volume == 1:
                    color = GREEN
                else:
                    color = RED
            pygame.draw.rect(self.app.screen, color, button)
            # Drawing text inside of the rectangle
            self.app.draw_text(button_text.upper(), [WIDTH//2, 80*idx+120 + self.button_height//2], 24, WHITE, START_FONT, True)
        
        pygame.display.update()

    def mute(self):
        if self.app.volume == 0:
            self.app.volume = 1
        else:
            self.app.volume = 0

        with open("settings.txt", "w") as fw:
            fw.write(str(self.app.volume))
        pygame.mixer.music.set_volume(self.app.volume)