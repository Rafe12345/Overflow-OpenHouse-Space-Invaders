import pygame, sys
from player import Player
class Game:
    def __init__(self):
        player_sprite = Player((screen_width/2,screen_height-20))
        self.player = pygame.sprite.GroupSingle(player_sprite)
    def run(self):
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

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
    clock.tick(60)