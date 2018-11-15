#1234567890123456789012345678901234567890123456789012345678901234567890123456789
# contains the main game-loop and settings

# import general modules
from random import randint
import re 
import shelve
#from copy import deepcopy
from sys import path as OSP

# linter
# TODO: Lint all python-files from the project
#import pylint as lint

# DEBUG: insert working directory in path to access the Scrabble-specific files
# TODO: work out proper path
OSP.insert(0, 'E:\\Projekte\\0Player-Scrabble\\')
#OSP.insert(0, "D:\\Projekte\\Scrabble Solver\\0Player-Scrabble\\")

#TODO: check if the other modules exist. OS.path or sys.path
#http://effbot.org/librarybook/os-path.htm
#appPath = osp.getabspath()

# DEBUG:
import pprint

# import scrabble-specific source files as global
global S, C, L, D, ScrabbleLogging
import settings as S 
import checks as C
import logic as L
import display as D
import logging as ScrabbleLogging

# DEBUG:
import unit_tests as UT


# ***GLOBALS***
# TODO: Make proper Game-Settings in a dict
#global GAMESETTINGS
#GAMESETTINGS = list(S.getGameSettings())

#pprint.pprint(GAMESETTINGS)
#print(GAMESETTINGS)


# Pseudo Unit-Testing/Sanity-Checks: 
UT.unit_tests()

#lint.run_pylint(settings)
#lint.run_pylint(checks)
#lint.run_pylint(logic)
#lint.run_pylint(display)
#lint.run_pylint(logging)
#lint.run_pylint(__name__)


