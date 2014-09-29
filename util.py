# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Util.py
#   This module houses general helper functions not specifically related to
#   other modules or classes.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import math
import pygame
from pygame.locals import *


def getDistance(x1, y1, x2, y2):
	""" Returns the distance between two points """
	dx = x1 - x2
	dy = y1 - y2
	return math.sqrt(dx * dx + dy * dy)

def getAngle(x1, y1, x2, y2):
	""" Returns the angle in radians between two points """
	dist = getDistance(x1, y1, x2, y2)
	if dist > 0:
		nx = float(x2 - x1) / dist
		ny = float(y2 - y1) / dist
		return math.atan2(nx, ny)
	else:
		return 0

def toggle_fullscreen():
	""" Helps switching between fullscreen and windowed mode. Needed since
		pygame.display.toggle_fullscreen() apparently only works on unix
		x11 driver.
		Source: http://www.pygame.org/wiki/toggle_fullscreen
		"""
	screen = pygame.display.get_surface()
	tmp = screen.convert()
	caption = pygame.display.get_caption()
	cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

	w,h = screen.get_width(),screen.get_height()
	flags = screen.get_flags()
	bits = screen.get_bitsize()

	pygame.display.quit()
	pygame.display.init()

	screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
	screen.blit(tmp,(0,0))
	pygame.display.set_caption(*caption)

	pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

	pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007

	return screen
