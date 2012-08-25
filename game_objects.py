# Filename game_objects.py 

import pygame, os, sys, re
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

# ##########################################################
# Monster Class 
# this is the class that will take care of all my monsters. I'm thinking just one monster class and
# give the monster an id which will determin style and behavior
# ##########################################################
class Monster():
	NONE = 0
	NORMAL = 1
	FAST = 2
	HEAVY = 4

	def __init__(self, pos_x, pos_y):
		self.pos = Vector2d(pos_x, pos_y)
		self.id = 0

	def draw(self, canvas):
		pass

	def update(self, args):
		pass



# ##########################################################
# Tile class 
# This is the object that will hold tiles and the status of a tile. This is just a holder and nothing else.
# The plan is to have the tiles take on a style... we'll see if that remains the case as the night goes on.
# ##########################################################
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
		elif self.status == Tile.STATUS_CLICK:
			pygame.draw.rect(canvas, (100, 100, 100), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))

		if self.type == Tile.TYPE_SOLID:
			pygame.draw.rect(canvas, (100, 40, 40), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))

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
			self.tiles.append([])
			for y in range(self.rows):
				self.tiles[x].append(Tile(x*self.tile_width, y*self.tile_height, x, y))


		self.load_map("level_map/level0.map")

	def draw(self, canvas):
		for x in range(self.cols):
			for y in range(self.rows):
				self.tiles[x][y].draw(canvas)

		return True

	def update_tile(self, x, y):
		pass

	def status_tile(self, x, y):
		pass

	def update(self, args):
		tile_x = (args.mpos.x / Tile.TILE_WIDTH)
		tile_y = (args.mpos.y / Tile.TILE_HEIGHT)

		# tile_index = (tile_y) * self.cols + (tile_x)

		if self.hover_tile != None:
			self.hover_tile.status = Tile.NONE

		self.hover_tile = self.tiles[tile_x][tile_y]
		self.hover_tile.status = Tile.STATUS_HOVER if args.mouse_down() == False else Tile.STATUS_CLICK

	def load_map(self, filename):
		re_comment = re.compile('^(\s)*?#.*$')
		re_nothing = re.compile('^\s*$')

		f = open('./level_map/level0.map')
		trows = f.readlines()

		current_row = 0
		current_col = 0

		for row in trows:
			if re_comment.match(row):
				continue
			if re_nothing.match(row):
				continue

			arow = row.split(" ")

			for tile in arow:
				tile_type = int(tile[0])
				tile_style = int(tile[1:3])

				self.tiles[current_col][current_row].type = tile_type
				self.tiles[current_col][current_row].style = tile_style

				current_col += 1

			current_row += 1
			current_col = 0

# End of File game_objects.py