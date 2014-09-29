# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Button.py
#   Represents a button with built in functionality for drawing itself and
#   managing mouse hover and clicks.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pygame.locals import *

# Bubble Math imports
import text
from gameflow import *


class Button():
	""" Represents a button with built in functionality for drawing itself and
	    managing mouse hover and clicks. An alternative source image rect can
		be set for toggle buttons. Text label is optional. """

	def __init__(self, game, destPos, sourceImage, sourceRectNormal, sourceRectHover, clickFunc, clickSound = None):
		self.game = game

		self.sourceRectNormal = sourceRectNormal    # rect pointing to the normal button image
		self.sourceRectHover = sourceRectHover      # rect pointing to the image to draw when mouse is hovering the button
		self.sourceRect = sourceRectNormal

		self.sourceImage = sourceImage      		# pygame surface containing the images
		self.destRect = Rect(destPos, (sourceRectNormal.width, sourceRectNormal.height))        # destination where to draw the button

		self.clickFunc = clickFunc                  # function to call when button is clicked
		self.clickSound = clickSound                # optional sound to play when button is clicked

		self.textString = ""                        # buttons do not have text initially -> call setText() to add text
		self.sourceAltRectNormal = None
		self.sourceAltRectHover = None

	def setText(self, label, size = 28, color = (0, 0, 0), font = "freesansbold.ttf"):
		""" Call this function to add text to a button.
		    Buttons do not have text initially. """
		self.textString = label
		self.textSize = size
		self.textColor = color
		self.textFont = font
		self.textOffsetX = 0
		self.textOffsetY = 0
		self.textAlign = text.ALIGN_CENTER

	def setTextPosition(self, align, offsetX = 0, offsetY = 0):
		""" By default button text is center aligned. Use this
		    function to tweak the text position """
		self.textAlign = align
		self.textOffsetX = offsetX
		self.textOffsetY = offsetY

	def setAlternativeSourceImage(self, sourceAltRectNormal, sourceAltRectHover):
		""" Load an alternative button image, then use toggleSourceImage() to
		    change currently displayed image. """
		self.sourceAltRectNormal = sourceAltRectNormal
		self.sourceAltRectHover = sourceAltRectHover

	def toggleSourceImage(self):
		""" Buttons that toggle between two states call this function. (Don't
		    forget to define an alternative image first.) """
		if self.sourceAltRectNormal == None or self.sourceAltRectHover == None:
			return
		# flip the currently displayed image and alternative one
		tmp1 = self.sourceRectNormal
		tmp2 = self.sourceRectHover
		self.sourceRectNormal = self.sourceAltRectNormal
		self.sourceRectHover = self.sourceAltRectHover
		self.sourceAltRectNormal = tmp1
		self.sourceAltRectHover = tmp2

	def update(self):
		# change image if mouse is over button + test for clicks
		if self.destRect.collidepoint(self.game.mouseX, self.game.mouseY):
			self.sourceRect = self.sourceRectHover  # change to "hover" image
			if self.game.mouseClicked:
				if self.clickFunc != None: # call click callback function (if any)
					self.clickFunc(self)
				if self.clickSound != None: # play the button click sound (if any)
					self.game.audio.playSound(self.clickSound)
		else:
			self.sourceRect = self.sourceRectNormal # change back to "normal" (non-hover) image


	def draw(self):
		self.game.screen.blit(self.sourceImage, self.destRect, self.sourceRect)
		if self.textString != "":
			x = self.destRect.centerx
			if self.textAlign == text.ALIGN_LEFT: x = self.destRect.left
			if self.textAlign == text.ALIGN_RIGHT: x = self.destRect.right
			text.drawText(self.game.screen, self.textString, x + self.textOffsetX, self.destRect.centery + self.textOffsetY, self.textSize, self.textColor, self.textFont, self.textAlign)

