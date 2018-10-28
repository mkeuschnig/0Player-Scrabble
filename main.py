# contains the main game-loop and settings

# import general modules
import random
import re 
import shelve
#from copy import deepcopy
from sys import path


#DEBUG: insert working directory in path to access the Scrabble-specific files
# TODO: work out proper path
##osp.insert(0, 'E:/Projekte/0Player-Scrabble/')
path.insert(-1, "D:\\Projekte\\Scrabble Solver\\0Player-Scrabble\\")

#TODO: check if the other modules exist. OS.path
#http://effbot.org/librarybook/os-path.htm
#appPath = osp.getabspath()

#DEBUG
import pprint

# import scrabble-specific source files
import settings as S
import checks as C
import logic as L
import display as D
import logging as ScrabbleLogging



# ***GLOBALS***
GAMESETTINGS = list(S.getGameSettings())


# list to hold the letters from the bag
RACK = []


# Pseudo Unit-Testing/Sanity-Checks:
#pprint.pprint(GAMESETTINGS)
print(GAMESETTINGS)

# checks.py
C.checkIsPositionValid("A1") is True
C.checkIsPositionValid("O15") is True
C.checkIsPositionValid("B52") is False
C.checkIsPositionValid("Z6") is False

C.checkIsCoordinateValid(0,0) is True
C.checkIsCoordinateValid(99,99) is False
C.checkIsCoordinateValid(75,0) is False
C.checkIsCoordinateValid(-1,-1) is False

# logic.py
list(L.findIndexesOfLetterInWord("A", "ABRACADABRA")) == [0,3,5,7,10]
list(L.findIndexesOfLetterInWord("Z", "BANANA")) == []

L.convertCoordinateToPosition(0, 0) == "A1"
L.convertCoordinateToPosition(14, 14) == "O15"
L.convertCoordinateToPosition(62, 52) is None
L.convertCoordinateToPosition(2, 52) is None
L.convertCoordinateToPosition(52, 2) is None

L.convertPositionToCoordinate("A1") == (0, 0)
L.convertPositionToCoordinate("O15") == (14, 14)
L.convertPositionToCoordinate("Ü92") == (None, None)
L.convertPositionToCoordinate("A92") == (None, None)
L.convertPositionToCoordinate("Z6") == (None, None)

L.getModifiedPosition("H8", -7, -7) == "A1"
L.getModifiedPosition("A1", +7, +7) == "H8"
L.getModifiedPosition("O15", -14, -14) == "A1"
L.getModifiedPosition("H8", -10, -10) is None
L.getModifiedPosition("B1", -4, -4) is None

L.convertPositionsToList("A1", "A5") == ["A1", "A2", "A3", "A4", "A5"]
L.convertPositionsToList("A1", "A1") == ["A1"]
L.convertPositionsToList("A1") == ["A1"]
L.convertPositionsToList("A1", "B2") == [] 

L.set






