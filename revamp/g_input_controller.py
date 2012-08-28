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

# For now, I am sticking with the event types that pygame provides. I think that will 
# cover all the bases for now.

# TODO: Only one instance of this class should be called at a time. Make this a singletone

# TODO: This needs some more thinking, Perhaps the the inputhandler should just be handed to 
# the objects that need it and there is no callback features that need to be added. The
# controller can a holder class for the input still but each object will implement its own
# controller methods via callbacks.

class InputController():
	_instance = None # for the singleton in the future
	_listener_id = 0

	def __init__(self):
		self.listeners = dict(pygame.KEYDOWN = [], pygame.KEYUP = [], pygame.MOUSEBUTTONDOWN = [], pygame.MOUSEBUTTONUP = [])
		self.input = InputHander()

	def listen(self, event_type, ls_obj, callback):
		if event_type in self.listeners.keys():
			InputController._listener_id += 1
			self.listeners[event_type].append( dict('id' = InputController._listener_id, 'callback' = callback, 'obj' = ls_obj))
			return InputController._listener_id
		return False

	# This is a wrapper function for the InputHandler()'s function fo the same name.
	def consume(self, event):
		return self.input.consume(event)

	# Broadcasts the events to all the listners
	def broadcast(self):
		pass


# End of g_input_controller.py