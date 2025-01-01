import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
from hand_detection import hand_status # Ensures hand detetion runs in the background


class Game:
    def __init__(self):
        #player setup
        player_sprite = Player((screen_width/2,screen_height-20), screen_width, screen_height)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.menu = True
        # health and score setup   
        self.lives = 3
        self.live_surf = pygame.image.load('resources/player_sprite.png').convert_alpha()
        self.live_surf = pygame.transform.scale(self.live_surf,(75, 75))
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('resources/Koulen-Regular.ttf', 40)


        #obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 5
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(40,600,*self.obstacle_x_positions)

        #alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 0.8
        self.paused = False
        self.pause_time = 1000

        #extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40,80) 


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
    
    def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 150):  #Alien positions (offset so that it away from the top and side of the)
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0: alien_sprite = Alien('red',x,y)          #Alien colors
                elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y) #Alien colors
                else: alien_sprite = Alien('yellow',x,y)                    #Alien colors
                self.aliens.add(alien_sprite)


    def alien_position_checker(self):       #Alien positions
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -0.8
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 0.8
                self.alien_move_down(2)


    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height,"red")
            self.alien_lasers.add(laser_sprite)


    def extra_alien_timmer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),screen_width))
            self.extra_spawn_time = randint(400,800)

    def collision_check(self):
        #player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #obsticle collision
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                #alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    for alien in aliens_hit:    
                        self.score += alien.value
                    laser.kill()
                        

                #extra alien collision
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score += 500
                    laser.kill()
                    

        #alien laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        hit_msg = self.font.render(f'Game Over! Final Score: {self.score}',False,'red') #Game over msgs
                        hit_rect = hit_msg.get_rect(center = (screen_width/2,screen_height/2))
                        screen.blit(hit_msg,hit_rect)
                        pygame.display.flip()
                        pygame.time.delay(1000)
                        pygame.time.set_timer(ALIENLASER, 0)
                        self.menu = True
                    else:
                        hit_msg = self.font.render(f'Damage! {self.lives} lives remaining',False,'red')
                        hit_rect = hit_msg.get_rect(center = (screen_width/2,60))
                        screen.blit(hit_msg,hit_rect)
                        self.paused = True
                        self.pause_time = pygame.time.get_ticks()

        #aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                    
                if pygame.sprite.spritecollide(alien,self.player,False):
                    hit_msg = self.font.render(f'Game Over! Final Score: {self.score}',False,'red') #Game over msgs
                    hit_rect = hit_msg.get_rect(center = (screen_width/2,screen_height/2))
                    screen.blit(hit_msg,hit_rect)
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    pygame.time.set_timer(ALIENLASER, 0)
                    self.menu = True

    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)
    def alienclear(self):
        if not self.aliens.sprites():
            self.alien_setup(rows = 6, cols = 8)

    def run(self):  #Game loop
        if self.paused:
            if pygame.time.get_ticks() - self.pause_time > 500:
                self.paused = False
            return
        self.player.update()    #Player movement #Where the CV will take over instead of listening to keybinds it listens to the cv output
        self.alien_lasers.update()  #Updates the alien lasers
        self.extra.update()
        self.aliens.update(self.alien_direction)    #Alien movement
        self.alien_position_checker()   #Alien positions
        self.extra_alien_timmer()   #Extra alien timer
        self.collision_check()      #Collision check
        

        self.player.sprite.lasers.draw(screen)      #Draws the player lasers
        self.player.draw(screen)    #Draws the player
        self.blocks.draw(screen)     #Draws the obstacles
        self.aliens.draw(screen)      #Draws the aliens
        self.alien_lasers.draw(screen)  #Draws the alien lasers
        self.extra.draw(screen)
        self.display_lives()        #Displays the lives
        self.display_score()        #Displays the score
        self.alienclear()


class CRT:  #CRT class
    def __init__(self): #Loads the tv image
        self.tv = pygame.image.load('resources/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))

    def create_crt_lines(self): #Creates the crt lines
        line_height = 3
        line_amount = int((screen_height / line_height))
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)

    def draw(self):    #Draws the tv
        self.tv.set_alpha(randint(75,90))   #Sets the alpha of the tv
        self.create_crt_lines()    #Creates the crt lines
        screen.blit(self.tv,(0,0))  #Draws the tv

    
pygame.init()
screen_width = 800  
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
crt = CRT()

ALIENLASER = pygame.USEREVENT + 1 #Sets the timer for the alien laser

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == ALIENLASER:
            game.alien_shoot()
    if game.menu:
        bg = pygame.image.load('./resources/background.png')
        bg = bg.convert_alpha()
        bg = pygame.transform.scale(bg, (screen_width, screen_height))
        logo = pygame.image.load('./resources/logo.png')
        logo = logo.convert_alpha()
        logo_rect = logo.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        bg_rect = bg.get_rect()
        screen.fill((60, 25, 60))  # Clear screen only when running
        screen.blit(bg, bg_rect)
        screen.blit(logo, logo_rect)
        text = game.font.render('Start' , True , 'black')
        highscore = game.font.render(f"High Score: {game.score}", True, 'black')
        btn = pygame.draw.rect(screen, (171, 54, 214),[ (screen_width - 260) // 2, (screen_height - 50) // 2,260,50],border_radius=14)
        highscorebg = pygame.draw.rect(screen, (171, 54, 214),[ (screen_width - 300) // 2, (screen_height - 50) // 2 + 100,300,50],border_radius=14)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        highscore_rect = highscore.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(highscore, highscore_rect)
        screen.blit(text , text_rect)
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(mouse_pos):
            pygame.time.set_timer(ALIENLASER,500)
            game = Game()
            game.run()
            game.menu = False
    else:
        if not game.paused:
            screen.fill((10, 10, 10))  # Clear screen only when running
            screen.blit(bg, bg_rect)
            crt.draw()
        game.player.sprite.update()
        game.run()
    pygame.display.flip()
    clock.tick(60) #Sets the fps to be 60



