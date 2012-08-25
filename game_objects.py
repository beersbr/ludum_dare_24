# Filename game_objects.py 

import pygame, os, sys
from pygame.locals import *

# ##########################################################
# Vector2d Class 
# This will be the object that will represent position on the coordinate
# plane
# ##########################################################
class Vector2d():
	def __init__(self, _x, _y):
		self.x, self.y = _x, _y

	def to_ary(self):
		return (self.x, self.y)

	# Keep in mind this will return radians
	def dot_product(self, vec2d):
		return ((self.x * vec2d.x) + (self.y * vec2d.y))

# ##########################################################
# Entity class 
# this is the class that will be the base class for all the drawable/movable objects on the screen
# ##########################################################
class Entity():
	def __init__(self, pos_x, pos_y):
		self.pos = Vector2d(pos_x, pos_y)

	def x(self):
		return self.pos.x

	def y(self):
		return self.pos.y

	def draw(self, canvas):
		pass

	def update(self, args):
		pass

# ##########################################################
# Map class
# this will be the object that keeps track of what the map will look like and the items
# in the game
# ##########################################################
class Map(Entity):
	def __init__(self):
		pass

	def draw(self, canvas):
		

	def update(self, args):
		pass

# End of File game_objects.py