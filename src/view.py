
from state import State
from dfa import DFA
from edge import Edge
from point import Point
from observer import Observer
from settings import Settings


import pygame as pg

class View(Observer):

	def __init__(self):

		pg.init()

	def attach_controller(self, controller):
		self.controller = controller

	def _render_DFA(self, dfa):

		self.screen.fill(Settings.BACKGROUND_COLOR)

		for state in dfa.states:
			
			x, y = state.point.x, state.point.y

			thickness = Settings.STATE_DEFAULT_THICKNESS
			color = Settings.STATE_COLOR

			# Change thickness base on accepting
			if state.is_accepting:
				thickness = Settings.STATE_ACCEPTING_THICKNESS
				color = Settings.ACCEPTING_COLOR

			# Change color if it is selected
			if state.is_selected:
				color = Settings.SELECTED_COLOR

			# Draw circle
			pg.draw.circle(self.screen, color, (x, y), Settings.STATE_RADIUS, thickness)

			# Label circle
			label_string = "q"+str(state.value)
			font = pg.font.SysFont(Settings.DFA_FONT[0], Settings.DFA_FONT[1])
			label_surface = font.render(label_string, True, color)
			
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

		self.screen = pg.display.set_mode((Settings.dimensions, Settings.dimensions))    
		pg.display.set_caption("Interactive DFA")

		while True:

			# Get all types of input and feed it into the controller
			e = pg.event.poll()
			key = pg.key
			mouse = pg.mouse
			self.controller.handle(e, key, mouse)
			
