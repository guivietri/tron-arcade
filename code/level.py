import pygame
from os import path
from tile import Border, Grid
from settings import *


class Level:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.fin = path.dirname(__file__)
        with open(path.join(self.fin, 'HS_FILE'), 'r') as file:
            try:
                self.highscore = int(file.read())
            except:
                self.highscore = 0

        self.visibles_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        
        self.draw_map()

    def draw_map(self):
        for row_index, row in enumerate(GRID):
            for col_index, col in enumerate(row):
                x = col_index * CELL_SIZE
                y = row_index * CELL_SIZE
                if col == 'g':
                    Grid((x,y),[self.visibles_sprites])
                if col == 'b':
                    Border((x,y),[self.visibles_sprites,self.obstacles_sprites])

    def hs_update(self,score):
        self.fin = path.dirname(__file__)
        with open(path.join(self.fin, 'HS_FILE'), 'w') as file:
            file.write(str(score))
                

    def run(self):
        self.visibles_sprites.draw(self.display_surf)
        self.visibles_sprites.update()
