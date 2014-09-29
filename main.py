# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Main.py
#   This modules is the starting point for the game. Assets are loaded and the
#   pygame main loop is started. It handles events, calls the update & draw
#   methods and manages game mode changes.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import sys
import os
from pygame.locals import *

# Bubble Math imports
import title
import playfield
import help
import text
import util
from gameflow import *


def main():
	""" Initialize pygame and start main game loop """

	game = GameFlow()   # create an instance of the gameflow class

	# Initialize pygame & setup screen
	try:
		os.environ['SDL_VIDEO_CENTERED'] = '1' # center window at startup
		pygame.mixer.pre_init(44100, -16, 1, 512) # initializing sound before pygame.init() solves problems with lagging sound!
		pygame.init() #initialize pygame
		game.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF)    # optional flag: FULLSCREEN
		fadeSurface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha() # fadeSurface is blitted on top of everything else to provide a nice fade effect between game modes
		pygame.display.set_icon(pygame.image.load(os.path.join('gfx', 'icon.png')))     # Note: The icon looks horrible - icons do not seem to work properly in pygame (my computer only?)
	except:
		game.fatalError(self.game.strings["error_init"])

	pygame.display.set_caption(GAME_NAME )
	fpsClock = pygame.time.Clock()

	# Start with title screen
	gameTitle = title.Title(game)
	game.audio.playMusic("InSpira_-_Follow_the_Waves.mp3")

	# Main game loop
	while 1:

		# Wait for next frame
		game.ticks = float(fpsClock.tick(FPS)) / 1000

		# Handle events
		game.mouseClicked = False
		for event in pygame.event.get():
			if event.type == QUIT:
				game.fadeTo(GM_QUIT)
			elif event.type == KEYUP and event.key == K_ESCAPE:		# ESC: Back to title screen or quit game on title screen
				if game.gameMode == GM_TITLE:
					game.fadeTo(GM_QUIT)
				else:
					game.fadeTo(GM_TITLE)
			elif event.type == KEYUP and event.key == K_F11:		# F11: Toggle fullscreen (does not work on my computer)
					game.fullscreen = not game.fullscreen
					game.screen = util.toggle_fullscreen()
			elif event.type == MOUSEMOTION:
				game.mouseX, game.mouseY = event.pos	# cache mouse events in game instance for other modules to query
			elif event.type == MOUSEBUTTONUP:
				game.mouseX, game.mouseY = event.pos	# -"-
				game.mouseClicked = True

		# Update game state
		if game.gameMode == GM_TITLE:
			gameTitle.update()
		elif game.gameMode == GM_HELP:
			gameHelp.update()
		elif game.gameMode == GM_GAME:
			game.playfield.update()

		# Update buttons
		for but in game.buttonHandler:
			but.update()

		# Update fade overlay
		if game.fadeMode == FADE_IN:
			game.fadeValue -= 1.75 * game.ticks
			if game.fadeValue <= 0:
				game.fadeValue = 0
				game.fadeMode = FADE_NONE
				game.fadeColor = 255		# game starts from black and fades to titlescreen, but then we want all fades to be to/from white (this line)
		elif game.fadeMode == FADE_OUT:
			game.fadeValue += 1.75 * game.ticks
			if game.fadeValue >= 1:
				# fade is complete -> change game mode!
				game.fadeValue = 1
				game.fadeMode = FADE_IN
				game.gameMode = game.fadeToGameMode
				text.clearTextCache()
				game.buttonHandler = [] # clear buttons
				if game.delayedSetLangued != "": # language change waiting
					game.setLanguage(game.delayedSetLangued, False )
				# initialize new game mode objects
				if game.gameMode == GM_TITLE:
					gameTitle = title.Title(game)
					game.audio.playMusic("InSpira_-_Follow_the_Waves.mp3")
				elif game.gameMode == GM_HELP:
					gameHelp = help.Help(game)
					game.audio.playMusic("InSpira_-_Follow_the_Waves.mp3")
				elif game.gameMode == GM_GAME:
					game.playfield = playfield.Playfield(game)
					game.newGame()
					game.audio.playMusic("InSpira_-_BEACH_GROOVE.mp3")
				elif game.gameMode == GM_QUIT:
					pygame.quit()
					sys.exit()

		# Draw screen
		if game.gameMode == GM_TITLE:
			gameTitle.draw()
			pass
		elif game.gameMode == GM_HELP:
			gameHelp.draw()
		elif game.gameMode == GM_GAME:
			game.playfield.draw()

		# Draw buttons
		for but in game.buttonHandler:
			but.draw()

		# Draw fade overlay if needed
		if game.fadeMode == FADE_IN or game.fadeMode == FADE_OUT:
			fadeSurface.fill((game.fadeColor, game.fadeColor, game.fadeColor, 255 * game.fadeValue))
			game.screen.blit(fadeSurface, (0, 0))

		# Update display
		pygame.display.flip()


# Launch the game
if __name__ == "__main__":
	main()
