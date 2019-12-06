
from state import State
from dfa import DFA
from edge import Edge
from point import Point

import pygame as pg

class GUI:

	def __init__(self):

		pg.init()

		self.dimensions = 600

		# Color Pallete
		self.STATE_COLOR = (255, 255, 255)
		self.EDGE_COLOR = (255, 255, 255)
		self.TEXT_COLOR = (255, 255, 255)

		# Fonts

		# State Parameters
		self.STATE_RADIUS = 10

		# Edge Parameters
		self.EDGE_THICKNESS = 2

		self.dfa = None


	def _render_DFA(self):

		if self.dfa:
			# Draw DFA
			pass

	def _undo(self):
		print("Undo Command", flush=True)
		pass


	def _handle_input(self, keys, key_string):
		
		# Modifier Command
		if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:

			if keys[pg.K_z]:
				self._undo()

			return

		# State instantiation command

		state = State







	def run_gui(self):

		screen = pg.display.set_mode((self.dimensions, self.dimensions))    
		pg.display.set_caption('Interactive DFA')

		while True:

			# Exit Condition
			e = pg.event.poll()
			if e.type == pg.QUIT:
				return

			keys = pg.key.get_pressed()
			if e.type == pg.KEYDOWN:

				self._handle_input(keys, e.unicode)

				pg.display.update()
			


if __name__ == '__main__':
	
	gui = GUI()
	gui.run_gui()