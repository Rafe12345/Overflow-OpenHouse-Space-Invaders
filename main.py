import pygame, sys
from player import Player
import obstacle


from alien import Alien
from random import choice

class Game:
    def __init__(self):
        #player setup
        player_sprite = Player((screen_width/2,screen_height-20))
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 5
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(40,600,*self.obstacle_x_positions)

        #alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1




    def create_obstacle(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for column_index, column in enumerate(row):
                if column == 'x':
                    x = x_start + column_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(220,20,60),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,x_start,y_start,*offset):
        for x in offset:
            self.create_obstacle(x_start,y_start,x)
    
    def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):  #Alien positions
        for row_index, rows in enumerate(range(rows)):
            for col_index, cols in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset


                if row_index == 0: alien_sprite = Alien('red',x,y)          #Alien colors
                elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y) #Alien colors
                else: alien_sprite = Alien('yellow',x,y)                    #Alien colors
                self.aliens.add(alien_sprite)


    def alien_position_checker(self):       #Alien positions#alien positions
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)


    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            



    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        self.aliens.draw(screen)

pygame.init()
screen_width = 800  
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((10,10,10)) 
    game.run()
    pygame.display.flip()
    clock.tick(60) #Sets the fps to be 60











