import pygame, os, sys
from pygame.locals import *
from game_objects import *
from game_controller import *


# ##########################################################
# GameInput class
# This object will take care of handling keyboard events.
# TODO: make this a singleton as I dont want more than one instance... or does it really matter?
# ##########################################################
class GameInput():
	def __init__(self):
		self._keys = {}
		self.mpos = Vector2d(-1, -1)
		self.mdown = False

	def consume(self, event):
		if event.type == pygame.KEYDOWN:
			self._keys[event.key] = True

		if event.type == pygame.KEYUP:
			self._keys[event.key] = False

		if event.type == pygame.MOUSEMOTION:
			self.mpos.setc(event.pos[0], event.pos[1])

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.mouse.set_visible(False)
			self.mdown = True

		if event.type == pygame.MOUSEBUTTONUP:
			pygame.mouse.set_visible(True)
			self.mdown = False

		return True

	def key_down(self, key):
		if key in self._keys.keys():
			if self._keys[key] == True:
				return True
		return False

	def mouse_pos(self):
		return self.mpos

	def mouse_down(self):
		return self.mdown

# ##########################################################
# Menu class 
# Menu object will hold the number monsters left and the 
# ##########################################################

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
		
	def init_towers(self):
		#We can do this however, just return a list of TowerData objects
		re_comment = re.compile('^(\s)*?#.*$')
		re_nothing = re.compile('^\s*$')
		towers = []

		f = open("./level_map/towers")
		lines = f.readlines()

		for line in lines:
			if re_comment.match(line):
				continue
			if re_nothing.match(line):
				continue

			tower = line.strip().split(" ")
			td = TowerData()
			td.set_props(tower[0], tower[1], tower[2], tower[3], tower[4], tower[5])
			towers.append(td)

		f.closed

		return towers

	def game_init(self):
		pygame.init()
		pygame.display.set_icon(pygame.image.load("./images/icon.png"))
		pygame.display.set_caption('LudumDare 24 :: Evolution')
		self.canvas = pygame.display.set_mode(self.res, pygame.HWSURFACE | pygame.DOUBLEBUF)
		tData = self.init_towers()
		self.controller = Controller(tData)
		self.ui = UInterface()
		self.ui.get_towers(tData)

	def draw(self):
		self.ui.draw(self.canvas)
		self.map.draw(self.canvas)

	def update(self):
		if self.input.key_down(K_ESCAPE):
			self.running = False
			return False

		self.map.update(self.input)
		self.controller.update(self.map, self.input)

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