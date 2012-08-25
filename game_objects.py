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

	def __str__(self):
		return ("<x: " + str(self.x) + " y: " + str(self.y) + ">")

	def to_ary(self):
		return (self.x, self.y)

	# Keep in mind this will return radians
	def dot_product(self, vec2d):
		return ((self.x * vec2d.x) + (self.y * vec2d.y))

	def setv(self, vec2d):
		self.x, self.y = vec2d.x, vec2d.y

	def setc(self, x, y):
		self.x, self.y = x, y

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

class Tile(Entity):
	NONE 		= 0
	STATUS_HOVER  = 1
	STATUS_CLICK  = 2
	TYPE_SOLID 	= 3
	TYPE_WALKABLE = 4
	TYPE_PLOT 	= 5
	STYLE_GRASS = 6
	STYLE_STONE = 7
	STYLE_PATH 	= 8

	TILE_WIDTH = -1
	TILE_HEIGHT = -1

	def __init__(self, rx, ry, fx, fy):
		self.x, self.y = rx, ry
		self.fx, self.fy = fx, fy
		self.status = Tile.NONE
		self.style = Tile.NONE
		self.type = Tile.NONE

	def draw(self, canvas):
		if self.status == Tile.STATUS_HOVER:
			pygame.draw.rect(canvas, (180, 180, 180), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))
		return True

# ##########################################################
# Map class
# this will be the object that keeps track of what the map will look like and the items
# in the game
# ##########################################################
class Map(Entity):
	def __init__(self, _rows, _cols, _width, _height):
		self.cols, self.rows = _rows, _cols
		self.width, self.height = _width, _height
		self.tile_width = self.width / self.cols
		self.tile_height = self.height / self.rows
		self.tiles = []

		Tile.TILE_WIDTH = self.tile_width
		Tile.TILE_HEIGHT = self.tile_height

		self.hover_tile = None

		for x in range(self.cols):
			for y in range(self.rows):
				self.tiles.append(Tile(x*self.tile_width, y*self.tile_height, x, y))

	def draw(self, canvas):
		# for x in range(0, self.cols):
		# 	for y in range(0, self.rows):
		# 		pygame.draw.rect(canvas, (255, 255, 255), (x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height), 1)

		for t in self.tiles:
			t.draw(canvas)

		return True

	def update_tile(self, x, y):
		pass

	def status_tile(self, x, y):
		pass

	def update(self, args):
		tile_x = 0 if args.mpos.x == 0 else (args.mpos.x / Tile.TILE_WIDTH)
		tile_y = 0 if args.mpos.y == 0 else (args.mpos.y / Tile.TILE_HEIGHT)

		tile_index = (tile_y) * self.cols + (tile_x)

		if self.hover_tile != None:
			self.hover_tile.status = Tile.NONE

		self.hover_tile = self.tiles[tile_index]
		self.hover_tile.status = Tile.STATUS_HOVER


# End of File game_objects.py