import pygame
from hand_detection import hand_status
from laser import Laser
class Player(pygame.sprite.Sprite):
    def __init__(self,pos, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load('./resources/player_sprite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(75, 75)) #Sets the size of the player to be 75 by 75
        self.rect = self.image.get_rect(midbottom = pos) #initial position of the player
        self.speed = 2
        self.laserCoolDown = 500
        self.lastshottime = 0 
        self.lasers = pygame.sprite.Group()
        self.screen_width = screen_width # Store screen dimensions
        self.screen_height = screen_height 
        self.triple = False
        self.tripletime = 0
        self.laser_sound = pygame.mixer.Sound('audio/audio_laser.wav')
        self.laser_sound.set_volume(0.5)
        self.count = 0
    def getinput(self): #Where the CV will take over instead of listening to keybinds it listens to the cv output
        # Move left if left hand is raised
        if hand_status["left"]:
            self.rect.x -= self.speed
        # Move right if right hand is raised
        if hand_status["right"]:
            self.rect.x += self.speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]: #Movement for the player sprite (RIGHT)
            if self.rect.x < 720:
                self.rect.x += self.speed
        elif keys[pygame.K_a]:  #Movement for the player sprite (LEFT)
            if self.rect.x > 5:
                self.rect.x -= self.speed
        # Keep the player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def shootlaser(self):
        self.lasers.add(Laser(self.rect.center,-6,self.rect.bottom,"green")) #Creates laser objects and adding it into the sprite group
        
    def automatic_shoot(self):  # Automatically shoot laser every 2 seconds
        if self.current_time - self.lastshottime >= self.laserCoolDown:
            self.shootlaser()
            self.laser_sound.play()
            self.lastshottime = self.current_time
    def triple_shootlaser(self):
        offsets = [-15, 0, 15]
        if self.count < 5:
            if self.current_time - self.tripletime >= 500:
                for offset in offsets:
                    laser_position = (self.rect.centerx + offset, self.rect.top)
                    self.lasers.add(Laser(laser_position, -6, self.rect.bottom, "green"))
                self.tripletime = self.current_time
                self.count += 1
        else:
            self.count = 0
            self.triple = False

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.lasers.update()
        self.getinput() # Handle Movement
        self.automatic_shoot() # Calling automatic shooting function
        if self.triple:
            self.triple_shootlaser()