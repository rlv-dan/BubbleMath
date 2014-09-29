# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Gameflow.py
#   This module contains the Game class, which is the "glue" that ties the
#   game modules together. An instance of this class is passed to all modules
#   during the game. It contains variables and methods for running the game.
#   This module also contains constants with enumerations and global settings.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import sys
import random
from pygame.locals import *

# Bubble Math imports
import strings
import audio

# App settings
GAME_NAME 		= "Bubble Math"
SCREEN_WIDTH 	= 800
SCREEN_HEIGHT 	= 600
FPS 			= 30

# Game settings
MAX_SHOT_FORCE 	= 1200		# shot strength at max value on the power bar
POWER_BAR_SPEED = 1			# speed at which the power bar cycles
FRICTION 		= 0.975		# slowing down moving bubbles ("drag" in pyparticles)
MIN_SPEED 		= 0.4		# the bubbles stop when their speed is lower than this
SHOTS           = 10		# initial number of shots given to player

# Game modes
GM_NONE 	= 0
GM_TITLE 	= 1
GM_GAME 	= 2
GM_HELP 	= 3
GM_QUIT     = 4

# Difficulty
DIFF_EASY   = 0
DIFF_MEDIUM = 1
DIFF_HARD   = 2

# Fade modes
FADE_NONE 	= 0
FADE_IN 	= 1
FADE_OUT	= 2

# Operators
OP_PLUS		= "+"
OP_MINUS	= "-"
OP_MULTIP	= "*"
OP_DIV		= "/"

# Colors
COLOR_BLACK 			= (0,0,0)
COLOR_WHITE 			= (255,255,255)
COLOR_BUTTON_TEXT 		= (119,119,119)
COLOR_SIDEBAR_TEXT 		= (44,44,44)
COLOR_SIDEBAR_LABEL 	= (106,137,33)
COLOR_BUBBLE_TEXT 		= (255,255,255)
COLOR_BUBBLE_POP_TEXT 	= (200,200,200)
COLOR_GAME_COMPLETED 	= (77,77,77)
COLOR_HELP_TEXT 		= (77,77,77)
COLOR_HELP_HEADER 		= (240,55,55)

# additional imports (down here due to dependencies on settings above)
import bubble
import PyParticles


