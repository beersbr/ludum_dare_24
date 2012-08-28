# Filename: g_input_controller.py

import pygame, sys, os
from pygame.locals import *
from g_input_handler import *

# InputController:
# This is going to attempt to be a more generic version of the prevous controller. This
# is an awesome abstraction and will be used to dish out events. It will maintain the 
# game focus (as in item focus and blur), and will dish out events to the entities that 
# are listening

# For right now this will maintain  a list of listeners. When an event happens then
# the object will iterate over the listeners and dish out the evenst appropriately. The 
# listeners will eventually be put into a tree, for right now they will be iterated over
# in a linear manner.

class InputController():
	def __init__(self):
		self.listeners = []
		self.input = InputHander()
		

# End of g_input_controller.py