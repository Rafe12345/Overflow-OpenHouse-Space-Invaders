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
        self.live_surf = pygame.transform.scale(self.live_surf,(50, 50))
        self.live_x_start_pos = screen_width - 10
        self.live_surf_rect = self.live_surf.get_rect(topright = (self.live_x_start_pos,8))
        self.score = 0
        self.font = pygame.font.Font('resources/Koulen-Regular.ttf', 40)
        self.explosion_group = pygame.sprite.Group()

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
        self.powerupsgroup = pygame.sprite.Group()
        self.tripleshoot = pygame.sprite.Group()
	# Audio
        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(0.2)
        music.play(loops = -1)
        self.laser_sound = pygame.mixer.Sound('audio/audio_laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('audio/audio_explosion.wav')
        self.explosion_sound.set_volume(0.5)
	


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
            # self.laser_sound.play()


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
                        pos = alien.rect.center
                        num = randint(1,10)
                        if num == 1:
                            self.powerupsgroup.add(Powerups(pos))
                        elif num == 2:
                            self.tripleshoot.add(tripleshoot(pos))
                        explosion = Explosion(pos[0],pos[1])
                        self.explosion_group.add(explosion)      
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()
                        

                #extra alien collision
                if pygame.sprite.spritecollide(laser,self.extra,False):
                    pos = self.extra.sprite.rect.center
                    explosion = Explosion(pos[0],pos[1])
                    self.explosion_group.add(explosion) 
                    self.score += 500
                    self.extra.sprite.kill()
                    laser.kill()
                    

        #alien laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    pos = self.player.sprite.rect.top
                    explosion = Explosion(self.player.sprite.rect.center[0],pos)
                    self.explosion_group.add(explosion) 
                    self.lives -= 1
                    if self.lives <= 0:
                        hit_msg = self.font.render(f'Game Over! Final Score: {self.score}',False,'red') #Game over msgs
                        hit_rect = hit_msg.get_rect(center = (screen_width//2,screen_height//2))
                        screen.blit(hit_msg,hit_rect)
                        pygame.display.flip()
                        pygame.time.delay(1100)
                        pygame.time.set_timer(ALIENLASER, 0)
                        self.menu = True
                    else:
                        hit_msg = self.font.render(f'Damage! {self.lives} lives remaining',False,'red')
                        hit_rect = hit_msg.get_rect(center = (screen_width//2,60))
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
        #powerups
        if self.powerupsgroup:
            for powerup in self.powerupsgroup:
                if pygame.sprite.spritecollide(powerup,self.player,False):
                    powerup.kill()
                    self.lives += 1
        if self.tripleshoot:
            for triple in self.tripleshoot:
                if pygame.sprite.spritecollide(triple,self.player,False):
                    triple.kill()
                    self.player.sprite.triple = True

    def display_lives(self):
        lives = self.font.render(f'{self.lives}',False,'white')
        lives_rect = lives.get_rect(topright=(self.live_x_start_pos-60, 5))
        screen.blit(self.live_surf,self.live_surf_rect)
        screen.blit(lives,lives_rect)

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)

    def alienclear(self):
        if not self.aliens.sprites():
            self.alien_setup(rows = 6, cols = 8)
    def inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            pygame.time.set_timer(ALIENLASER, 0)
            self.menu = True
    def run(self):  #Game loop
        self.explosion_group.draw(screen)
        self.explosion_group.update()
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
        self.powerupsgroup.update()
        self.tripleshoot.update()
        self.player.sprite.lasers.draw(screen)      #Draws the player lasers
        self.player.draw(screen)    #Draws the player
        self.blocks.draw(screen)     #Draws the obstacles
        self.aliens.draw(screen)      #Draws the aliens
        self.alien_lasers.draw(screen)  #Draws the alien lasers
        self.powerupsgroup.draw(screen)
        self.tripleshoot.draw(screen)
        self.extra.draw(screen)
        self.display_lives()        #Displays the lives
        self.display_score()        #Displays the score
        self.alienclear()
        self.inputs()

class Powerups(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('./resources/powerups/health.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(75, 75)) 
        self.rect = self.image.get_rect(center = pos) 
    def update(self):
        if self.rect.y < screen_height:
            self.rect.y += 1.2
        else:
            self.kill()
class tripleshoot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('./resources/powerups/triple.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(75, 75)) 
        self.rect = self.image.get_rect(center = pos) 
    def update(self):
        if self.rect.y < screen_height:
            self.rect.y += 1.2
        else:
            self.kill()

class CRT:  #CRT class
    def __init__(self): #Loads the tv image
        self.tv = pygame.image.load('resources/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))

    def create_crt_lines(self): #Creates the crt lines
        line_height = 6
        line_amount = int((screen_height / line_height))
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)

    def draw(self):    #Draws the tv
        self.tv.set_alpha(randint(75,90))   #Sets the alpha of the tv
        self.create_crt_lines()    #Creates the crt lines
        screen.blit(self.tv,(0,0))  #Draws the tv

class Explosion(pygame.sprite.Sprite): #Explosion code from Russcode
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"./resources/explosion/exp{num}.png")
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

class menu: #Aliens for the game menu not for the game itself
    def __init__(self):
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 0.9
        self.alien_lasers = pygame.sprite.Group()
        self.lastshottime = 0 
    def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 220):  #Alien positions (offset so that it away from the top and side of the)
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
                self.alien_direction = -0.9
            elif alien.rect.left <= 0:
                self.alien_direction = 0.9
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height,"red")
            self.alien_lasers.add(laser_sprite)
            self.lastshottime = pygame.time.get_ticks()
    def run(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.lastshottime >= 300:
            self.alien_shoot()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
pygame.init()
screen_width = 800  
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
crt = CRT()
menualien = menu()
ALIENLASER = pygame.USEREVENT + 1 #Sets the timer for the alien laser
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == ALIENLASER:
            game.alien_shoot()
    if game.menu: #Game Menu
        bg = pygame.image.load('./resources/background.png')
        bg = bg.convert_alpha()
        bg = pygame.transform.scale(bg, (screen_width, screen_height))
        logo = pygame.image.load('./resources/logo.png')
        logo = logo.convert_alpha()
        logo_rect = logo.get_rect(center=(screen_width // 2, 150))
        bg_rect = bg.get_rect()
        screen.blit(bg, bg_rect)
        screen.blit(logo, logo_rect)
        text = game.font.render('Start' , True , 'black')
        highscore = game.font.render(f"High Score: {game.score}", True, 'black')
        btn = pygame.draw.rect(screen, (171, 54, 214),[ (screen_width - 260) // 2, 550,260,50],border_radius=14)
        highscorebg = pygame.draw.rect(screen, (171, 54, 214),[ (screen_width - 300) // 2, 650,300,50],border_radius=14)
        text_rect = text.get_rect(center=(screen_width // 2, 575))
        highscore_rect = highscore.get_rect(center=(screen_width // 2, 675))
        screen.blit(highscore, highscore_rect)
        screen.blit(text , text_rect)
        menualien.run()
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(mouse_pos):
            pygame.time.set_timer(ALIENLASER,500)
            game = Game()
            game.run()
            game.menu = False
    else:
        if not game.paused:
            screen.blit(bg, bg_rect)
            crt.draw()
        game.player.sprite.update()
        game.run()
    pygame.display.flip()
    clock.tick(60) #Sets the fps to be 60