class GameFlow:
	""" The gameflow class contain all data needed to keep track of the game.
	    Most modules require an instance of this class being passed to
		their __init__() function """

	def __init__(self):
		self.gameMode = GM_TITLE    # start at the title screen
		self.fadeMode = FADE_IN
		self.fadeToGameMode = GM_TITLE
		self.fadeValue = 1.0
		self.fadeColor = 0

		self.screen = None	# this is the main pygame surface
		self.ticks = 0;		# used to determine how fast to move sprites so that the game runs equally fast on all computers
		self.fullscreen = False

		self.playfield = None   # will contain areference to the playfield instance
		self.rectPlayfield = Rect(128, 16, SCREEN_WIDTH - 128 - 16, SCREEN_HEIGHT - 16 - 16 )   # this is the area the bubbles can move in

		self.buttonHandler = []
		self.difficulty = DIFF_EASY
		self.audio = audio.Audio(self)  # initialize audio wrapper

		# modules can check mouse status using these
		self.mouseX = 0
		self.mouseY = 0
		self.mouseClicked = False

		# Current game setup variables
		self.gameGoal = None
		self.gameOperator = None
		self.gamePairs = None
		self.gameShots = None
		self.bubbleLeft = 0

		# Locale settings
		self.currentLanguage = "en"
		self.setLanguage(self.currentLanguage, False)
		self.delayedSetLangued = ""

		# init random number generator
		random.seed()

	def setLanguage(self, lang, delay = True):
		""" Call this function to change the game languge
		    Setting delay to True will delay the change to
		    next gamemode change """
		if delay:
			self.delayedSetLangued = lang
		else:
			self.currentLanguage = lang
			self.strings = strings.getStrings(self.currentLanguage)

	def newGame(self):
		""" Setup a new game """

		#reset game variables
		self.gameShots = SHOTS
		self.gameCompleted = False

		# pairs, starting positions and limits depends on the difficulty level
		if self.difficulty == DIFF_EASY:
			pairs = 3
			startingPositions = [             (228,86)  , (408,86)  ,
								  (100,278) ,                         (548,278) ,
								              (228,470) , (408,470) ]
		elif self.difficulty == DIFF_MEDIUM:
			pairs = 4
			startingPositions = [             (228,86)  , (408,86)  ,
								  (100,208) ,                         (548,208) ,
								  (100,348) ,                         (548,348) ,
								              (228,470) , (408,470) ]
		elif self.difficulty == DIFF_HARD:
			pairs = 5
			startingPositions = [ (145,162)  , (243,76)  , (393,76)  , (503,162) ,
								  (100,278) ,                         (548,278) ,
								  (145,394) , (243,480) , (393,480) , (503,394) ]

		# get a random operator
		self.gameOperator = random.choice((OP_PLUS , OP_MINUS))

		# get a random goal & random bubble numbers
		if self.gameOperator == OP_PLUS:
			# note: minimum lower limit is 2*pairs
			if self.difficulty == DIFF_EASY:
				lowerLimit = 2*pairs
				upperLimit = 20
			elif self.difficulty == DIFF_MEDIUM:
				lowerLimit = 2*pairs + 10
				upperLimit = 100
			elif self.difficulty == DIFF_HARD:
				lowerLimit = 2*pairs + 100
				upperLimit = 1000
			self.gameGoal = random.randint(lowerLimit,upperLimit)
			self.gamePairs = []
			while len(self.gamePairs) < pairs:
				num1 = random.randint(1, self.gameGoal-1)
				num2 = self.gameGoal - num1
				if not (num1,num2) in self.gamePairs and not (num2,num1) in self.gamePairs:
					self.gamePairs.append((num1,num2))
		elif self.gameOperator == OP_MINUS:
			# mote: minimum upper limit is 2*pairs * 2
			if self.difficulty == DIFF_EASY:
				lowerLimit = 2
				upperLimit = 2*pairs + 20
			elif self.difficulty == DIFF_MEDIUM:
				lowerLimit = 10
				upperLimit = 2*pairs + 90
			elif self.difficulty == DIFF_HARD:
				lowerLimit = 50
				upperLimit = 2*pairs + 990
			self.gameGoal = random.randint(lowerLimit, upperLimit - 2*pairs)
			self.gamePairs = []
			while len(self.gamePairs) < pairs:
				num1 = random.randint(self.gameGoal+1, upperLimit)
				num2 = num1 - self.gameGoal
				if not (num1,num2) in self.gamePairs and not (num2,num1) in self.gamePairs:
					self.gamePairs.append((num1,num2))

		# create the sprite group
		self.bubbleSprites = pygame.sprite.RenderPlain()

		# create player and add to sprite group
		self.player = bubble.Bubble(self, 318, 278, 0, True)
		self.bubbleSprites.add(self.player)

		# create bubble pairs and add to sprite group
		for n in range(len(self.gamePairs)):
			start = startingPositions[ random.randint(0, len(startingPositions)-1) ]
			startingPositions.remove(start)
			newBubble = bubble.Bubble(self, start[0], start[1], self.gamePairs[n][0])
			self.bubbleSprites.add(newBubble)
			newBubble.scaleSoundPlayed = True   # only half of the bubbles will play their popup sound so it doesn't get too crowded

			start = startingPositions[ random.randint(0, len(startingPositions)-1 ) ]
			startingPositions.remove(start)
			newBubble = bubble.Bubble(self, start[0], start[1], self.gamePairs[n][1] )
			self.bubbleSprites.add(newBubble)

		# Init PyParticles environment
		self.particleEnvironment = PyParticles.Environment((self.rectPlayfield.width, self.rectPlayfield.height))
		self.particleEnvironment.addBubbles(self.bubbleSprites)

	def fadeTo(self, destGameMode, stopMusic = True):
		""" Use this function to change game mode """
		if self.fadeMode == FADE_NONE:
			self.fadeMode = FADE_OUT
			self.fadeToGameMode = destGameMode
			self.fadeValue = 0
			if stopMusic:
				self.audio.stopMusic()
			if destGameMode == GM_QUIT:
				self.fadeColor = 0      # when quitting, fade to black

	def fatalError(self, msg):
		""" In case of critical errors, this function is called to gracefully
		    shut down the application and print an error message """
		print(self.strings["error"])
		print(msg + ": " + pygame.get_error())
		pygame.quit()
		sys.exit()

