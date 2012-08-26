# Filename game_objects.py 

import pygame, os, sys, re, math
from pygame.locals import *
import random

# ##########################################################
# UI object
# This will render the ui in the appropriate spot
# ##########################################################
class UInterface():
	def __init__(self):
		self.game_name = "Something"
		self.surface = pygame.image.load("./images/ui_background.png")
		self.towers_info = []

	def get_towers(self, towers):

		tfont = pygame.font.SysFont('monoco', 16)

		current_y = 30
		cur_tower = 1
		for tower in towers:

			key_num = str(cur_tower)

			self.surface.blit(tfont.render(key_num, True, (80, 80, 80), (255, 255, 255)), (25, current_y+7))

			filename = "./images/"+tower.name+".png"

			if os.path.isfile(filename):
				image = pygame.image.load(filename)
				self.surface.blit(image, (40, current_y))

			tower_name = tower.name.replace("_", " ")
			self.surface.blit(tfont.render(tower_name, True, (80, 80, 80), (255,255,255)), (70, current_y+5))

			current_y += 30
			cur_tower += 1


	def draw(self, canvas):
		canvas.blit(self.surface, (600, 0))

	def update(self, args):
		pass

# ##########################################################
# TowerData Class 
# structure encapsulating tower data. Need to initialize a structure of these and give it to the controller
# ##########################################################
class TowerData():
	def __init__(self):
		self.name = "<NO NAME>"
		self.cost = 0
		self.damage = 0
		self.range = 0
		self.shoot_frequency = 0
		self.splash_range = 0

	def set_props(self, name, cost, dam, ran, sfreq, splash):
		self.name = name
		self.cost = cost
		self.damage = dam
		self.range = ran
		self.splash_range = splash
		self.shoot_frequency = sfreq
		

# ##########################################################
# Vector2d Class 
# This will be the object that will represent position on the coordinate
# plane
# ##########################################################
class Vector2d():
	def __init__(self, _x = 0, _y = 0):
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
		return self

	def distance(self, vec):
		dx = self.x - vec.x
		dy = self.y - vec.y

		return math.sqrt(dx*dx + dy*dy)

	def subtract(self, vec):
		return Vector2d(self.x - vec.x, self.y - vec.y)

	def normalize(self):
		length = math.sqrt(self.x*self.x + self.y*self.y)
		if length == 0:
			return Vector2d(0, 0)
		return Vector2d((self.x/length), (self.y/length))

	def divide(self, scalar):
		if scalar == 0:
			return self

		return Vector2d(self.x/scalar, self.y/scalar)

	def add(self, vec):
		return Vector2d(self.x + vec.x, self.y + vec.y)

	def multiply(self, scalar):
		return Vector2d(self.x * scalar, self.y * scalar)


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
#
# unline the other object the center of the bullet will be the x and y
# ##########################################################
class Monster(Entity):
	NONE = 0
	NORMAL = 1
	FAST = 2
	HEAVY = 4

	def __init__(self, pos_x, pos_y, target_x, target_y):
		self.pos = Vector2d(pos_x, pos_y)
		self.id = 0
		self.health = 10
		self.target_id = 1
		self.target_pos = Vector2d(target_x, target_y)
		self.speed = 3

		self.color = (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))

	def draw(self, canvas):
		pygame.draw.rect(canvas, self.color, (self.pos.x-5, self.pos.y-5, 10, 10))

	def update(self, args):
		path_list = args[0]
		neighbors = args[1]
		self.find_next_pos(path_list, neighbors)

	# This will be the a* search from node to node so they dont have to search the entire map
	def find_next_pos(self, path, neighbors):
		if pygame.Rect(self.pos.x, self.pos.y, 10, 10).collidepoint(self.target_pos.x, self.target_pos.y):
			if (self.target_id + 1) % len(path) == 0:
				self.target_id = 1
				self.target_pos.setc(path[self.target_id].center_x(), path[self.target_id].center_y())
				self.pos.setc(path[0].center_x(), path[0].center_y())
			else:
				self.target_id = self.target_id + 1
				self.target_pos.setc(path[self.target_id].center_x(), path[self.target_id].center_y())

		diff_y = (self.target_pos.y - self.pos.y)
		diff_x = (self.target_pos.x - self.pos.x)

		# get the angle with respect to the horizontal axis between the two points
		angle = math.atan2(diff_y, diff_x) # * 180 / math.pi # we are using radians

		dx = math.cos(angle)# * self.speed
		dy = math.sin(angle)# * self.speed

		count = 0
		mean = Vector2d()

		for n in neighbors:
			if n == self:
				continue

			distance = self.pos.distance(n.pos)

			if distance < 15 and distance > 0:
				# tv = Vector2d(self.pos.x, self.pos.y)
				mean = mean.add( self.pos.subtract(n.pos).normalize().divide(distance).multiply(2))
				count += 1

		dirv = Vector2d(dx, dy)

		if count > 0:
			newv = mean.divide(count)
			dirv = dirv.add(newv)
			dirv = dirv.divide(2)

		self.pos.x += (dirv.x)
		self.pos.y += (dirv.y)

	def _find_next_pos(self):
		pass

