
from observable import Observable
from settings import Settings
from point import Point

import math as m

class DFA(Observable):

	def __init__(self):

		Observable.__init__(self)

		self.states = []
		self.transition_table = []
		self.start_state = None
		self.selected_state = None

	def add_state(self, state):
		self.states.append(state)
		
		# Sort based on value
		self.states = sorted(self.states, key=lambda s: s.value)
		
		self.start_state = self.states[0]

		self.notify_observers()

	def _get_state(self, x, y):

		returned_state = None

		# Find the clicked state
		for state in self.states:

			sx, sy = state.point.x, state.point.y
			distance = m.sqrt(((x - sx)**2) + ((y - sy)**2))

			if distance <= Settings.STATE_RADIUS:
				returned_state = state
				break

		return returned_state


	def select_state(self, mx, my):

		self.selected_state = self._get_state(mx, my)
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

	def delete_selected_state(self):

		i = self.states.index(self.selected_state)

		self.selected_state = None

		removed_state = self.states.pop(i)
		del removed_state

		self.states = sorted(self.states, key=lambda s: s.value)
		self.start_state = self.states[0]

		self.notify_observers()

	def create_edge(self, symbol, mx, my):

		to_state = self._get_state(mx, my)

		if self.selected_state and to_state:
			
			# Check to make sure there are no duplicates
			for i in range(len(self.transition_table)):
				fr, s, to = self.transition_table[i]
				if self.selected_state == fr and to_state == to and symbol in s:
					# Duplicate
					s.pop(s.index(symbol))
					if len(s) == 0:
						self.transition_table.pop(i)
					self.notify_observers()
					return

				elif self.selected_state == fr and to_state == to and symbol not in s:
					s.append(symbol)
					self.transition_table[i] = (fr, s, to)
					self.notify_observers()
					return

			# New transition
			self.transition_table.append((self.selected_state, [symbol], to_state))

		self.notify_observers()
		