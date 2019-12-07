
from observable import Observable

class DFA(Observable):

	def __init__(self):

		Observable.__init__(self)

		self.states = []
		self.start_state = None
		self.selected_state = None

	def add_state(self, state):
		self.states.append(state)
		
		# Sort based on value
		self.states = sorted(self.states, key=lambda s: s.value)
		
		self.start_state = self.states[0]

		self.notify_observers()