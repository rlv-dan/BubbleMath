# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Title.py
#   This module displays the title screen.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import os
from pygame.locals import *

# Bubble Math imports
import text
import button
import util
from gameflow import *


class Title:
	""" Displays the title screen """

	def __init__(self, game ):

		self.game = game

		# load assets
		try:
			self.imgTitleBG = pygame.image.load( os.path.join('gfx', 'title.png') ).convert()
			self.imgButtons = pygame.image.load( os.path.join('gfx', 'buttons.png') ).convert_alpha()
			self.sfxClick = pygame.mixer.Sound( os.path.join('sfx', 'click.ogg') )
		except:
			self.game.fatalError(self.game.strings["error_title_assets"])

		# setup button rectangles
		self.rectButton1Area = Rect(196 , 419 , 190 , 49)
		self.rectButton2Area = Rect(420 , 419 , 190 , 49)

        # setup exit button
		self.game.buttonHandler.append(button.Button(self.game, (10, 10), self.imgButtons, Rect(0, 0, 26, 26), Rect(32, 0, 26, 26), self.btnExit_Click, self.sfxClick ))

        # setup mute button
		btn = button.Button(self.game, (SCREEN_WIDTH-80 , 11), self.imgButtons, Rect(0, 32, 31, 23), Rect(32, 32, 31, 23), self.btnSound_Click, self.sfxClick)
		btn.setAlternativeSourceImage(Rect(0, 64, 31, 23), Rect(32, 64, 31, 23))
		if self.game.audio.muted: btn.toggleSourceImage()
		self.game.buttonHandler.append(btn)

        # setup fullscreen button
		btn = button.Button(self.game, (SCREEN_WIDTH-35 , 10), self.imgButtons, Rect(0, 96, 25, 25), Rect(32, 96, 25, 25), self.btnFullscreen_Click, self.sfxClick)
		btn.setAlternativeSourceImage(Rect(0, 128, 25, 25), Rect(32, 128, 25, 25))
		if self.game.fullscreen: btn.toggleSourceImage()
		self.game.buttonHandler.append(btn)

		# setup flag buttons
		self.game.buttonHandler.append(button.Button(self.game, (SCREEN_WIDTH-65, SCREEN_HEIGHT-70 ) , self.imgButtons , Rect(0, 160, 24, 18), Rect(32, 160, 24, 18), self.btnEnglish_Click, self.sfxClick )) 	# english
		self.game.buttonHandler.append(button.Button(self.game, (SCREEN_WIDTH-35, SCREEN_HEIGHT-70 ) , self.imgButtons , Rect(0, 192, 24, 18), Rect(32, 192, 24, 18), self.btnSwedish_Click, self.sfxClick ))  	# swedish

		# setup start button
		btn = button.Button(self.game, (SCREEN_WIDTH/2 -95 ,370), self.imgButtons, Rect(0, 224, 191, 49), Rect(0, 288, 191, 49), self.btnStart_Click, self.sfxClick)
		btn.setText(self.game.strings["new_game"], 16, COLOR_BUTTON_TEXT, 'freesansbold.ttf' )
		self.game.buttonHandler.append(btn)

		# setup help button
		btn = button.Button(self.game, (SCREEN_WIDTH/2 -95 ,435), self.imgButtons, Rect(0, 224, 191, 49), Rect(0, 288, 191, 49), self.btnHelp_Click, self.sfxClick)
		btn.setText(self.game.strings["how_to_play"] , 16 , COLOR_BUTTON_TEXT , 'freesansbold.ttf' )
		self.game.buttonHandler.append(btn)

		# setup difficulty button
		btn = button.Button(self.game, (SCREEN_WIDTH/2 -60 , 500), self.imgButtons, Rect(0, 448, 120, 33), Rect(136, 448, 120, 33), self.btnDifficulty_Click, self.sfxClick)
		txt = self.game.strings["easy"]
		if self.game.difficulty == DIFF_MEDIUM: txt = self.game.strings["medium"]
		if self.game.difficulty == DIFF_HARD: txt = self.game.strings["hard"]
		btn.setText(txt, 14, COLOR_BUTTON_TEXT, 'freesansbold.ttf')
		btn.setTextPosition(text.ALIGN_CENTER, 0, -1)
		self.game.buttonHandler.append(btn)


	# Button click handlers

	def btnStart_Click(self, btn):
		self.game.fadeTo(GM_GAME)

	def btnHelp_Click(self, btn):
		self.game.fadeTo(GM_HELP,False)

	def btnDifficulty_Click(self, btn):
		if self.game.difficulty == DIFF_EASY: self.game.difficulty = DIFF_MEDIUM
		elif self.game.difficulty == DIFF_MEDIUM: self.game.difficulty = DIFF_HARD
		elif self.game.difficulty == DIFF_HARD: self.game.difficulty = DIFF_EASY

		txt = self.game.strings["easy"]
		if self.game.difficulty == DIFF_MEDIUM: txt = self.game.strings["medium"]
		if self.game.difficulty == DIFF_HARD: txt = self.game.strings["hard"]
		btn.setText(txt, 14, COLOR_BUTTON_TEXT, 'freesansbold.ttf')
		btn.setTextPosition(text.ALIGN_CENTER, 0, -1)

	def btnExit_Click(self, btn):
		self.game.fadeTo(GM_QUIT)

	def btnFullscreen_Click(self, btn):
		self.game.screen = util.toggle_fullscreen()
		self.game.fullscreen = not self.game.fullscreen
		btn.toggleSourceImage()

	def btnSound_Click(self, btn):
		self.game.audio.toggleMute()
		btn.toggleSourceImage()

	def btnEnglish_Click(self, btn):
		self.game.fadeTo(GM_TITLE,False)
		self.game.setLanguage("en")

	def btnSwedish_Click(self, btn):
		self.game.fadeTo(GM_TITLE,False)
		self.game.setLanguage("se")


	def update(self):
		pass

	def draw(self):
		# draw backdrop & credits text at bottom
		self.game.screen.blit(self.imgTitleBG, (0, 0))
		text.drawText(self.game.screen, self.game.strings["credits"], SCREEN_WIDTH / 2, SCREEN_HEIGHT - 16, 13, (11, 85, 114), 'freesansbold.ttf', text.ALIGN_CENTER)
