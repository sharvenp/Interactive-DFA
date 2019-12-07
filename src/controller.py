
import pygame as pg
from point import Point
from state import State
from settings import Settings

import math as m

class Controller:

	def set_model(self, dfa):
		self.dfa = dfa

	def _handle_keyboard_input(self, keys):
		
		if keys[pg.K_z]: # Undo last command
			self._undo()

		elif keys[pg.K_s]: # Create State
			mx, my = pg.mouse.get_pos()
			point = Point(mx, my)
			state = State(point)
			self.dfa.add_state(state)


	def _handle_mouse_input(self, mouse):

		mx, my = mouse.get_pos()

		selected_state = None

		# Find the clicked state
		for state in self.dfa.states:

			sx, sy = state.point.x, state.point.y
			distance = m.sqrt(((mx - sx)**2) + ((my - sy)**2))

			if distance <= Settings.STATE_RADIUS:
				selected_state = state
				break

		self.dfa.select_state(selected_state)


	def handle(self, e, key, mouse):

		keys = key.get_pressed()

		if e.type == pg.QUIT: 
			quit(0)

		if e.type == pg.KEYDOWN:

			self._handle_keyboard_input(keys)
		
		elif e.type == pg.MOUSEBUTTONDOWN:

			self._handle_mouse_input(mouse)

