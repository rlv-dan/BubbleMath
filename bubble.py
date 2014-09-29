# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Bubble.py
#   This module contains two classes: Bubble and BubblePop. Both inherit from
#   pygame sprites. Bubble represents bubbles on the playfield, and also
#   inherit from PyParticles. When two bubbles match, they "burst" with an
#   effect displayed by a BubblePop.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import random
import math
from pygame.locals import *

# Bubble Math imports
import PyParticles
from gameflow import *


class Bubble(pygame.sprite.Sprite, PyParticles.Particle):
	""" Represents a bubble sprite in the game (both the player bubble
	    and number bubbles) """

	def __init__(self, game, startX, startY, number, is_player = False):
		self.game = game
		self.is_player = is_player
		self.x, self.y = float(startX), float(startY)   # pygame uses rects with ints to hold coordinates. x/y keep coords as floats instead since or else the movements will not be good enough...
		self.startX, self.startY = startX, startY
		self.number = number    # this is the number displayed on the bubble

		# init "popup" scaling
		if is_player:
			self.scaleCountIn = self.game.ticks * 50     # player is always last
		else:
			self.scaleCountIn = self.game.ticks * random.randint(1, 50)    # delay popup by using a negative value
		self.scaleCount = math.pi * 1.5
		self.scaleSoundPlayed = False

		# call "constructors" of parent objects
		pygame.sprite.Sprite.__init__(self)
		PyParticles.Particle.__init__(self, (startX , startY))

		# the main difference between the player and other bubbles is the image used
		if is_player:
			self.image = pygame.Surface(game.playfield.imgPlayer.get_rect().size, SRCALPHA).convert_alpha()
			self.imgSource = pygame.Surface(game.playfield.imgPlayer.get_rect().size, SRCALPHA).convert_alpha()
			self.imgSource.blit(game.playfield.imgPlayer, (0,0))      # make a copy of the bubble image cached by the playfield object
		else:
			self.imgSource = pygame.Surface(game.playfield.imgBubble.get_rect().size , SRCALPHA).convert_alpha()
			self.imgSource.blit(game.playfield.imgBubble, (0,0))      # make a copy of the bubble image cached by the playfield object

		# pygames wants a rect for sprites
		self.rect = Rect(self.imgSource.get_rect())
		self.rect.centerx, self.rect.centery = startX, startY

		# pyparticle settings
		self.size = int(self.imgSource.get_rect().width / 2)
		self.drag = FRICTION

		# pre-render bubble+number for better performance
		if not is_player:
			fontSize = 28
			if self.number >= 100: fontSize = 24
			fontObj = pygame.font.Font('freesansbold.ttf', fontSize)
			self.imgNumberText = fontObj.render(str(self.number), True, COLOR_BUBBLE_TEXT )
			self.rectNumberText = self.imgNumberText.get_rect()

			self.rectNumberText.centerx = self.imgSource.get_rect().centerx
			self.rectNumberText.centery = self.imgSource.get_rect().centery
			self.imgSource.blit(self.imgNumberText, self.rectNumberText)

		# set image
		self.image = pygame.Surface(self.imgSource.get_rect().size, SRCALPHA ).convert_alpha()


	def update(self):
		# popup animation at beginning
		if self.scaleCountIn > 0:     # count in
			self.scaleCountIn -= 4 * self.game.ticks
			if self.scaleCountIn <= 0:
				self.scaleCountIn = 0
		elif self.scaleCountIn == 0:    # scale up
			self.scaleCount += 6 * self.game.ticks
			size = int(52 * (math.sin(self.scaleCount) * 1.25 ))
			if size < 0: size = 0
			self.image = pygame.transform.smoothscale(self.imgSource, (size, size))

			if not self.scaleSoundPlayed and self.scaleCount >= math.pi*2.25:
				self.game.audio.playSound(self.game.playfield.sfxBubble)
				self.scaleSoundPlayed = True

			if(self.scaleCount >= math.pi*2.70):
				self.scaleCountIn = -1  # stop scaling
				self.image = pygame.Surface(self.imgSource.get_rect().size, SRCALPHA ).convert_alpha()
				self.image.blit(self.imgSource, (0,0))

	def draw(self):
		if self.scaleCountIn == 0:
			self.game.screen.blit(self.image, (self.rect.left + (26 - (self.image.get_rect().width/2)), self.rect.top + (26 - (self.image.get_rect().height/2)) ) )
		else:
			self.game.screen.blit(self.image, (self.rect.left, self.rect.top))


class BubblePop(pygame.sprite.Sprite):
	""" Displays an expanding, rotating ring with smaller bubbles to
	    symbolize a bursting bubble. """

	def __init__(self, game , startX , startY , number , speed , angle):
		self.game = game
		self.imgPop = game.playfield.imgPop	# image is cached in the playfield object
		self.speed = speed
		self.angle = angle
		self.startX, self.startY = startX, startY
		self.x, self.y = float(startX), float(startY)

		# these twp variables are used to draw an expanding "ring" of bubbles
		self.popCount = random.randint(0,72)
		self.popSize = 2.0

		# call the pygame sprite "costructor"
		pygame.sprite.Sprite.__init__(self)

		# pygame sprites require an image and a rect, but these are not actually used by this class since I draw the sprites myself...
		self.image = pygame.Surface((52, 52))
		self.image.fill((255, 255, 255, 0))
		self.rect = Rect(self.image.get_rect() )
		self.rect.centerx, self.rect.centery = startX, startY

	def update(self):
		# animate bubble ring
		self.popCount += 1 * self.game.ticks
		self.popSize+= 64 * self.game.ticks
		if self.popSize > 32:
			self.kill()

		# move sprite slightly to make bubble->pop look less abrutive
		self.speed *= 1000 * self.game.ticks
		self.x += math.sin(self.angle) * (15 * self.game.ticks)
		self.y += math.cos(self.angle) * (15 * self.game.ticks)

	def draw(self):
		# draws a ring of small bubbles
		for n in range(5):
			x = math.sin(math.radians(n*72) + self.popCount) * self.popSize
			y = math.cos(math.radians(n*72) + self.popCount) * self.popSize
			self.game.screen.blit(self.imgPop, (self.x + x - (self.imgPop.get_rect().width/2), self.y + y - (self.imgPop.get_rect().height/2) ) )
