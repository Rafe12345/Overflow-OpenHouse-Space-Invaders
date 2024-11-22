import pygame
# 49:22
class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = '../graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = self.image.get_rect(topleft = (x,y))
    

