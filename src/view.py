
from state import State
from dfa import DFA
from point import Point
from observer import Observer
from settings import Settings

import pygame as pg
import math as m
import time as t

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
	def _symbol_list_to_string(self, s):

		out = ""

		for i in range(len(s)):

			if i == len(s) - 1:
				out += s[i]
			else:
				out += s[i] + ","

		return out

	def _render_DFA(self, dfa):

		self.screen.fill(Settings.BACKGROUND_COLOR)

		# Draw Edges
		for transition in dfa.transition_table:
			fr, symbol_list, to, bend = transition

			symbol_list.sort()
				
			s = self._symbol_list_to_string(symbol_list)
			x, y = fr.point.x, fr.point.y
			tx, ty = to.point.x, to.point.y

			if fr == to: # Transition to same state

				# Draw arc
				pg.draw.arc(self.screen, Settings.EDGE_COLOR, \
							(x - Settings.STATE_RADIUS//2, y - 90, Settings.STATE_RADIUS, 180), \
							0, m.pi, Settings.EDGE_THICKNESS)

				# Draw arrow
				arrow_points = [(x - Settings.ARROW_WIDTH//2, y - 105 + Settings.ARROW_HEIGHT), 
								(x + Settings.ARROW_WIDTH//2, y - 105 + 2*Settings.ARROW_HEIGHT),
							    (x - Settings.ARROW_WIDTH//2, y - 105 + 3*Settings.ARROW_HEIGHT), 
							    (x - Settings.ARROW_WIDTH//2, y - 105 + Settings.ARROW_HEIGHT)]
				pg.draw.polygon(self.screen, Settings.EDGE_COLOR, arrow_points)

				font = pg.font.SysFont(Settings.SYMBOL_FONT[0], Settings.SYMBOL_FONT[1])
				symbol_surface = font.render(s, True, Settings.STATE_COLOR)
				symbol_rect = symbol_surface.get_rect(center=(x, y - 110))
				self.screen.blit(symbol_surface, symbol_rect)


			else: # Transition to different state

				try:

					mid_x = (tx + x) // 2
					mid_y = (ty + y) // 2
					distance = m.sqrt(((x - tx)**2) + ((y - ty)**2))

					major_axis = distance
					minor_axis = bend
					ellipse_surface = pg.Surface((major_axis, minor_axis + 4*Settings.ARROW_HEIGHT), pg.SRCALPHA, 32)
					ellipse_surface = ellipse_surface.convert_alpha()
					
					# Draw arc
					pg.draw.arc(ellipse_surface, Settings.EDGE_COLOR, (0, 2*Settings.ARROW_HEIGHT, major_axis, minor_axis - 2*Settings.ARROW_HEIGHT), 0, m.pi, Settings.EDGE_THICKNESS)
					
					# Draw arrow
					arrow_points = [(major_axis//2 - Settings.ARROW_WIDTH, Settings.ARROW_HEIGHT), 
									(major_axis//2 + Settings.ARROW_WIDTH, 2*Settings.ARROW_HEIGHT),
								    (major_axis//2 - Settings.ARROW_WIDTH, 3*Settings.ARROW_HEIGHT), 
								    (major_axis//2 - Settings.ARROW_WIDTH, Settings.ARROW_HEIGHT)]
					pg.draw.polygon(ellipse_surface, Settings.EDGE_COLOR, arrow_points)

					# Rotate arc surface
					rotation = -m.degrees(m.atan2(ty - y, tx - x))
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

				except:

					print("Error!")


		# Draw start state arrow
		if dfa.start_state:
			sx, sy = dfa.start_state.point.x, dfa.start_state.point.y 	
			pg.draw.line(self.screen, Settings.EDGE_COLOR, (sx - Settings.START_ARROW_LENGTH - Settings.STATE_RADIUS, sy), (sx, sy), Settings.EDGE_THICKNESS)
			arrow_points = [(sx - Settings.STATE_RADIUS, sy), 
							(sx - Settings.STATE_RADIUS - Settings.ARROW_WIDTH, sy - Settings.ARROW_HEIGHT),
						    (sx - Settings.STATE_RADIUS - Settings.ARROW_WIDTH, sy + Settings.ARROW_HEIGHT), 
						    (sx - Settings.STATE_RADIUS, sy)]
			pg.draw.polygon(self.screen, Settings.EDGE_COLOR, arrow_points)

		# Draw States
		for state in dfa.states:
			
			x, y = state.point.x, state.point.y

			color = Settings.STATE_COLOR

			# Change color if it is selected
			if state == dfa.selected_state:
				color = Settings.SELECTED_COLOR

			if dfa.is_parsing and state == dfa.curr_state:
				color = Settings.PARSE_COLOR

			# Draw circle
			pg.draw.circle(self.screen, color, (x, y), Settings.STATE_RADIUS)
			pg.draw.circle(self.screen, Settings.BACKGROUND_COLOR, (x, y), Settings.STATE_RADIUS - Settings.STATE_THICKNESS)

			# Draw inner circle if accepting
			if state.is_accepting:
				pg.draw.circle(self.screen, color, (x, y), Settings.STATE_ACCEPTING_INNER_RADIUS, Settings.STATE_THICKNESS)

			# Label circle
			label_string = "q"+str(state.value)
			font = pg.font.SysFont(Settings.DFA_FONT[0], Settings.DFA_FONT[1], state.is_accepting)
			label_surface = font.render(label_string, True, color)
			
			# Center the text
			label_rect = label_surface.get_rect(center=(x, y))

			# Draw label
			self.screen.blit(label_surface, label_rect)

		# Draw Division line
		pg.draw.line(self.screen, Settings.STATE_COLOR, (0, Settings.WINDOW_DIMENSION - Settings.DIVISION_HEIGHT), \
					(Settings.WINDOW_DIMENSION, Settings.WINDOW_DIMENSION - Settings.DIVISION_HEIGHT))


		# If DFA is parsing, draw the parsing text
		if dfa.is_parsing:

			font_size = Settings.WINDOW_DIMENSION // len(dfa.parsed_string)
			font = pg.font.SysFont('Consolas', font_size)
			characters = []
			for i, c in enumerate(dfa.parsed_string):
				# s = " " * i + c
				s=c
				color = Settings.STATE_COLOR

				if dfa.curr_index == i:
					color = Settings.PARSE_COLOR

				s_image = font.render(s, True, color)
				characters.append(s_image)

			for i in range(len(characters)):
				self.screen.blit(characters[i], (i * font_size, Settings.WINDOW_DIMENSION - (Settings.DIVISION_HEIGHT // 2) - (font_size // 2), font_size, font_size))


	def update(self, dfa):

		self._render_DFA(dfa)
		pg.display.update()

		if dfa.is_parsing:
			t.sleep(Settings.PARSE_DELAY)

	def launch(self):

		self.screen = pg.display.set_mode((Settings.WINDOW_DIMENSION, Settings.WINDOW_DIMENSION))    
		pg.display.set_caption("Interactive DFA")

		# Draw Division line
		pg.draw.line(self.screen, Settings.STATE_COLOR, (0, Settings.WINDOW_DIMENSION - Settings.DIVISION_HEIGHT), \
					(Settings.WINDOW_DIMENSION, Settings.WINDOW_DIMENSION - Settings.DIVISION_HEIGHT))
		pg.display.update()

		while True:

			# Get all types of input and feed it into the controller
			e = pg.event.poll()
			key = pg.key
			mouse = pg.mouse
			self.controller.handle(e, key, mouse)
			
