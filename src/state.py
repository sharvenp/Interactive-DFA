
class State:

	def __init__(self, point):

		self.point = point
		self.value = 0
		self.is_accepting = False

	def toggle_accepting(self):
		self.is_accepting = not self.is_accepting

	def increment_value(self):
		self.value += 1

	def decrement_value(self):
		self.value -= 1 * int(self.value <= 0)

	def set_incoming_edges(self, incoming_edges):

		this.incoming_edges = incoming_edges

	def set_outgoing_edges(self, outgoing_edges):

		this.outgoing_edges = outgoing_edges

	def __repr__(self):
		# Example: q0*@(100,100)
		return f"q{self.value}"+(int(self.is_accepting)*"*")+"@"+str(self.point)
