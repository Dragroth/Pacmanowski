import abc

from settings import *
from app import *

class State(abc.ABC):
    def __init__(self, app):
        self.app = app
        self.change_state = ""
    
    @abc.abstractmethod
    def events(self):
        ...

    @abc.abstractmethod
    def update(self):
        ...

    @abc.abstractmethod
    def draw(self):
        ...

    def draw_text(self, screen, message, pos, size, color, font_name, centered=False) -> None:
        font = pygame.font.SysFont(font_name, size)
        text = font.render(message, True, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)
