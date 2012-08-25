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
		self.mpos = Vector2d(-1, -1)

	def consume(self, event):
		if event.type == pygame.KEYDOWN:
			self._keys[event.key] = True

		if event.type == pygame.KEYUP:
			self._keys[event.key] = False

		if event.type == pygame.MOUSEMOTION:
			self.mpos.setc(event.pos[0], event.pos[1])
			# print self.mpos

		return True

	def key_down(self, key):
		if key in self._keys.keys():
			if self._keys[key] == True:
				return True
		return False

	def mouse_pos():
		return self.mpos

# ##########################################################
# Game class 
# This object will take care of maintaining the game state
# ##########################################################
class Game():
	def __init__(self, res_x = 800, res_y = 600, fullscreen = False):
		self.res = self.res_x, self.res_y = res_x, res_y
		self.running = True
		self.input = GameInput()
		self.map = Map(40, 30, self.res_x, self.res_y)

	def game_init(self):
		pygame.init()
		pygame.display.set_caption('LudumDare 24 :: Evolution')
		self.canvas = pygame.display.set_mode(self.res, pygame.HWSURFACE | pygame.DOUBLEBUF)

	def draw(self):
		self.map.draw(self.canvas)


	def update(self):
		if self.input.key_down(K_ESCAPE):
			self.running = False
			return False

		self.map.update(self.input)

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