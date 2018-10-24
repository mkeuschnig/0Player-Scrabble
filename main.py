# contains the main game-loop and settings

# import general modules
import random, re, shelve, copy
from os import path as osp

#TODO: check if the other modules exist. OS.path
#http://effbot.org/librarybook/os-path.htm
appPath = osp.getabspath()

#DEBUG
import pprint

# import scrabble-specific source files
import settings as S
import logic as L
import checks as C
import display as D
import logging as log


# ***GLOBALS***
GAMESETTINGS = S.getGameSettings()


# list to hold the letters from the bag
RACK = []


pprint.pprint(GAMESETTINGS)