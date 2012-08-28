# Filename: g_main.py

import sys, os, pygame
from pygame.locals import *
from g_vector import *
from g_input_handler import *

class Game():
	def __init__(self, res_x = 800, res_y = 600, fullscreen = False):
		self.resolution = Vector2d(res_x, res_y)
		self.running = True
		self.input = InputHandler()
		self.clock = pygame.time.Clock()
		self.buffer = None

	def init(self):
		pygame.init()
		pygame.display.set_icon(pygame.image.load("./images/icon.png"))
		pygame.display.set_caption("LudumDare 24 :: Evolution Code Revamp")
		self.buffer = pygame.display.set_mode(self.resolution.to_array(), pygame.HWSURFACE | pygame.DOUBLEBUF)
		return True

	def draw(self):
		pass

	def update(self):
		if self.input.key_down(K_ESCAPE):
			self.running = False

	def cleanup(self):
		pygame.quit()

	def consume_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
			return False

		self.input.consume(event)
		return True

	def play(self):
		if self.init() == False:
			self.running = False

		while self.running:
			self.clock.tick(60)
			for event in pygame.event.get():
				self.consume_event(event)

			self.update()
			self.buffer.fill(pygame.Color("Black"))
			self.draw()
			pygame.display.flip()

		self.cleanup()

if __name__ == "__main__":
	print "Starting the game..."
	game = Game()
	game.play()
	print "Done."

# End of g_main.py