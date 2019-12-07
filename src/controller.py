
import pygame as pg
from point import Point
from state import State
from settings import Settings

import math as m

class Controller:

	def __init__(self):

		self.drag = False

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


	def _select_state(self, mouse):

		mx, my = mouse.get_pos()
		self.dfa.select_state(mx, my)

	def _move_selected_state(self, mouse):
		mx, my = mouse.get_pos()
		self.dfa.update_selected_state_point(mx, my)

	def handle(self, e, key, mouse):

		keys = key.get_pressed()

		if e.type == pg.QUIT: 
			quit(0)

		if e.type == pg.KEYDOWN:

			self._handle_keyboard_input(keys)
		
		elif e.type == pg.MOUSEBUTTONDOWN:

			self._select_state(mouse)
			self.drag = True

		elif e.type == pg.MOUSEMOTION and self.drag:

			self._move_selected_state(mouse)

		elif e.type == pg.MOUSEBUTTONUP:

			self.drag = False
