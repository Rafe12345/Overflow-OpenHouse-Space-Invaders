import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((5,20)) #Sets the size of the laser beam
        self.image.fill('red') #Colour of laser beam
        self.rect = self.image.get_rect(center = pos)
        self.speed_of_laser = 5
    def update(self):
        if self.rect.y > 50: #movement for the laser beam (UP)
            self.rect.y -= self.speed_of_laser
        if self.rect.y < 50: #Once it reaches the top it deletes to reduce objects drawn
            self.kill() 