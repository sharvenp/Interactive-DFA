
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

	
	def _undo(self):
		print("Undo Command")


	def _handle_keyboard_input(self, keys, mouse, e):
		
		if e.type == pg.KEYDOWN:

			if keys[pg.K_BACKSPACE]: # Undo last command
				self._undo()

			elif keys[pg.K_UP]: # Increment State value
				self.dfa.update_selected_state_value(1)

			elif keys[pg.K_DOWN]: # Decrement State value
				self.dfa.update_selected_state_value(-1)

			elif keys[pg.K_SPACE]: # Toggle accepting
				self.dfa.toggle_accepting()

			elif keys[pg.K_DELETE]: # Delete object
				self.dfa.delete_selected_state()

			else: # Symbol click
				if e.unicode: # Create Edge
					mx, my = mouse.get_pos()
					self.dfa.create_edge(e.unicode, mx, my)



	def _handle_mouse_input(self, mouse, e):

		buttons = mouse.get_pressed()	

		if e.type == pg.MOUSEBUTTONDOWN:

			if buttons[0]: # Select State
				self._select_state(mouse)
			elif buttons[2]: # Create State
				mx, my = mouse.get_pos()
				point = Point(mx, my)
				state = State(point)
				self.dfa.add_state(state)

			self.drag = True

		elif e.type == pg.MOUSEMOTION and self.drag and buttons[0]:

			self._move_selected_state(mouse)

		elif e.type == pg.MOUSEBUTTONUP:

			self.drag = False

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

		self._handle_keyboard_input(keys, mouse, e)
		self._handle_mouse_input(mouse, e)
		