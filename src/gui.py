
from state import State
from dfa import DFA
from edge import Edge
from point import Point

import pygame as pg

class GUI:

	def __init__(self):

		pg.init()

		self.dimensions = 700

		# Color Pallete
		self.BACKGROUND_COLOR = (0, 0, 0)
		self.STATE_COLOR = (255, 255, 255)
		self.SELECTED_COLOR = (255, 180, 180)
		self.ACCEPTING_COLOR = (180, 255, 180)
		self.EDGE_COLOR = (255, 255, 255)
		self.TEXT_COLOR = (255, 255, 255)

		# Fonts
		self.DFA_FONT = pg.font.SysFont('Consolas', 25)

		# State Parameters
		self.STATE_RADIUS = 40
		self.STATE_DEFAULT_THICKNESS = 2
		self.STATE_ACCEPTING_THICKNESS = 5

		# Edge Parameters
		self.EDGE_THICKNESS = 3

		self.dfa = DFA()


	def _render_DFA(self):

		self.screen.fill(self.BACKGROUND_COLOR)

		for state in self.dfa.states:
			
			x, y = state.point.x, state.point.y

			thickness = self.STATE_DEFAULT_THICKNESS

			if state.is_accepting:
				thickness = self.STATE_ACCEPTING_THICKNESS

			pg.draw.circle(self.screen, self.STATE_COLOR, (x, y), self.STATE_RADIUS, thickness)

			label_string = "q"+str(state.value)
			label_surface = self.DFA_FONT.render(label_string, True, self.TEXT_COLOR)
			
			# Center the text
			label_rect = label_surface.get_rect(center=(x, y))

			self.screen.blit(label_surface, label_rect)


	def _undo(self):
		print("Undo Command")


	def _handle_input(self, keys, event):
		
		if keys[pg.K_z]: # Undo last command
			self._undo()

		elif keys[pg.K_s]: # Create State
			mx, my = pg.mouse.get_pos()
			point = Point(mx, my)
			state = State(point)
			self.dfa.add_state(state)







	def run_gui(self):

		self.screen = pg.display.set_mode((self.dimensions, self.dimensions))    
		pg.display.set_caption("Interactive DFA")

		while True:

			# Exit Condition
			e = pg.event.poll()
			if e.type == pg.QUIT:
				return

			keys = pg.key.get_pressed()
			if e.type == pg.KEYDOWN:

				self._handle_input(keys, e)
				
				self._render_DFA()

				pg.display.update()
			


if __name__ == '__main__':
	
	gui = GUI()
	gui.run_gui()