import pygame, sys
from settings import *
from level import Level
from player import Player
from enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TRON: light cycle v 0.02")
        
        self.screen = pygame.display.set_mode(DISPLAY)
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.player = Player()
        self.enemy = Enemy()

        self.score = [0,0]
        self.font = pygame.font.Font('../graphics/tron-arcade.ttf', 16)
        
    def run(self):
        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE , 80)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # player/enemies update
                if event.type == SCREEN_UPDATE:
                    self.player.move_player()
                    self.player.player_collision()

                    self.enemy.move_enemy()
                    self.enemy.enemy_collision()
                    self.enemy.enemy_direction()

                # player keys
                if event.type == pygame.KEYDOWN:
                    self.player.player_keys(event)
                    
                # enemy avoid player
                if (self.enemy.body[0] + self.enemy.direction) in self.player.body:
                    try_1 = self.enemy.avoid_beam()
                    if ((self.enemy.body[0] + try_1) in self.enemy.body) or ((self.enemy.body[0] + try_1) in self.player.body):
                        self.enemy.direction = - try_1
                    else:
                        self.enemy.direction = try_1

                # player/enemy interact
                if self.enemy.body[0] in self.player.body:
                    self.enemy.kill_enemy()
                    self.player.speed = 0
                if self.player.body[0] in self.enemy.body:
                    self.player.kill_player()
                    self.enemy.speed = 0
            
                if self.player.alive == False and self.player.lives > 0:
                    # self.enemy.speed = 0
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.score[1] += 1
                            self.player = Player()
                            self.player.lives -= self.score[1]
                            self.enemy = Enemy()
                if self.enemy.alive == False and self.player.lives > 0:
                    # self.player.speed = 0
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.score[0] += 100
                            self.player = Player()
                            self.player.lives -= self.score[1]
                            self.enemy = Enemy()

                            
                        if self.score[0] > self.level.highscore:
                            self.level.highscore = self.score[0]
                            self.level.hs_update(self.score[0])
                
            self.screen.fill((BACK_COLOR))
            self.level.run()
            self.player.draw_player()
            self.enemy.draw_enemy()

            score2 = self.font.render(f'    {self.player.lives}     HIGHSCORE', True, (25,25,175))
            score1 = self.font.render('{:05d}         {}'.format(self.score[0], self.level.highscore), True, (25,25,175))
            self.screen.blit(score2, (7 * CELL_SIZE , 3))
            self.screen.blit(score1, (7 * CELL_SIZE , 22))
            if (self.enemy.alive == False or self.player.alive == False) and self.player.lives > 0:
                restart = self.font.render(' Press space to continue', True, (255,255,255))
                self.screen.blit(restart, (6 * CELL_SIZE , 13 * CELL_SIZE))
            if (self.enemy.alive == False or self.player.alive == False) and self.player.lives <= 0:
                game_over = self.font.render('GAME OVER', True, (175,25,25))
                self.screen.blit(game_over, (12 * CELL_SIZE , 13 * CELL_SIZE))
                
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()