
import pygame as pg

class Settings:

	WINDOW_DIMENSION = 800
	DIVISION_HEIGHT = 100

	# Color Pallete
	BACKGROUND_COLOR = (0, 0, 0)
	STATE_COLOR = (255, 255, 255)
	SELECTED_COLOR = (120, 255, 120)
	PARSE_COLOR = (255, 110, 110)
	EDGE_COLOR = (255, 255, 255)

	# Fonts
	# (Font Face, Font Size)
	DFA_FONT = ('Consolas', 22)
	SYMBOL_FONT = ('Consolas', 19)
	INPUT_FONT = ('Consolas', 20)

	# State Parameters
	STATE_RADIUS = 40
	STATE_ACCEPTING_INNER_RADIUS = 32
	STATE_THICKNESS = 2

	# Edge Parameters
	EDGE_THICKNESS = 2
	EDGE_DEFAULT_BEND = 20
	ARROW_WIDTH = 10
	ARROW_HEIGHT = 8
	START_ARROW_LENGTH = 75
	BEND_DELTA = 10

	# Parse Parameters
	PARSE_DELAY = 0.5 # seconds

	# Controls
	KEY_EXIT = pg.K_x
	KEY_ACCEPTING = pg.K_a
	KEY_SAVE = pg.K_s
	KEY_LOAD = pg.K_d
	KEY_UNDO = pg.K_z
	KEY_SET_START = pg.K_q
	KEY_INPUT_STRING = pg.K_w
