# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Text.py
#   This module makes is easier to draw text in pygame, requiring only one
#   function call. The class TextObject is used internally to cache surfaces
#   with rendered text for performance.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
from pygame.locals import *

# Bubble Math imports
from gameflow import *

# Text align constants
ALIGN_CENTER = 0
ALIGN_LEFT   = 1
ALIGN_RIGHT  = 2

__textCache = {}

def clearTextCache():
	""" Frees memory by clearing the text cache """
	__textCache = {}

def drawText(surface, text, x, y, size = 28, color = (0, 0, 0), font = "freesansbold.ttf", align = ALIGN_CENTER):
	""" Draws a string onto a pygame surface i a single function call.
	    Strings are cached for better performance.
		Should not be used to draw always changing strings since
		it would use up surface memory quickly! """

	try:
		# if not found in cache, create as a TextObject and store in cache
		if not text in __textCache:
			__textCache[text + str(size) + str(color)] = TextObject(text, size, color, font)

		# recall text from cache and set alignment
		t = __textCache[text + str(size) + str(color)]
		t.rect.centery = y
		if align == ALIGN_CENTER:
			t.rect.centerx = x
		elif align == ALIGN_LEFT:
			t.rect.left = x
		elif align == ALIGN_RIGHT:
			t.rect.right = x

		# draw text onto targe surface
		surface.blit(t.image, t.rect)

	except:
		pass


class TextObject():
	""" Represents a string, pre-rendered onto a surface, ready to
	    draw with pygame """

	def __init__(self, text, size, color, font):

		try:
			fontObj = pygame.font.Font(font, int(size))
			self.image = fontObj.render(text, True, color)
			self.rect = self.image.get_rect()

		except:
			print("Error initializing text object: " + pygame.get_error())