# ##########################################################
# Tower Class 
# This is the object that will produce the bullets that will follow and kills the enemies
# ##########################################################
class Tower(Entity):
	def __init__(self, target_tile, towerData):
		self.pos = Vector2d(target_tile.x, target_tile.y)
		self.id = 0 # Change this
		self.cost = towerData.cost
		self.damage = towerData.damage
		self.range = towerData.range
		self.shoot_frequency = towerData.shoot_frequency
		self.splash = towerData.splash_range
		self.tile = target_tile
		self.name = towerData.name

		filename = "./images/"+self.name+".png"

		if os.path.isfile(filename):
			self.image = self.image = pygame.image.load(filename)
		else:
			self.image = pygame.Surface((20, 20))
			self.color = (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)) #temporary	
			self.image.fill(self.color)

		# print "Tower created at (" + str(self.tile.x) + "," + str(self.tile.y) + ")"

	def draw(self, canvas):
		canvas.blit(self.image, (self.tile.x, self.tile.y))
		# pygame.draw.rect(canvas, self.color, (self.tile.x, self.tile.y, self.tile.TILE_WIDTH, self.tile.TILE_HEIGHT))

	# list of enemies
	def update(self, args):
		pass

# ##########################################################
# Bullet Class
# This is the object produced by the tower and the item responsible for
# hitting the enemies.
# ##########################################################
class Bullet(Entity):
	def __init__(self, pos_x, pos_y):
		self.pos = Vector2d(pos_x, pos_y)
		self.id = 0
		self.damage = 1
		self.speed = 1

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

	TILE_WIDTH = -1
	TILE_HEIGHT = -1

	def __init__(self, rx, ry, fx, fy):
		self.x, self.y = rx, ry
		self.fx, self.fy = fx, fy
		self.status = Tile.NONE
		self.style = Tile.NONE
		self.type = Tile.NONE
		self.path_id = 0
		self.image = None

	def draw(self, canvas):
		if self.type == Tile.TYPE_SOLID:
			pygame.draw.rect(canvas, (100, 40, 40), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))
		elif self.type == Tile.TYPE_PLOT:
			pygame.draw.rect(canvas, (40, 40, 100), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))
		elif self.type == Tile.TYPE_WALKABLE:
			pygame.draw.rect(canvas, (40, 100, 40), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))

		if self.style == Tile.STYLE_GRASS:
			if self.style == Tile.STYLE_GRASS:
				if self.image == None:
					self.image = pygame.image.load("./images/grass.png")
			canvas.blit(self.image, (self.x, self.y))

		if self.path_id > 0:
			pygame.draw.rect(canvas, (40, 150, 150), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))

		if self.status == Tile.STATUS_HOVER:
			pygame.draw.rect(canvas, (180, 180, 180), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))
		elif self.status == Tile.STATUS_CLICK:
			pygame.draw.rect(canvas, (100, 100, 100), (self.x, self.y, Tile.TILE_WIDTH, Tile.TILE_HEIGHT))

		return True

	def update(self, args):
		pass

	def is_path_node(self):
		return (True if Tile.path_node_number else False)

	def center_x(self):
		return (self.x + (Tile.TILE_WIDTH/2))

	def center_y(self):
		return (self.y + (Tile.TILE_HEIGHT/2))

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
		self.path_nodes = []

		self.enemies = []
		self.towers = []

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

		for enemy in self.enemies:
			enemy.draw(canvas)
			
		for tower in self.towers:
			tower.draw(canvas)

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

		for enemy in self.enemies:
			enemy.update((self.path_nodes, self.enemies))

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

			arow = row.strip().split(" ")

			for tile in arow:
				tile_type = int(tile[0])
				tile_style = int(tile[1:3])
				tile_path = int(tile[3:5])

				current_tile = self.tiles[current_col][current_row]

				current_tile.type = tile_type
				current_tile.style = tile_style
				current_tile.path_id = tile_path

				if tile_path > 0:
					self.path_nodes.append(current_tile)

				current_col += 1

			current_row += 1
			current_col = 0

		for x in range(20):
			self.enemies.append(Monster(self.path_nodes[0].center_x()+random.randint(-5, 5), self.path_nodes[0].center_y()+random.randint(-15, 15), self.path_nodes[1].center_x(), self.path_nodes[1].center_y()))

# End of File game_objects.py