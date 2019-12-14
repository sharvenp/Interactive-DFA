
import pygame as pg
from point import Point
from state import State
from settings import Settings

import math as m
from tkinter import messagebox
from tkinter import *

class Controller:

	"""
	
	
	"""

	def __init__(self):

		self.drag = False

	def set_model(self, dfa):
		self.dfa = dfa

	
	def _undo(self):
		print("Undo Command")

	def _save(self):
		print("Save Command")

	def _load(self):
		print("Load Command")

	def get_string_from_user(self):

		self.string = ""

		if self.dfa.check_valid():

			master = Tk()
			master.title("Input String")
			e = Entry(master, width=80)
			e.pack()

			e.focus_set()

			def alarm(self, e=e):
				e.focus_force()
				e.bell()

			e.bind("<FocusOut>", alarm)	

			def parse_on_action(m=master):
			    self.string = e.get()	
			    master.destroy()

			b1 = Button(master, text = "Parse", width = 20, command=parse_on_action)
			b1.pack()

			b2 = Button(master, text = "Cancel", width = 20, command=master.destroy)
			b2.pack()

			mainloop()

		else:

			root = Tk()
			root.withdraw()
			messagebox.showerror("Invalid DFA", "The drawn DFA is not valid.\nTroubleshooting:\n-Check")


	def _handle_keyboard_input(self, keys, mouse, e):
		
		if e.type == pg.KEYDOWN:

			if keys[pg.K_ESCAPE]: # Quit
				quit(0)


			if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]: # Ctrl key pressed

				if keys[Settings.KEY_EXIT]:
					quit(0)

				elif keys[Settings.KEY_ACCEPTING]: # Toggle accepting
					self.dfa.toggle_accepting()

				elif keys[Settings.KEY_SET_START]: # Set start state
					self.dfa.set_start()

				elif keys[Settings.KEY_UNDO]: # Undo last command
					self._undo()

				elif keys[Settings.KEY_SAVE]: # Save dfa
					self._save()

				elif keys[Settings.KEY_LOAD]: # Load dfa
					self._load()

				elif keys[Settings.KEY_INPUT_STRING]: # Open input box
					self.get_string_from_user()
					self.dfa.parse_string(self.string)


			if keys[pg.K_UP]: # Increment State value
				self.dfa.update_selected_state_value(1)

			elif keys[pg.K_DOWN]: # Decrement State value
				self.dfa.update_selected_state_value(-1)

			elif keys[pg.K_DELETE]: # Delete object
				self.dfa.delete_selected_state()

			else: # Symbol click
				if e.unicode: # Create Edge
					mx, my = mouse.get_pos()
					self.dfa.create_edge(e.unicode, mx, my)



	def _handle_mouse_input(self, mouse, e):

		mx, my = mouse.get_pos()	

		if e.type == pg.MOUSEBUTTONDOWN:

			if my > Settings.WINDOW_DIMENSION - Settings.DIVISION_HEIGHT - Settings.STATE_RADIUS:
				return

			if e.button == 1: # Select State
				self.dfa.select_state(mx, my)
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

			self.dfa.update_selected_state_point(mx, my)

		elif e.type == pg.MOUSEBUTTONUP:

			self.drag = False

	def handle(self, e, key, mouse):

		keys = key.get_pressed()

		if e.type == pg.QUIT: 
			quit(0)

		self._handle_keyboard_input(keys, mouse, e)
		self._handle_mouse_input(mouse, e)
		