
from state import State
from dfa import DFA
from point import Point
from observer import Observer
from settings import Settings

import pygame as pg
import math as m

class View(Observer):

	def __init__(self):

		pg.init()

	def attach_controller(self, controller):
		self.controller = controller

	def _get_sign(self, val):

		if val >= 0:
			return 1
		else:
			return -1

	def _render_DFA(self, dfa):

		self.screen.fill(Settings.BACKGROUND_COLOR)

		# Draw Edges
		for transition in dfa.transition_table:
			fr, s, to = transition
			
			x, y = fr.point.x, fr.point.y
			tx, ty = to.point.x, to.point.y

			if fr == to: # Transition to same state

				pg.draw.arc(self.screen, Settings.EDGE_COLOR, \
							(x - Settings.STATE_RADIUS//2, y - Settings.EDGE_DEFAULT_BEND//2, Settings.STATE_RADIUS, Settings.EDGE_DEFAULT_BEND), \
							0, m.pi, Settings.EDGE_THICKNESS)

			else: # Transition to different state

				mid_x = (tx + x) // 2
				mid_y = (ty + y) // 2
				distance = m.sqrt(((x - tx)**2) + ((y - ty)**2))

				major_axis = distance
				minor_axis = Settings.EDGE_DEFAULT_BEND
				ellipse_surface = pg.Surface((major_axis, minor_axis), pg.SRCALPHA, 32)
				ellipse_surface = ellipse_surface.convert_alpha()
				
				# Draw arc
				pg.draw.arc(ellipse_surface, Settings.EDGE_COLOR, (0, 0, major_axis, minor_axis), m.pi, 2*m.pi, Settings.EDGE_THICKNESS)
				
				# Rotate arc surface
				rotation = -m.degrees(m.atan2(y - ty, x - tx))
				ellipse_center = ellipse_surface.get_rect().center
				rotated_ellipse = pg.transform.rotate(ellipse_surface, rotation)
				rotated_rect = rotated_ellipse.get_rect(center=(mid_x, mid_y))

				# Apply arc surface to screen
				self.screen.blit(rotated_ellipse, (rotated_rect.x, rotated_rect.y))

				# Draw label
				font = pg.font.SysFont(Settings.SYMBOL_FONT[0], Settings.SYMBOL_FONT[1])
				symbol_surface = font.render(s, True, Settings.STATE_COLOR)
				symbol_rect = symbol_surface.get_rect(center=(mid_x, mid_y + self._get_sign(x - tx)*(minor_axis//2 + 20)))
				self.screen.blit(symbol_surface, symbol_rect)


		# Draw States
		for state in dfa.states:
			
			x, y = state.point.x, state.point.y

			thickness = Settings.STATE_DEFAULT_THICKNESS
			color = Settings.STATE_COLOR

			# Change thickness base on accepting
			if state.is_accepting:
				thickness = Settings.STATE_ACCEPTING_THICKNESS

			# Change color if it is selected
			if state == dfa.selected_state:
				color = Settings.SELECTED_COLOR

			# Draw circle
			pg.draw.circle(self.screen, color, (x, y), Settings.STATE_RADIUS)
			pg.draw.circle(self.screen, Settings.BACKGROUND_COLOR, (x, y), Settings.STATE_RADIUS - thickness)

			# Label circle
			label_string = "q"+str(state.value)
			font = pg.font.SysFont(Settings.DFA_FONT[0], Settings.DFA_FONT[1], state.is_accepting)
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
			
