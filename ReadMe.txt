
--- Bubble Math ---------------------------------------------------------------------

Bubble Math is an edutainment game with mechanics similar to billiards/pool. 
You shoot your bubble around, knocking other bubbles trying to get them to hit 
each other so that their numbers together equal the specified goal.

Developed by RL Vision (c) 2013-2014 (www.rlvision.com)

License:
  Bubble Math is free, open source software.
  Source code licensed under GPLv3 (see LICENSE.txt).
  Source code available at GitHub (github.com/rlv-dan/BubbleMath)
  Game assets may be covered by other license (see credits below).

The game was conveived as part of a Python course I took. It received top grade. The 
source code is well structured and contains lots of comments, and might be suitable 
for learning how to make a game using Python and PyGame.


--- Starting the Game ---------------------------------------------------------------

Windows users:
  Start the game by double clicking on the exe file. The game has been tested to 
  work on Windows XP and Windows 7.
  
  Note: If the game does not start, asking for "MSVCR90.dll", you probably need 
  to install the "Microsoft Visual C++ 2008 Redistributable Package":
  (www.microsoft.com/en-us/download/details.aspx?id=29)
  
Other operating systems: 
  The game is built with Python 2. All system that can run Python 2 applications 
  should be able to run the game. All source code is included in the src folder. 
  Note that the data folders (gfx, sfx and mp3) must be in the same folder and 
  the source code, so you should copy these to the src folder first.


--- How to Play ---------------------------------------------------------------------

At the title screen, click the 'Instructions' button to learn how to play the game.


--- Difficulty ----------------------------------------------------------------------

There are three difficuly levels to choose from, with the following 
characteristics:

        |  Bubbles  |  Number Range  |
 -------|-----------|----------------|
 Easy   |        6  |          2-20  |
 Medium |        8  |        10-100  |
 Hard   |       10  |      100-1000  |

The mathematical operator (plus or minus) is randomly chosen for each game.


--- Bubble Math Credits -------------------------------------------------------------

Designed and programmed by Dan Saedén

Some graphics based on "PuzzleGraphics" by Kenney Vleugels (www.kenney.nl)

PyParticles module by Peter Collingridge (www.petercollingridge.co.uk/pygame-physics-simulation)

Music by InSpira (www.jamendo.com/en/artist/350698/inspira) (CC BY-NC-ND 3.0)

Made with Python 2 (www.python.org)

Game engine by Pygame (www.pygame.org)

Window Exe created with py2exe (www.py2exe.org)

Sound effects:
	ball.ogg: from Ballsmacker (ballsmacker.sourceforge.net) (GPL2)
	bubble.ogg: by Glaneur de sons (www.freesound.org/people/Glaneur%20de%20sons) (CC BY-NC 3.0)
	click.ogg: from NeverBall (www.neverball.org) (GPL2)
	gameover.ogg, complete.ogg: from Secret Maryo Chronicles (www.secretmaryo.org) (GPL3)
	wall.ogg: by WormNut (www.flashkit.com/soundfx/Interfaces/Thwacks/Footstep-WormNut-8072/index.php) (Freeware)
