import pygame, random
from pygame.math import Vector2
from settings import *

class Enemy():
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.body = [Vector2(15,3)]
        self.speed = 1
        self.steps = 0
        self.direction = Vector2(0,1)
        self.alive = True

        self.enemy_up = pygame.image.load('../graphics/enemy/enemy_up.png').convert_alpha()
        self.enemy_down = pygame.image.load('../graphics/enemy/enemy_down.png').convert_alpha()
        self.enemy_right = pygame.image.load('../graphics/enemy/enemy_right.png').convert_alpha()
        self.enemy_left = pygame.image.load('../graphics/enemy/enemy_left.png').convert_alpha()

        self.enemy_beam_v = pygame.image.load('../graphics/enemy/beam_vertical.png').convert_alpha()
        self.enemy_beam_h = pygame.image.load('../graphics/enemy/beam_horizontal.png').convert_alpha()

        self.enemy_beam_l_u = pygame.image.load('../graphics/enemy/beam_l_u.png').convert_alpha()
        self.enemy_beam_r_u = pygame.image.load('../graphics/enemy/beam_r_u.png').convert_alpha()
        self.enemy_beam_u_l = pygame.image.load('../graphics/enemy/beam_u_l.png').convert_alpha()
        self.enemy_beam_u_r = pygame.image.load('../graphics/enemy/beam_u_r.png').convert_alpha() 

    def draw_enemy(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            body_rect = pygame.Rect(x_pos , y_pos , CELL_SIZE, CELL_SIZE)

            if index == 0:
                if self.direction.x == -1:
                    self.screen.blit(self.enemy_left, body_rect)
                if self.direction.x == 1:
                    self.screen.blit(self.enemy_right, body_rect)
                if self.direction.y == -1:
                    self.screen.blit(self.enemy_up, body_rect)
                if self.direction.y == 1:
                    self.screen.blit(self.enemy_down, body_rect)
            elif index == len(self.body) - 1:
                pass
            else:
                pre_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if pre_block.x == next_block.x:
                    self.screen.blit(self.enemy_beam_v, body_rect)
                elif pre_block.y == next_block.y:
                    self.screen.blit(self.enemy_beam_h, body_rect)
                else:
                    if (pre_block.x == -1 and next_block.y == -1) or (pre_block.y == -1 and next_block.x == -1):
                        self.screen.blit(self.enemy_beam_r_u, body_rect)
                    if (pre_block.x == -1 and next_block.y == 1) or (pre_block.y == 1 and next_block.x == -1):
                        self.screen.blit(self.enemy_beam_u_l, body_rect)
                    if (pre_block.x == 1 and next_block.y == -1) or (pre_block.y == -1 and next_block.x == 1):
                        self.screen.blit(self.enemy_beam_l_u, body_rect)
                    if (pre_block.x == 1 and next_block.y == 1) or (pre_block.y == 1 and next_block.x == 1):
                        self.screen.blit(self.enemy_beam_u_r, body_rect)

    def move_enemy(self):
        if self.speed == 1:
            if len(self.body) >= BEAM_SIZE:
                body_copy = self.body[:-1]
                body_copy.insert(0 , body_copy[0] + self.direction)
                self.body = body_copy[:]
            else:
                body_copy = self.body[:]
                body_copy.insert(0 , body_copy[0] + self.direction)
                self.body = body_copy[:]

    def avoid_beam(self):
        try_dir = Vector2(self.direction.y , self.direction.x)
        next_pos = self.body[0] + try_dir
        if (try_dir != - self.direction) and (- try_dir != - self.direction):
            if next_pos in self.body or (next_pos.x > 2 and next_pos.x < CELL_NUMBER - 4) and (next_pos.y > 2 and next_pos.y < CELL_NUMBER - 5):
                self.direction = - try_dir
            else:
                self.direction = try_dir
        return self.direction

    def enemy_direction(self):
        if self.speed != 0 and len(self.body) > random.randint(2,6):
            
            next_pos = Vector2(self.body[0] + self.direction)
            pre_dir = self.direction

            if self.steps < 5:
                 possible_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                 direction_change = Vector2(random.choice(possible_directions))
                 random_pos = self.body[0] + direction_change
                 if random_pos not in self.body and direction_change != (- pre_dir):
                    if (random_pos.x > 2 and random_pos.x < CELL_NUMBER - 4) and (random_pos.y > 2 and random_pos.y < CELL_NUMBER - 2):
                         self.direction = direction_change
                         self.steps = random.randint(1, 20)
                    elif (- direction_change) not in self.body:
                        self.direction = - direction_change
                        self.steps = random.randint(1, 20)

            if next_pos in self.body:
                try_dir = self.avoid_beam()
                if (self.body[0] + try_dir) in self.body and try_dir != (- pre_dir):
                    self.direction = - try_dir
                elif try_dir != (- pre_dir):
                    self.direction = try_dir
                else:
                    pass
            if next_pos.x < 2 or next_pos.x >= CELL_NUMBER - 4 and (next_pos - self.body[0]) != (- pre_dir):
                if self.body[0].y > 15 and next_pos not in self.body:
                    self.direction = Vector2(0,-1)
                elif next_pos not in self.body:
                    self.direction = Vector2(0,1)
                else:
                    pass
            if next_pos.y < 3 or next_pos.y >= CELL_NUMBER - 5 and (next_pos - self.body[0]) != (- self.direction):
                if self.body[0].x > 15 and next_pos not in self.body:
                    self.direction = Vector2(-1,0)
                elif next_pos not in self.body:
                    self.direction = Vector2(1,0)
                else:
                    pass
            

            else:
                self.steps = random.randint(1, 20)

    def kill_enemy(self):
        self.explosion = [pygame.image.load('../graphics/level/explosion1.png').convert_alpha(), 
        pygame.image.load('../graphics/level/explosion2.png').convert_alpha(),
        pygame.image.load('../graphics/level/explosion3.png').convert_alpha(), 
        pygame.image.load('../graphics/level/explosion4.png').convert_alpha(), 
        pygame.image.load('../graphics/level/explosion5.png').convert_alpha()]
        self.alive = False
        self.speed = 0

        index = 0
        exp_rect = pygame.Rect((self.body[0].x * CELL_SIZE) , (self.body[0].y * CELL_SIZE) , CELL_SIZE, CELL_SIZE)
        
        for i in self.explosion:
            image = self.explosion[index]
            self.screen.blit(image, exp_rect)
            index += 1

    def enemy_collision(self):
        if self.alive == True:
            if self.body[0] in self.body[1:]:
                self.kill_enemy()
            if self.body[0].x < 2 or self.body[0].x > CELL_NUMBER - 4:
                self.kill_enemy()
            if self.body[0].y < 3 or self.body[0].y > CELL_NUMBER - 2:
                self.kill_enemy()