import pygame
from hand_detection import hand_status
from laser import Laser
class Player(pygame.sprite.Sprite):
    def __init__(self,pos, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load('./resources/player_sprite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(75, 75)) #Sets the size of the player to be 75 by 75
        self.rect = self.image.get_rect(midbottom = pos) #initial position of the player
        self.speed = 10
        self.laserCoolDown = 300
        self.lastshottime = 0 
        self.lasers = pygame.sprite.Group()
        self.screen_width = screen_width # Store screen dimensions
        self.screen_height = screen_height 

    def getinput(self): #Where the CV will take over instead of listening to keybinds it listens to the cv output
        # Move left if left hand is raised
        if hand_status["left"]:
            self.rect.x -= self.speed
        # Move right if right hand is raised
        if hand_status["right"]:
            self.rect.x += self.speed

        # Keep the player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: # Movement for the player sprite (SHOOT)
            if self.current_time - self.lastshottime >= self.laserCoolDown: # Cool down timer for laser
                self.shootlaser()
                self.lastshottime = self.current_time

    def shootlaser(self):
        self.lasers.add(Laser(self.rect.center,-6,self.rect.bottom)) #Creates laser objects and adding it into the sprite group
        
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.lasers.update()
        self.getinput()