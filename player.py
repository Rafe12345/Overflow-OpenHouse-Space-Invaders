import pygame
from laser import Laser
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('./resources/player_sprite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(75, 75)) #Sets the size of the player to be 75 by 75
        self.rect = self.image.get_rect(midbottom = pos) #initial position of the player
        self.speed = 10
        self.laserCoolDown = 300
        self.lastshottime = 0 
        self.lasers = pygame.sprite.Group()
    def getinput(self): #Where the CV will take over instead of listening to keybinds it listens to the cv output
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]: #Movement for the player sprite (RIGHT)
            if self.rect.x < 720:
                self.rect.x += self.speed
        elif keys[pygame.K_a]:  #Movement for the player sprite (LEFT)
            if self.rect.x > 5:
                self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:  #Movement for the player sprite (SHOOT)
            if self.current_time - self.lastshottime >= self.laserCoolDown: #Cool down timer for laser
                self.shootlaser()
                self.lastshottime = self.current_time
    def shootlaser(self):
        self.lasers.add(Laser(self.rect.center,-6,self.rect.bottom)) #Creates laser objects and adding it into the sprite group
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.lasers.update()
        self.getinput()