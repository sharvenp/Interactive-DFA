
from point import Point

class State:

	def __init__(self, point):

		self.point = point
		self.value = 0

		self.is_accepting = False

	def toggle_accepting(self):
		self.is_accepting = not self.is_accepting

	def update_value(self, val):
		self.value += val
		self.value = max(self.value, 0)

	def __repr__(self):
		# Example: q0*@(100,100)
		return f"q{self.value}"+(int(self.is_accepting)*"*")+"@"+str(self.point)
