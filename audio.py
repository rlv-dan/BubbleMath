# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Audio.py
#   This module is a wrapper for playing pygame sfx and music, taking into
#   consideration things such as mute and already playing music
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import os
from pygame.locals import *

# Bubble Math imports
from gameflow import *


class Audio():
	""" Wrapper for playing pygame sfx and music, taking into consideration
	    things such as mute and already playing music """

	def __init__(self, game):
		self.game = game
		self.muted = False
		self.currentSong = ""

	def toggleMute(self):
		""" Mute or un-mute audio. Un-muting automatically restarts
		    the current music """
		self.muted = not self.muted
		if not self.muted and self.currentSong != "":
			self.playMusic(self.currentSong)
		else:
			pygame.mixer.music.stop()

	def playSound(self, sfx):
		""" Play sound effect, provided sound is not muted """
		if not self.muted:
			sfx.play()

	def playMusic(self, song):
		""" Load and play music file, provided sound is not muted """
		if self.currentSong == song:    # already playing this song
			return
		self.currentSong = song
		pygame.mixer.music.stop()
		if not self.muted:
			pygame.mixer.music.set_volume(0.5)
			pygame.mixer.music.load(os.path.join('mp3', song))
			pygame.mixer.music.play(-1)

	def stopMusic(self):
		""" Fade out and stop currently playing music """
		pygame.mixer.music.fadeout(750)     # 750ms is fast enough to finish before screen fade is complete
		self.currentSong = ""
