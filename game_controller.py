# Filename game_controller.py
# Rudimentary click handling object that makes updates based on interaction

import pygame
from pygame.locals import *
from game_objects import *


class Controller():
	IDLE = 0
	PLACE_TOWER = 1
	TOWER_ONE = 1
	def __init__(self, map, input, towerData):
		self.map = map
		self.input = input
		self.state = Controller.IDLE
		self.selectedTower = 0
		self.towerList = towerData
	
	def update():
		#When update is called, we check the state of the mouse and make a call if it's down
		#Ask the map which tile is hovered.
		tmpTile = map.hover_tile
		if input.mouse_down():
			#evaluate our status
			if self.state == Controller.PLACE_TOWER:
				# place tower logic here, use the god damn map. Create a new tower object and add it to the map
				# we should check if we're in a valid tile, too.
				if tmpTile.type == TYPE_PLOT:
					newTower = Tower(tmpTile, towerList[selectedTower])
					map.towers.push_back(newTower)
				