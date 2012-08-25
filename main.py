import pygame, os, sys
from pygame.locals import *
from game_objects import *

# ##########################################################
# GameInput class
# This object will take care of handling keyboard events.
# TODO: make this a singleton as I dont want more than one instance... or does it really matter?
# ##########################################################
class GameInput():
	def __init__(self):
		self._keys = {}

	def consume(self, event):
		if event.type == pygame.KEYDOWN:
			self._keys[event.key] = True
		if event.type == pygame.KEYUP:
			self._keys[event.key] = False

	def key_down(self, key):
		if key in self._keys.keys():
			if self._keys[key] == True:
				return True
		return False

# ##########################################################
# Game class 
# This object will take care of maintaining the game state
# ##########################################################
class Game():
	def __init__(self, res_x = 800, res_y = 600, fullscreen = False):
		self._res = self._res_x, self._res_y = res_x, res_y
		self.running = True
		self.input = GameInput()

	def game_init(self):
		pygame.init()
		pygame.display.set_caption('LudumDare 24 :: Evolution')
		self.canvas = pygame.display.set_mode(self._res, pygame.HWSURFACE | pygame.DOUBLEBUF)

	def draw(self):
		pass


	def update(self):
		if self.input.key_down(K_ESCAPE):
			self.running = False
			return

	def cleanup(self):
		pygame.quit()

	def gather_events(self, event):
		if event.type == pygame.QUIT:
			self.running = False
		
		self.input.consume(event)

	def play(self):
		if self.game_init() == False:
			self.running = False

		while self.running:
			for event in pygame.event.get():
				self.gather_events(event)

			self.update()
			self.canvas.fill(pygame.Color("Black"))
			self.draw()
			pygame.display.flip()

		self.cleanup()

if __name__ == "__main__":
	game = Game()
	game.play()