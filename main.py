# First things first: get a basic loop running again.
# rewrite functions from Scrabble Solver.py into cleaner ones.

# contains the main game-loop with applied settings

# import general modules
# from random import randint
# import re
# import shelve
# from copy import deepcopy
# from sys import path as OSP

# DEBUG: insert working directory in path to access the Scrabble-specific files
# TODO: work out proper path

# DEBUG:
import pprint

# import settings as S
# import checks as C
# import logic as L
# import display as D
# import logging as ScrabbleLogging

from logic_new import Datatypes
from logic_new import Settings
from logic_new import Checks
from logic_new import Logic
from logic_new import Display
from logic_new import WordSearch
from logic_new import WordLog

# DEBUG:
import unit_tests as UT

# ***GLOBALS***
LANGUAGE = "german"
# lang = "english"
GAMEMODE = "normal"

# dirty solution.
gameSettings = Settings.get_game_settings(GAMEMODE, LANGUAGE)
Settings.set_game_settings(settings=gameSettings)

# Pseudo Unit-Testing/Sanity-Checks:
UT.basics()


# Words5LettersWithE = gameSettings['words'][5]['E']
# Words5LettersWithB = gameSettings['words'][5]['B']


# samplePlayA = WordSearch.createPlay("BEISPIEL",
#                                    "A1",
#                                    "x")
# samplePlayB = WordSearch.createPlay("ABLAUF",
#                                     "A2",
#                                     "x")

# print("play A:")
# pprint.pprint(samplePlayA)
# print("play B:")
# pprint.pprint(samplePlayB)
#
#
# WordLog.log(samplePlayA['word'],
#             samplePlayA['position'],
#             samplePlayA['axis'],
#             samplePlayA['score'])
#
# WordLog.log(samplePlayB['word'],
#             samplePlayB['position'],
#             samplePlayB['axis'],
#             samplePlayB['score'])

# Display.print_board()
# print("Letters on the Rack:")
# print(Settings.get_rack())

# a = Datatypes.Word("TESTING", "A1", "x")
# print(a)
# b = Datatypes.Play("TESTING", "A1", "x")
# print(b)
#
# print("Log:")
# pprint.pprint(WordLog.getWholeLog())
# BUG:
# Checks.is_position_open("O8", "J8")
# neighborPositions for O8: 	 ['O7', 'P8', 'O9', 'N8']

# usable = WordSearch.findUsablePositions("I5", "x")
# print(usable, "\n")

# WordSearch.findPlays()

# possibleWords = WordSearch.createWords(usable, "x")

# b = WordSearch.findUsablePositions("I6", "x")
# print(b, "\n")
# c = WordSearch.findUsablePositions("I7", "x")
# print(c, "\n")
# d = WordSearch.findUsablePositions("G10", "x")
# # BUG: H10 is still a usable position
# print(d, "\n")
#Settings.set_rack()


# while there's more than 0 letter in the bag:
bag = Settings.GAME_SETTINGS['bag']
while len(bag) > 0:
    Settings.fill_rack()
    # find the usable areas
    # create turn
    # create all subturns
    # execute turn
# draw letters to the rack, remove from the bag
# find all plays
# if turn 1: usable space is around the center
# find highest scoring play
# execute highest scoring play
# put play to log
# increase turn

