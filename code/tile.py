import pygame
from settings import *

class Grid(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/level/grid.jpg')
        self.rect = self.image.get_rect(bottomleft = pos)

class Border(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/level/border.jpg')
        self.rect = self.image.get_rect(bottomleft = pos)

