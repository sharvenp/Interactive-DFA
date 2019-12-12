
import pygame as pg
from point import Point
from state import State
from settings import Settings

import math as m
from tkinter import *

class Controller:

	def __init__(self):

		self.drag = False

	def set_model(self, dfa):
		self.dfa = dfa

	
	def _undo(self):
		print("Undo Command")

	def create_text_window(self):

		self.string = ""

		master = Tk()
		e = Entry(master, width=80)
		e.pack()

		e.focus_set()

		def parse_on_action(m=master):
		    self.string = e.get()
		    master.destroy()

		b1 = Button(master, text = "Parse", width = 20, command=parse_on_action)
		b1.pack()

		b2 = Button(master, text = "Cancel", width = 20, command=master.destroy)
		b2.pack()

		mainloop()

	def _handle_keyboard_input(self, keys, mouse, e):
		
		if e.type == pg.KEYDOWN:

			if keys[pg.K_ESCAPE]: # Quit
				quit(0)

			elif keys[pg.K_BACKSPACE]: # Undo last command
				self._undo()

			elif keys[pg.K_UP]: # Increment State value
				self.dfa.update_selected_state_value(1)

			elif keys[pg.K_DOWN]: # Decrement State value
				self.dfa.update_selected_state_value(-1)

			elif keys[pg.K_SPACE]: # Toggle accepting
				self.dfa.toggle_accepting()

			elif keys[pg.K_DELETE]: # Delete object
				self.dfa.delete_selected_state()

			elif keys[pg.K_LSHIFT]: # Open input box
				self.create_text_window()
				self.dfa.parse_string(self.string)

			else: # Symbol click
				if e.unicode: # Create Edge
					mx, my = mouse.get_pos()
					self.dfa.create_edge(e.unicode, mx, my)



	def _handle_mouse_input(self, mouse, e):

		if e.type == pg.MOUSEBUTTONDOWN:

			mx, my = mouse.get_pos()

			if my > Settings.WINDOW_DIMENSION - Settings.DIVISION_HEIGHT - Settings.STATE_RADIUS:
				return

			if e.button == 1: # Select State
				self._select_state(mouse)
			elif e.button == 3: # Create State
				point = Point(mx, my)
				state = State(point)
				self.dfa.add_state(state)
			elif e.button == 4: # Increase Edge Bend
				self.dfa.update_bend(mx, my, 1)
			elif e.button == 5: # Decrease Edge Bend
				self.dfa.update_bend(mx, my, -1)

			self.drag = True

		elif e.type == pg.MOUSEMOTION and self.drag and mouse.get_pressed()[0]:

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
		