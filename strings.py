# "Bubble Math"
#   Developed RL Vision (www.rlvision.com)
#   Source code licensed under GPLv3 (see LICENSE.txt)
#   Dev Env: Portable Python 2.7.5.1 (Python2/Windows/Pygame/PyScripter)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Strings.py
#   This module contains the localized strings.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def getStrings(language):
	""" Returns a dictionary with game strings of specified locale """
	if language == "en":
		return __langEn()
	elif language == "se":
		return __langSe()
	else:
		raise NotImplementedError


def __langEn():
	""" English strings """
	return {
		# Playfield
		"restart": 				u"Restart",
		"exit": 				u"Exit",
		"well_done_1":    	 	u"Well Done!",
		"well_done_2": 			u"You solved the",
		"well_done_3": 			u"math puzzle!",
		"game_over_1":    	 	u"No More Shots!",
		"game_over_2": 			u"Please try again...",
		"goal":					u"GOAL:",
		"operator":				u"OPERATOR:",
		"shots_left":			u"SHOTS LEFT:",
		"power":				u"POWER:",

		# Title
		"new_game": 			u"Play",
		"how_to_play": 			u"Instructions",
		"credits": 				u"A game by RL Vision. See ReadMe.txt for credit details.",
		"easy":					u"easy",
		"medium":				u"medium",
		"hard":					u"hard",

		# Help
		"help_header_1": 		u"How to play Bubble Math",
		"help_header_2": 		u"Click anywhere to return to the title screen...",
		"help_ball": 			u"This is your bubble",
		"help_aim_1": 			u"Aim with the mouse and click to",
		"help_aim_2":			u"shoot. The power meter determines",
		"help_aim_3": 			u"the strength of the shot",
		"help_bump_1": 			u"Hit the other bubbles",
		"help_bump_2": 			u"to bump them around",
		"help_main_1": 			u"There is a mathematical",
		"help_main_2": 			u"operator and goal number",
		"help_main_3": 			u"When two bubbles touch, their numbers",
		"help_main_4": 			u"are combined using the operator",
		"help_main_5": 			u"If the result match the goal number",
		"help_main_6": 			u"the two bubbles are popped",
		"help_main_7":			u"You have 10 shots to",
		"help_main_8": 			u"match all bubbles!",

		# Errors
		"error":				u"--- ERROR ---",
		"error_game_assets": 	u"Could not load playfield assets",
		"error_init": 			u"Could not initialize pygame",
		"error_game_assets": 	u"Could not load main game assets",
		"error_font_init": 		u"Could not initialize title fonts",
		"error_title_assets": 	u"Could not load title assets",
		"error_help_assets": 	u"Could not load help assets",
	}


def __langSe():
	""" Swedish strings """
	return {
		# Playfield
		"restart": 				u"Omstart",
		"exit": 				u"Avsluta",
		"well_done": 			u"Bravo!",
		"well_done_1":    	 	u"Bravo!",
		"well_done_2": 			u"Du löste",
		"well_done_3": 			u"mattepusslet!",
		"game_over_1":    	 	u"Slut På Skott!",
		"game_over_2": 			u"Försök igen...",
		"goal":					u"MÅL:",
		"operator":				u"OPERATOR:",
		"shots_left":			u"SKOTT KVAR:",
		"power":				u"KRAFT:",

		# Title
		"new_game": 			u"Spela",
		"how_to_play": 			u"Instruktioner",
		"credits": 				u"Ett spel av RL Vision. Läs ReadMe.txt för detaljer.",
		"easy":					u"lätt",
		"medium":				u"mellan",
		"hard":					u"svårt",

		# Help
		"help_header_1": 		u"Instruktioner",
		"help_header_2": 		u"Klicka med musen för att återgå till titelskärmen...",
		"help_ball": 			u"Detta är din bubbla",
		"help_aim_1": 			u"Sikta med musen och klicka för",
		"help_aim_2": 			u"att skjuta. Kraftmätaren",
		"help_aim_3": 			u"bestämmer styrkan på skottet",
		"help_bump_1":			u"Träffa bubblorna för",
		"help_bump_2": 			u"att studsa runt dem",
		"help_main_1": 			u"Det finns en slumpmässig matematisk",
		"help_main_2": 			u"operator samt ett målnummer",
		"help_main_3": 			u"När två bubblor krockar kombineras",
		"help_main_4": 			u"deras nummer med hjälp av operatorn",
		"help_main_5": 			u"Om resultatet matchar målnummret",
		"help_main_6": 			u"plockas bubblorna bort från spelplanen",
		"help_main_7": 			u"Du har 10 skott på dig",
		"help_main_8": 			u"att matcha alla bubblor!",

		# Errors
		"error": 				u"--- FEL ---",
		"error_game_assets": 	u"Kunde inte ladda spelplanens material",
		"error_init": 			u"Kunde inte starta pygame",
		"error_game_assets": 	u"Kunde inte ladda spelets huvudmaterial",
		"error_font_init": 		u"Kunde inte initialisera typsnitt",
		"error_title_assets": 	u"Kunde inte ladda titelskärmens material",
		"error_help_assets": 	"uKunde inte ladda hjälpskärmens material",
	}
