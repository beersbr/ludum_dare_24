# Filename: g_input_handler.py

import pygame, os, sys
from pygame.locals import *
from g_vector import *

class InputHandler():
	def __init__(self):
		self._keys = {}
		self.mouse_pos = Vector2d()
		self.mouse_down = False

	def consume(self, event):
		if event.type == pygame.KEYDOWN:
			self._keys[event.key] = True

		if event.type == pygame.KEYUP:
			self._keys[event.key] = False

		if event.type == pygame.MOUSEMOTION:
			self.mouse_pos.set_array(event.pos)

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.mouse_down = True

		if event.type == pygame.MOUSEBUTTONUP:
			pygame.mouse_down = False

	def key_down(self, key):
		if key in self._keys.keys():
			if self._keys[key] == True:
				return True
		return False

	def mouse_pos(self):
		return self.mouse_pos

	def mouse_down(self):
		return self.mouse_down


# End of g_input_handler.py