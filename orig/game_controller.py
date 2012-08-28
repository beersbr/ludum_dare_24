# Filename game_controller.py
# Rudimentary click handling object that makes updates based on interaction

import pygame
from pygame.locals import *
from game_objects import *

class Controller():
	IDLE = 0
	PLACE_TOWER = 1
	TOWER_ONE = 1
	def __init__(self, towerData):
		#self.map = map
		#self.input = input
		self.state = Controller.IDLE
		self.selectedTower = 0
		self.towerList = towerData
	
	def update(self, map, input):
		#When update is called, we check the state of the mouse and make a call if it's down
		#Ask the map which tile is hovered.
		tmpTile = map.hover_tile
		if input.mouse_down():
			#evaluate our status
			if self.state == Controller.PLACE_TOWER:
				# place tower logic here, use the god damn map. Create a new tower object and add it to the map
				# we should check if we're in a valid tile, too.
				if tmpTile.type == tmpTile.TYPE_PLOT:
					newTower = Tower(tmpTile, self.towerList[self.selectedTower])
					map.towers.append(newTower)
					self.state = Controller.IDLE
					# print "Tower created!\n"

		if self.state == Controller.IDLE:
			if input.key_down(K_1):
				if 0 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 0

			if input.key_down(K_2):
				if 1 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 1

			if input.key_down(K_3):
				if 2 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 2

			if input.key_down(K_4):
				if 3 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 3

			if input.key_down(K_5):
				if 4 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 4

			if input.key_down(K_6):
				if 5 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 5

			if input.key_down(K_7):
				if 6 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 6

			if input.key_down(K_8):
				if 7 < len(self.towerList):
					self.state = Controller.PLACE_TOWER
					self.selectedTower = 7

				