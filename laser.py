import pygame 

class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,speed,screen_height):
		super().__init__()
		self.image = pygame.Surface((5,20)) #Sets the size of the laser beam
		self.image.fill('red') #Colour of laser beam
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_constraint = screen_height

	def destroy(self): #Checks if the laser has reached the top of the screen or reach the bottom of the screen. If so then it will delete itself
		if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.destroy()