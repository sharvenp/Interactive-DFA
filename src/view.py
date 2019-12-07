
from state import State
from dfa import DFA
from edge import Edge
from point import Point
from observer import Observer

import pygame as pg

class View(Observer):

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

		self.selected_state = None


	def attach_controller(self, controller):
		self.controller = controller

	def _render_DFA(self, dfa):

		self.screen.fill(self.BACKGROUND_COLOR)

		for state in dfa.states:
			
			x, y = state.point.x, state.point.y

			thickness = self.STATE_DEFAULT_THICKNESS

			# Change thickness base on accepting
			if state.is_accepting:
				thickness = self.STATE_ACCEPTING_THICKNESS

			# Draw circle
			pg.draw.circle(self.screen, self.STATE_COLOR, (x, y), self.STATE_RADIUS, thickness)

			# Label circle
			label_string = "q"+str(state.value)
			label_surface = self.DFA_FONT.render(label_string, True, self.TEXT_COLOR)
			
			# Center the text
			label_rect = label_surface.get_rect(center=(x, y))

			# Draw label
			self.screen.blit(label_surface, label_rect)


	def _undo(self):
		print("Undo Command")


	def update(self, dfa):
		self._render_DFA(dfa)
		pg.display.update()

	def launch(self):

		self.screen = pg.display.set_mode((self.dimensions, self.dimensions))    
		pg.display.set_caption("Interactive DFA")

		while True:

			# Exit Condition
			e = pg.event.poll()
			key = pg.key
			mouse = pg.mouse
			self.controller.handle(e, key, mouse)
			
