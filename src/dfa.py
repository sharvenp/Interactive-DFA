
from observable import Observable
from settings import Settings

import math as m

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

	def select_state(self, mx, my):

		self.selected_state = None

		# Find the clicked state
		for state in self.states:

			sx, sy = state.point.x, state.point.y
			distance = m.sqrt(((mx - sx)**2) + ((my - sy)**2))

			if distance <= Settings.STATE_RADIUS:
				self.selected_state = state
				break


		self.notify_observers()

	def update_selected_state_point(self, mx, my):

		if self.selected_state:
			self.selected_state.point.x = mx
			self.selected_state.point.y = my

		self.notify_observers()

	def update_selected_state_value(self, val):

		if self.selected_state:
			self.selected_state.update_value(val)

		self.notify_observers()

	def toggle_accepting(self):

		if self.selected_state:
			self.selected_state.toggle_accepting()

		self.notify_observers()