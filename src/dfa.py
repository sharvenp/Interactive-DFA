
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

		self.parsed_string = ""
		self.curr_index = 0
		self.curr_state = None
		self.is_parsing = False

	def add_state(self, state):
		self.states.append(state)
		
		# Sort based on value
		self.states = sorted(self.states, key=lambda s: s.value)

		if len(self.states) == 1: # This is the first state added
			self.start_state = state

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
		
		deleted_transitions = []
		k = 0
		while k < len(self.transition_table):

			found_transition = False

			fr, s, to, bend = self.transition_table[k]
			if fr == self.selected_state or to == self.selected_state:
				found_transition = True
				deleted_transitions.append(self.transition_table.pop(k))
				k = 0

			k += 1 * int(not found_transition)

		
		# Remove selected state from states
		removed_state = self.states.pop(i)
		del removed_state

		# Remove all transitions in the transition table involving the selected state
		deleted_transitions.clear()
		del deleted_transitions[:]

		self.states = sorted(self.states, key=lambda s: s.value)

		if self.start_state == self.selected_state:
			if self.states:
				self.start_state = self.states[0]
			else:
				self.start_state = None
			
		self.selected_state = None

		self.notify_observers()

	def create_edge(self, symbol, mx, my):

		to_state = self._get_state(mx, my)

		if self.selected_state and to_state:
			
			# Check to make sure there are no duplicates
			for i in range(len(self.transition_table)):
				fr, s, to, bend = self.transition_table[i]
				if self.selected_state == fr and to_state == to and symbol in s:
					# Duplicate
					s.pop(s.index(symbol))
					if len(s) == 0:
						self.transition_table.pop(i)
					self.notify_observers()
					return

				elif self.selected_state == fr and to_state == to and symbol not in s:
					s.append(symbol)
					self.transition_table[i] = (fr, s, to, bend)
					self.notify_observers()
					return

			# New transition
			self.transition_table.append((self.selected_state, [symbol], to_state, Settings.EDGE_DEFAULT_BEND))

		self.notify_observers()

	def update_bend(self, mx, my, sign):

		delta = sign * Settings.BEND_DELTA

		to_state = self._get_state(mx, my)

		for i in range(len(self.transition_table)):

			fr, s, to, bend = self.transition_table[i]

			if self.selected_state == fr and to == to_state:

				bend += delta
				bend = max(Settings.EDGE_DEFAULT_BEND, bend)

				self.transition_table[i] = (fr, s, to, bend)

		self.notify_observers()
		

	def set_start(self):

		if self.selected_state:
			self.start_state = self.selected_state

			self.notify_observers()

	def check_unique(self):

		if not self.states or not self.transition_table:
			# DFA is empty
			return False

		# Check if states are unique
		for i in range(len(self.states)):
			for j in range(i+1, len(self.states)):
				if self.states[i].value == self.states[j].value:
					# Duplicate State
					return False

		return True


	def _transition(self, curr_state, symbol):

		for transition in self.transition_table:
			fr, s, to, bend = transition
			if fr == curr_state and symbol in s:
				return to			

	def parse_string(self, alphabet, string):

		self.parsed_string = string
		print("Parsing:", string, "with Alphabet:", list(set(alphabet)))

		# Check if string/DFA uses only the given alphabets
		symbols_used = []
		for transition in self.transition_table:
			symbols_used.extend(transition[1])

		symbols_used = list(set(symbols_used))

		if symbols_used != list(set(alphabet)):
			return 1;

		for c in string:
			if c not in alphabet:
				return 1

		# Check if there is atleast one accepting state
		found_accepting = False
		for state in self.states:
			if state.is_accepting:
				found_accepting = True
				break

		if not found_accepting:
			return 4

		# Check if all states have transitions defined for all the alphabets
		transition_dictionary = {}
		for state in self.states:
			transition_dictionary[state] = []

		for transition in self.transition_table:
			fr, s, to, bend = transition
			for c in s:
				if c in transition_dictionary[fr]:
					return 3
				transition_dictionary[fr].append(c)

		list_alphabet = list(set(alphabet))
		list_alphabet.sort()
		for key in transition_dictionary:
			transition_dictionary[key].sort()
			if transition_dictionary[key] != list_alphabet:
				return 2

		# === DFA should be valid at this point === #
		self.curr_state = self.start_state
		
		self.is_parsing = True
		
		for i in range(len(self.parsed_string)):
			self.curr_index = i
			self.curr_state = self._transition(self.curr_state, self.parsed_string[i])		
			self.notify_observers()
		
		self.is_parsing = False

		if self.curr_state.is_accepting:
			return -1
		else:
			return -2


	def save(self, path):

		with open(path, 'w') as file:
			for state in self.states:
				file.write(str(state)+"\n")
			for transition in self.transition_table:
				file.write(str(transition).replace(" ", "").replace("(", "").replace(")","")+"\n")

	def load(self, path):

		with open(path, 'r') as file:
			
			for line in file:
				

