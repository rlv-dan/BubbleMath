# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Playfield.py
#   This module controls the game board, bubbles & player
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import os
import math
from pygame.locals import *

# Bubble Math imports
import bubble
import util
import PyParticles
import text
import button
from gameflow import *


class Playfield:
	""" This class controls the "actual" game (board, bubbles, player, game logic etc) """

	def __init__(self, game ):
		self.game = game
		self.bubblePopSprites =  pygame.sprite.RenderPlain()

		# load game assets
		try:
			# images
			self.imgBackground = pygame.image.load( os.path.join('gfx', 'playfield.png') ).convert()
			self.imgPlayerAim = pygame.image.load( os.path.join('gfx', 'player_aim.png') ).convert_alpha()
			self.imgGameCompleted = pygame.image.load( os.path.join('gfx', 'completed.png') )
			self.imgGameOver = pygame.image.load( os.path.join('gfx', 'completed.png') )
			self.imgPowerBar = pygame.image.load( os.path.join('gfx', 'power_bar.png') ).convert_alpha()
			self.imgButtons = pygame.image.load( os.path.join('gfx', 'buttons.png') ).convert_alpha()

			# bubble assets are store in the playfield so each bubble does not have to load it separately
			self.imgPop = pygame.image.load( os.path.join('gfx', 'bubble16.png') ).convert_alpha()
			self.imgPlayer = pygame.image.load( os.path.join('gfx', 'player52.png') ).convert_alpha()
			self.imgBubble = pygame.image.load( os.path.join('gfx', 'bubble52.png') ).convert_alpha()

			# sound fx
			self.sfxPop = pygame.mixer.Sound( os.path.join('sfx', 'pop.ogg') )
			self.sfxBounce = pygame.mixer.Sound( os.path.join('sfx', 'ball.ogg') )
			self.sfxWallBounce = pygame.mixer.Sound( os.path.join('sfx', 'wall.ogg') )
			self.sfxComplete = pygame.mixer.Sound( os.path.join('sfx', 'complete.ogg') )
			self.sfxShoot = pygame.mixer.Sound( os.path.join('sfx', 'shoot.ogg') )
			self.sfxClick = pygame.mixer.Sound( os.path.join('sfx', 'click.ogg') )
			self.sfxBubble = pygame.mixer.Sound( os.path.join('sfx', 'bubble.ogg') )
			self.sfxGameOver = pygame.mixer.Sound( os.path.join('sfx', 'gameover.ogg') )

		except:
			self.game.fatalError(self.game.strings["error_game_assets"])

		# init power bar
		self.powerCounter = 0
		self.powerIncrement = POWER_BAR_SPEED
		self.rectPower = Rect(0 , 0 , 0 , 23)

		# pre-render game over & game completed popups
		text.drawText( self.imgGameCompleted, self.game.strings["well_done_1"],  self.imgGameCompleted.get_rect().centerx , 32  , 24 , COLOR_BLACK , 'freesansbold.ttf' , text.ALIGN_CENTER )
		text.drawText( self.imgGameCompleted, self.game.strings["well_done_2"],  self.imgGameCompleted.get_rect().centerx , 64  , 16 , COLOR_GAME_COMPLETED , 'freesansbold.ttf' , text.ALIGN_CENTER )
		text.drawText( self.imgGameCompleted, self.game.strings["well_done_3"],  self.imgGameCompleted.get_rect().centerx , 84  , 16 , COLOR_GAME_COMPLETED , 'freesansbold.ttf' , text.ALIGN_CENTER )

		text.drawText( self.imgGameOver, self.game.strings["game_over_1"],  self.imgGameOver.get_rect().centerx , 38 , 24 , COLOR_BLACK , 'freesansbold.ttf' , text.ALIGN_CENTER )
		text.drawText( self.imgGameOver, self.game.strings["game_over_2"],  self.imgGameOver.get_rect().centerx , 72 , 16 , COLOR_GAME_COMPLETED , 'freesansbold.ttf' , text.ALIGN_CENTER )

		self.gameCompletedRect = Rect(0, 0, SCREEN_WIDTH, 0 )   # this is used to animate ("popup") the game completed of game over box

		# setup restart button
		self.rectButtonRestart = Rect(9, 513, 102, 33)
		btn = button.Button(self.game, self.rectButtonRestart.topleft, self.imgButtons, Rect(0, 352, 102, 33), Rect(112, 352, 102, 33), self.btnRestart_Click, self.sfxClick )
		btn.setText(self.game.strings["restart"] ,  15 , COLOR_BUTTON_TEXT , 'freesansbold.ttf' )
		btn.setTextPosition(text.ALIGN_LEFT, 29, 2)
		self.game.buttonHandler.append(btn)

		# setup exit button
		self.rectButtonExit = Rect(9, 553, 102, 33)
		btn = button.Button(self.game, self.rectButtonExit.topleft, self.imgButtons, Rect(0, 400, 102, 33), Rect(112, 400, 102, 33), self.btnExit_Click, self.sfxClick )
		btn.setText(self.game.strings["exit"],  15, COLOR_BUTTON_TEXT, 'freesansbold.ttf' )
		btn.setTextPosition(text.ALIGN_LEFT, 29, 2)
		self.game.buttonHandler.append(btn)


	# Button click handlers
	def btnRestart_Click(self, btn):
		self.game.fadeTo(GM_GAME,False)

	def btnExit_Click(self, btn):
		self.game.fadeTo(GM_TITLE)


	def update(self):
		# Update physics and move bubbles
		collisions = self.game.particleEnvironment.update()
		for spr in self.game.bubbleSprites:  # update bubble rects (contains the visual position of the bubble)
			spr.rect.centerx = spr.x + self.game.rectPlayfield.left
			spr.rect.centery = spr.y + self.game.rectPlayfield.top
		match = False
		for col in collisions:  # if there were collision, check to see if any mathematical matches occurred
			if col[0] != None and col[1] != None:
				match = self.matchBubbles(col[0], col[1])
		if match == False:
			if len(collisions) > 0:     # play sound if there were collisions
				if (None,None) in collisions:    # indicates a wall bounce
					self.game.audio.playSound(self.sfxWallBounce)
				else:
					self.game.audio.playSound(self.sfxBounce)

		# update bubbles
		for bub in self.game.bubbleSprites: bub.update()

        # wait for bubble popups to finish before game starts
		if self.game.player.scaleCountIn != -1:
			return

		# update power bar moving back and forth
		if self.game.player.speed == 0 and not self.game.gameCompleted:
			self.powerCounter += self.powerIncrement * self.game.ticks
			if self.powerCounter >= 1.1:
				self.powerCounter = 1.1
				self.powerIncrement = -self.powerIncrement
			elif self.powerCounter <= 0.0:
				self.powerCounter = 0.0
				self.powerIncrement = -self.powerIncrement
			self.rectPower.width = (int(90 * max(min(self.powerCounter, 1.0), 0.1)) / 8) * 8      # drawing width of power bar.

		# handle mouse events
		if self.game.mouseClicked:
            # skip clicks on button areas
			if self.rectButtonRestart.collidepoint(self.game.mouseX, self.game.mouseY) or self.rectButtonExit.collidepoint(self.game.mouseX, self.game.mouseY):
				pass
			# shoot the ball
			elif self.game.player.speed == 0 and not self.game.gameCompleted:
				self.game.gameShots -= 1
				if self.game.gameShots == 0:
					self.game.gameCompleted = True
				self.game.player.speed = max(min(self.powerCounter, 1.0), 0.1) * MAX_SHOT_FORCE * self.game.ticks
				self.game.player.angle = util.getAngle(self.game.player.rect.centerx, self.game.mouseY, self.game.mouseX ,self.game.player.rect.centery)
				self.game.audio.playSound(self.sfxShoot)

		# update bubble pop sprites
		for pop in self.bubblePopSprites:
			pop.update()

		# animate game completed overlay window
		if self.game.gameCompleted and self.game.player.speed < 2:
			if self.game.mouseClicked:
				self.game.fadeTo(GM_GAME,False)
			if self.gameCompletedRect.height == 0:  # play game completed sound only once
				if self.game.gameShots == 0 and self.game.bubblesLeft > 1:
					self.game.audio.playSound(self.sfxGameOver )
				else:
					self.game.audio.playSound(self.sfxComplete )
			self.gameCompletedRect.height += 350 * self.game.ticks



	def matchBubbles(self, b1, b2):
		""" Test if two bubbles match (and if so remove them from
		    playfield and PyParticle environment) """
		if b1 == self.game.player or b2 == self.game.player:    # no need to test player sprite
			return False
		match = False
		if self.game.gameOperator == OP_PLUS:
			if b1.number + b2.number == self.game.gameGoal: match = True
		elif self.game.gameOperator == OP_MINUS:
			if b1.number - b2.number == self.game.gameGoal: match = True
			elif b2.number - b1.number == self.game.gameGoal: match = True
		elif self.game.gameOperator == OP_MULTIP:
			if b1.number * b2.number == self.game.gameGoal: match = True
		elif self.game.gameOperator == OP_DIV:
			if b1.number / b2.number == self.game.gameGoal: match = True
			elif b2.number / b1.number == self.game.gameGoal: match = True

		if match:
			self.game.bubblesLeft = self.game.particleEnvironment.delBubbles((b1, b2))
			self.bubblePopSprites.add((bubble.BubblePop(self.game, b1.rect.centerx, b1.rect.centery, b1.number , b1.speed, b1.angle ) , bubble.BubblePop( self.game, b2.rect.centerx, b2.rect.centery, b2.number, b2.speed, b2.angle )))
			b1.kill()
			b2.kill()
			self.game.audio.playSound(self.sfxPop)
			if self.game.bubblesLeft == 1:    # test for game complete (only one bubble left => only player left )
				self.game.gameCompleted = True

		return match

	def draw(self):
		# draw backdrop
		self.game.screen.blit(self.imgBackground, (0, 0))

		# draw sprites
		for bub in self.game.bubbleSprites: bub.draw()
		for pop in self.bubblePopSprites: pop.draw()

		# draw player aim
		if self.game.player.speed == 0 and not self.game.gameCompleted and self.game.player.scaleCountIn == -1:
			for n in range(2,8):
				sin = math.sin( util.getAngle( self.game.player.rect.centerx , self.game.player.rect.centery , self.game.mouseX , self.game.mouseY ) )
				cos = math.cos( util.getAngle( self.game.player.rect.centerx , self.game.player.rect.centery , self.game.mouseX , self.game.mouseY ) )
				y = math.ceil( self.game.player.rect.centery + cos*(n*10 + 15) - 4 )
				x = math.ceil( self.game.player.rect.centerx + sin*(n*10 + 15) - 3 )
				self.game.screen.blit(self.imgPlayerAim, (x, y))

		# draw sidebar
		text.drawText(self.game.screen, str(self.game.gameGoal),  98, 155, 20, COLOR_SIDEBAR_TEXT , 'freesansbold.ttf', text.ALIGN_RIGHT)
		text.drawText(self.game.screen, self.game.gameOperator,  98, 217, 26, COLOR_SIDEBAR_TEXT, 'freesansbold.ttf' , text.ALIGN_RIGHT)
		text.drawText(self.game.screen, str(self.game.gameShots),  98, 283, 20, COLOR_SIDEBAR_TEXT, 'freesansbold.ttf' , text.ALIGN_RIGHT)
		self.game.screen.blit(self.imgPowerBar, (18, 322), self.rectPower)

		# draw sidebar text (drawing each text twice gives a nice bold look)
		for n in range(2): text.drawText(self.game.screen, self.game.strings["goal"], 16, 128, 11, COLOR_SIDEBAR_LABEL, 'freesansbold.ttf', text.ALIGN_LEFT)
		for n in range(2): text.drawText(self.game.screen, self.game.strings["operator"], 15, 192, 11, COLOR_SIDEBAR_LABEL, 'freesansbold.ttf', text.ALIGN_LEFT)
		for n in range(2): text.drawText(self.game.screen, self.game.strings["shots_left"], 16, 256, 11 , COLOR_SIDEBAR_LABEL, 'freesansbold.ttf', text.ALIGN_LEFT)
		for n in range(2): text.drawText(self.game.screen, self.game.strings["power"], 16, 320, 11, COLOR_SIDEBAR_LABEL, 'freesansbold.ttf', text.ALIGN_LEFT)

		# draw game completed overlay window
		if self.game.gameCompleted and self.game.player.speed < 2:
			if self.game.gameShots == 0 and self.game.bubblesLeft > 1:
				self.game.screen.blit(self.imgGameOver, (self.game.rectPlayfield.x + (self.game.rectPlayfield.height/2) -(self.imgGameOver.get_rect().width/2) , self.game.rectPlayfield.y + (self.game.rectPlayfield.height/2) - (self.imgGameOver.get_rect().height/2) ), self.gameCompletedRect)
			else:
				self.game.screen.blit(self.imgGameCompleted, (self.game.rectPlayfield.x + (self.game.rectPlayfield.height/2) -(self.imgGameCompleted.get_rect().width/2) , self.game.rectPlayfield.y + (self.game.rectPlayfield.height/2) - (self.imgGameCompleted.get_rect().height/2) ), self.gameCompletedRect)
