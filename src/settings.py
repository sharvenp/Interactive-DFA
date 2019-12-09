
import pygame as pg

class Settings:

	dimensions = 700

	# Color Pallete
	BACKGROUND_COLOR = (0, 0, 0)
	STATE_COLOR = (255, 255, 255)
	SELECTED_COLOR = (120, 255, 120)
	EDGE_COLOR = (255, 255, 255)

	# Fonts
	DFA_FONT = ('Consolas', 22)
	SYMBOL_FONT = ('Consolas', 19)


	# State Parameters
	STATE_RADIUS = 40
	STATE_DEFAULT_THICKNESS = 2
	STATE_ACCEPTING_THICKNESS = 8

	# Edge Parameters
	EDGE_THICKNESS = 2
	EDGE_DEFAULT_BEND = 180