# Filename: g_vector.py

import math

class Vector2d():
	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y

	def __str__(self):
		return ("("+str(self.x)+", "+str(self.y)+")")

	def __add__(self, vect):
		return Vector2d( (self.x+vect.x), (self.y+vect.y))

	def __sub__(self, vect):
		return Vector2d( (self.x-vect.x), (self.y-vect.y))

	def __mul__(self, scalar):
		return Vector2d( (self.x * scalar), (self.y * scalar))

	def __div__(self, scalar):
		if(sclar == 0):
			return None
		return Vector2d( (self.x/scalar), (self.y/scalar))

	def distance(self, vect):
		dx = self.x - vect.x
		dy = self.y - vect.y

		return math.sqrt(dx*dx, dy*dy)

	def set_coords(self, x, y):
		self.x = x
		self.y = y
		return self

	def set_vector(self, vect):
		self.x = vect.x
		self.y = vect.y
		return self

	def set_array(self, ar):
		self.x, self.y = ar
		return self

	def to_array(self):
		return (self.x, self.y)

	def normalize(self):
		length = math.sqrt(self.x*self.x, self.y*self.y)
		if(length == 0)
			return Vector2d(0.0, 0.0)
		return Vector2d( (self.x/lenth), (self.y/length))

	def dot_product(self, vect):
		return ((self.x * vect.x) + self.y * vect.y))


# End of g_vectory.py