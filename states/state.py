import pygame, abc

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