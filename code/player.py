import pygame
from pygame.math import Vector2
from settings import *

class Player():
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.body = [Vector2(15,28)]
        self.speed = 1
        self.lives = 2
        self.direction = Vector2(0,-1)
        self.alive = True

        self.player_up = pygame.image.load('../graphics/player/player_up.png').convert_alpha()
        self.player_down = pygame.image.load('../graphics/player/player_down.png').convert_alpha()
        self.player_right = pygame.image.load('../graphics/player/player_right.png').convert_alpha()
        self.player_left = pygame.image.load('../graphics/player/player_left.png').convert_alpha()

        self.player_beam_v = pygame.image.load('../graphics/player/beam_vertical.png').convert_alpha()
        self.player_beam_h = pygame.image.load('../graphics/player/beam_horizontal.png').convert_alpha()

        self.player_beam_l_u = pygame.image.load('../graphics/player/beam_l_u.png').convert_alpha()
        self.player_beam_r_u = pygame.image.load('../graphics/player/beam_r_u.png').convert_alpha()
        self.player_beam_u_l = pygame.image.load('../graphics/player/beam_u_l.png').convert_alpha()
        self.player_beam_u_r = pygame.image.load('../graphics/player/beam_u_r.png').convert_alpha()
        
    def draw_player(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            body_rect = pygame.Rect(x_pos , y_pos , CELL_SIZE, CELL_SIZE)

            if index == 0:
                if self.direction.x == -1:
                    self.screen.blit(self.player_left, body_rect)
                if self.direction.x == 1:
                    self.screen.blit(self.player_right, body_rect)
                if self.direction.y == -1:
                    self.screen.blit(self.player_up, body_rect)
                if self.direction.y == 1:
                    self.screen.blit(self.player_down, body_rect)
            elif index == len(self.body) - 1:
                pass
            else:
                pre_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if pre_block.x == next_block.x:
                    self.screen.blit(self.player_beam_v, body_rect)
                elif pre_block.y == next_block.y:
                    self.screen.blit(self.player_beam_h, body_rect)
                else:
                    if (pre_block.x == -1 and next_block.y == -1) or (pre_block.y == -1 and next_block.x == -1):
                        self.screen.blit(self.player_beam_r_u, body_rect)
                    if (pre_block.x == -1 and next_block.y == 1) or (pre_block.y == 1 and next_block.x == -1):
                        self.screen.blit(self.player_beam_u_l, body_rect)
                    if (pre_block.x == 1 and next_block.y == -1) or (pre_block.y == -1 and next_block.x == 1):
                        self.screen.blit(self.player_beam_l_u, body_rect)
                    if (pre_block.x == 1 and next_block.y == 1) or (pre_block.y == 1 and next_block.x == 1):
                        self.screen.blit(self.player_beam_u_r, body_rect)

    def move_player(self):
        if self.speed == 1:
            if len(self.body) >= BEAM_SIZE:
                body_copy = self.body[:-1]
                body_copy.insert(0 , body_copy[0] + self.direction)
                self.body = body_copy[:]
            else:
                body_copy = self.body[:]
                body_copy.insert(0 , body_copy[0] + self.direction)
                self.body = body_copy[:]
        
    def player_keys(self, event):
        if self.speed == 1:
            if event.key == pygame.K_UP and self.direction != Vector2(0,1):
                self.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and self.direction != Vector2(0,-1):
                self.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and self.direction != Vector2(1,0):
                self.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and self.direction != Vector2(-1,0):
                self.direction = Vector2(1,0)

    def kill_player(self):
        self.alive = False
        self.speed = 0

        images = []
        for i in range(1, 6):
            img = pygame.image.load(f'../graphics/level/explosion{i}.png').convert_alpha()
            images.append(img)
        index = 0
        exp_rect = pygame.Rect((self.body[0].x * CELL_SIZE) , (self.body[0].y * CELL_SIZE) , CELL_SIZE, CELL_SIZE)
        
        for i in images:
            image = images[index]
            self.screen.blit(image, exp_rect)
            index += 1
    

    def player_collision(self):
        if self.alive == True:
            if self.body[0] in self.body[1:]:
                self.kill_player()

            if self.body[0].x < 2 or self.body[0].x > CELL_NUMBER - 4:
                self.kill_player()
            if self.body[0].y < 3 or self.body[0].y > CELL_NUMBER - 2:
                self.kill_player()