# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Help.py
#   This module displays the help screen.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import os

import text
from pygame.locals import *
from gameflow import *


class Help:
	""" Displays the help screen """

	def __init__(self, game):
		self.game = game

		# Load assets
		try:
			self.imgHelpBG = pygame.image.load( os.path.join('gfx', 'help.png') ).convert()
			self.soundButtonClick = pygame.mixer.Sound( os.path.join('sfx', 'click.ogg') )
		except:
			self.game.fatalError( self.game.strings["error_help_assets"] )

	def update(self):
        # check mouse click event
		if self.game.mouseClicked:
			self.game.audio.playSound(self.soundButtonClick)
			self.game.fadeTo(GM_TITLE,False)  # go back to title screen

	def draw(self):
		# draw backdrop
		self.game.screen.blit(self.imgHelpBG, (0, 0))

		# draw headers
		text.drawText(self.game.screen, self.game.strings["help_header_1"], SCREEN_WIDTH / 2, 32, 28, COLOR_HELP_HEADER, 'freesansbold.ttf', text.ALIGN_CENTER)
		text.drawText(self.game.screen, self.game.strings["help_header_2"], SCREEN_WIDTH / 2, 64, 14, COLOR_HELP_HEADER, 'freesansbold.ttf', text.ALIGN_CENTER)

		# draw the help texts
		y = 200
		text.drawText(self.game.screen, self.game.strings["help_ball"]  , 120, y   , 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_CENTER)
		text.drawText(self.game.screen, self.game.strings["help_aim_1"] , 390, y   , 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_CENTER)
		text.drawText(self.game.screen, self.game.strings["help_aim_2"] , 390, y+20, 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_CENTER)
		text.drawText(self.game.screen, self.game.strings["help_aim_3"] , 390, y+40, 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_CENTER)
		text.drawText(self.game.screen, self.game.strings["help_bump_1"], 650, y   , 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_CENTER)
		text.drawText(self.game.screen, self.game.strings["help_bump_2"], 650, y+20, 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_CENTER)
		x, y = 400, 350
		text.drawText(self.game.screen, self.game.strings["help_main_1"], x, y      , 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
		text.drawText(self.game.screen, self.game.strings["help_main_2"], x, y + 20 , 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
		text.drawText(self.game.screen, self.game.strings["help_main_3"], x, y + 60 , 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
		text.drawText(self.game.screen, self.game.strings["help_main_4"], x, y + 80 , 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
		text.drawText(self.game.screen, self.game.strings["help_main_5"], x, y + 120, 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
		text.drawText(self.game.screen, self.game.strings["help_main_6"], x, y + 140, 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
		text.drawText(self.game.screen, self.game.strings["help_main_7"], x, y + 180, 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
		text.drawText(self.game.screen, self.game.strings["help_main_8"], x, y + 200, 15, COLOR_HELP_TEXT, 'freesansbold.ttf', text.ALIGN_LEFT)
