# 1234567890123456789012345678901234567890123456789012345678901234567890123456789
# Globals and Settings go here.
import shelve
from copy import deepcopy
from os import path

# TODO:
appPath = "D:\\Projekte\\Scrabble Solver\\0Player-Scrabble\\"

# ***SETTINGS***
# global GAMESETTINGS

searchPrecision = 0  # default: 100, 0 = search all words.

# LANGUAGE AND LETTER DISTRIBUTION
languages = {"german": "German",
             "english": "English (UK)"}

dictionaries = {"german": path.join(appPath, "german.txt"),
                "english": path.join(appPath, "english.txt")}

# MODE

# scrabble/super-scrabble/etc. - 
# see https://en.wikipedia.org/wiki/Scrabble#Gameboard_formats
modes = {"normal": "Regular Scrabble (15x15)",
         "super": "Super Scrabble (21x21)"}

boards = {"normal":
    [
        # A   B  C   D   E   F   G   H   I   J   K   L   M   N   O
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 1
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 2
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 3
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 4
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 5
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 6
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 7
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 8
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 9
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 10
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 11
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 12
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 13
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 14
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']  # 15
    ],
    "super": # columns A-U, rows 1-21
        [
            # A  B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 1
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 2
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 3
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 4
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 5
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 6
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 7
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 8
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 9
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 10
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 11
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 12
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 13
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 14
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 15
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 16
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 17
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 18
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 19
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],  # 20
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']  # 21
        ]}

# Temporary board
# global BOARD_TEMPORARY

# this just creates a shallow copy.
# BOARD_TEMPORARY = BOARD_ACTUAL[:]

#BOARD_TEMPORARY = deepcopy(BOARD_ACTUAL)

# Board for the Word- and Letter-modifiers:
# global BOARD_MODIFIERS
board_modifiers = {
    "normal": [
        # A   B   C   D    E    F    G    H    I    J    K    L    M    N    O
        ['TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW'],  # 1
        ['', 'DW', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DW', ''],  # 2
        ['', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', ''],  # 3
        ['DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL'],  # 4
        ['', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', ''],  # 5
        ['', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', ''],  # 6
        ['', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', ''],  # 7
        ['TW', '', '', 'DL', '', '', '', 'c', '', '', '', 'DL', '', '', 'TW'],  # 8
        ['', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', ''],  # 9
        ['', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', ''],  # 10
        ['', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', ''],  # 11
        ['DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL'],  # 12
        ['', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', ''],  # 13
        ['', 'DW', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DW', ''],  # 14
        ['TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW']  # 15
    ],
    "super": [
        # A  B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U
        ['QW', '', '', 'DL', '', '', '', 'TW', '', '', 'DL', '', '', 'TW', '', '', '', 'DL', '', '', 'QW'],  # 1
        ['', 'DW', '', '', 'TL', '', '', '', 'DW', '', '', '', 'DW', '', '', '', 'TL', '', '', 'DW', ''],  # 2
        ['', '', 'DW', '', '', 'QL', '', '', '', 'DW', '', 'DW', '', '', '', 'QL', '', '', 'DW', '', ''],  # 3
        ['DL', '', '', 'TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW', '', '', 'DL'],  # 4
        ['', 'TL', '', '', 'DL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DL', '', '', 'TL', ''],  # 5
        ['', '', 'QL', '', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', '', 'QL', '', ''],  # 6
        ['', '', '', 'DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL', '', '', ''],  # 7
        ['TW', '', '', '', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', '', '', '', 'TW'],  # 8
        ['', 'DW', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', 'DW', ''],  # 9
        ['', '', 'DW', '', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', '', 'DW', '', ''],  # 10
        ['DL', '', '', 'TW', '', '', 'DL', '', '', '', 'c', '', '', '', 'DL', '', '', 'TW', '', '', 'DL'],##  # 11
        ['', '', 'DW', '', '', 'DL', '', '', '', 'DL', '', 'DL', '', '', '', 'DL', '', '', 'DW', '', ''],  # 12
        ['', 'DW', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'TL', '', '', 'DW', ''],  # 13
        ['TW', '', '', '', '', '', '', 'DW', '', '', '', '', '', 'DW', '', '', '', '', '', '', 'TW'],  # 14
        ['', '', '', 'DL', '', '', 'DW', '', '', '', 'DL', '', '', '', 'DW', '', '', 'DL', '', '', ''],  # 15
        ['', '', 'QL', '', '', 'DW', '', '', '', 'DL', '', 'DL', '', '', '', 'DW', '', '', 'QL', '', ''],  # 16
        ['', 'TL', '', '', 'DL', '', '', '', 'TL', '', '', '', 'TL', '', '', '', 'DL', '', '', 'TL', ''],  # 17
        ['DL', '', '', 'TW', '', '', 'DL', '', '', '', 'TW', '', '', '', 'DL', '', '', 'TW', '', '', 'DL'], # 18
        ['', '', 'DW', '', '', 'QL', '', '', '', 'DW', '', 'DW', '', '', '', 'QL', '', '', 'DW', '', ''],  # 19
        ['', 'DW', '', '', 'TL', '', '', '', 'DW', '', '', '', 'DW', '', '', '', 'TL', '', '', 'DW', ''],  # 20
        ['QW', '', '', 'DL', '', '', '', 'TW', '', '', 'DL', '', '', 'TW', '', '', '', 'DL', '', '', 'QW'] # 21
    ]
}

# Dict for the Word- and Letter-Modifiers:
# global MODIFIER_WORD
MODIFIER_WORD = {"DW": 2,  # Double Word
                 "TW": 3,  # Triple Word
                 "QW": 4,  # Quadruple Word
                 "DL": 1,  # Double Letter
                 "TL": 1,  # Triple Letter
                 "QL": 1,  # Quadruple Letter
                 "": 1}  # Empty Square

# global MODIFIER_LETTER
MODIFIER_LETTER = {"DW": 1,  # Double Word
                   "TW": 1,  # Triple Word
                   "QW": 1,  # Quadruple Word
                   "DL": 2,  # Double Letter
                   "TL": 3,  # Triple Letter
                   "QL": 4,  # Quadruple Letter
                   "": 1}  # Empty Square

# list for temporary Positions
# global RECENT_POSITIONS_TEMPORARY
RECENT_POSITIONS_TEMPORARY = []

# numerals for maximum x/y-value of the board.
# global SIZEHORIZONTAL
# SIZEHORIZONTAL = len(BOARD_ACTUAL)
# global SIZEVERTICAL
# SIZEVERTICAL = len(BOARD_ACTUAL[0])

# Point-values for letters:
# Keys are letters, values are point-values in the game. 
# German: https://en.wikipedia.org/wiki/Scrabble_letter_distributions#German
# English: https://en.wikipedia.org/wiki/Scrabble_letter_distributions#English
LETTERS = {
    "normal": {
        "german": {
            "E": 1, "N": 1, "S": 1, "I": 1, "R": 1,
            "U": 1, "A": 1, "D": 1, "H": 2, "G": 2,
            "L": 2, "O": 2, "M": 3, "B": 3, "W": 3,
            "Z": 3, "C": 4, "F": 4, "K": 4, "P": 4,
            "Ä": 6, "J": 6, "Ü": 6, "V": 6, "Ö": 8,
            "X": 8, "Q": 10, "Y": 10, "?": 0, "T": 1
        },
        "english": {
            "L": 1, "S": 1, "U": 1, "N": 1, "R": 1,
            "T": 1, "O": 1, "A": 1, "I": 1, "E": 1,
            "G": 2, "D": 2, "B": 3, "C": 3, "M": 3,
            "P": 3, "F": 4, "H": 4, "V": 4, "W": 4,
            "Y": 4, "K": 5, "J": 8, "X": 8, "Q": 10,
            "Z": 10, "?": 0
        }
    },
    "super": {
        # TODO
        "german": {
            "E": 1, "N": 1, "S": 1, "I": 1, "R": 1,
            "U": 1, "A": 1, "D": 1, "H": 2, "G": 2,
            "L": 2, "O": 2, "M": 3, "B": 3, "W": 3,
            "Z": 3, "C": 4, "F": 4, "K": 4, "P": 4,
            "Ä": 6, "J": 6, "Ü": 6, "V": 6, "Ö": 8,
            "X": 8, "Q": 10, "Y": 10, "?": 0, "T": 1
        },
        "english": {
            "L": 1, "S": 1, "U": 1, "N": 1, "R": 1,
            "T": 1, "O": 1, "A": 1, "I": 1, "E": 1,
            "G": 2, "D": 2, "B": 3, "C": 3, "M": 3,
            "P": 3, "F": 4, "H": 4, "V": 4, "W": 4,
            "Y": 4, "K": 5, "J": 8, "X": 8, "Q": 10,
            "Z": 10, "?": 0
        }
    }
}

# Letter distribution
# Keys are letters,
# values are the amount of that letter in the bag at the start of the game.
AMOUNT = {
    "normal": {
        "german": {
            "E": 15, "N": 9, "S": 7, "I": 6, "R": 6,
            "U": 6, "A": 5, "D": 4, "H": 4, "G": 3,
            "L": 3, "O": 3, "M": 4, "B": 2, "W": 1,
            "Z": 1, "C": 2, "F": 2, "K": 2, "P": 1,
            "Ä": 1, "J": 1, "Ü": 1, "V": 1, "Ö": 1,
            "X": 1, "Q": 1, "Y": 1, "?": 2
        },
        "english": {
            "L": 4, "S": 4, "U": 4, "N": 6, "R": 6,
            "T": 6, "O": 8, "A": 9, "I": 9, "E": 12,
            "G": 3, "D": 4, "B": 2, "C": 2, "M": 2,
            "P": 2, "F": 2, "H": 2, "V": 2, "W": 2,
            "Y": 2, "K": 1, "J": 1, "X": 1, "Q": 1,
            "Z": 1, "?": 2
        }
    },
    "super": {
        "german": {
            # double the letters from the normal game,
            # but remove one E, I, N, R each.
            "E": 29, "N": 17, "S": 14, "I": 11, "R": 11,
            "U": 12, "A": 10, "D": 8, "H": 8, "G": 6,
            "L": 6, "O": 6, "M": 8, "B": 4, "W": 2,
            "Z": 2, "C": 4, "F": 4, "K": 4, "P": 2,
            "Ä": 2, "J": 2, "Ü": 2, "V": 2, "Ö": 2,
            "X": 2, "Q": 2, "Y": 2, "?": 4
        },
        "english": {
            "L": 7, "S": 10, "U": 7, "N": 13, "R": 13,
            "T": 15, "O": 15, "A": 16, "I": 13, "E": 24,
            "G": 5, "D": 8, "B": 4, "C": 6, "M": 6,
            "P": 4, "F": 4, "H": 5, "V": 3, "W": 4,
            "Y": 4, "K": 2, "J": 2, "X": 2, "Q": 2,
            "Z": 2, "?": 4
        }
    }
}


def getGameSettings(gameMode: str, gameLanguage: str) -> dict:
    # guard clause: Language and Mode are available
    if gameMode not in modes.keys():
        raise ValueError(f"""{gameMode} is not a valid mode.
        Valid modes: {list(modes.keys())}""")
    if gameLanguage not in languages.keys():
        raise ValueError(f"""{gameLanguage} is not a valid language.
        Valid languages: {list(languages.keys())}""")

    return {"language": gameLanguage,
            "mode": gameMode,
            "dictionary": dictionaries[gameLanguage],
            "letter_score": LETTERS[gameMode][gameLanguage],
            "letter_amounts": AMOUNT[gameMode][gameLanguage],
            "board_actual": deepcopy(boards[gameMode]),
            "board_temporary": deepcopy(boards[gameMode]),
            "board_modifiers": deepcopy(board_modifiers[gameMode]),
            "size_x": len(boards[gameMode]),
            "size_y": len(boards[gameMode][0]),
            }


# Helper-function to return either the temporary or actual board.
# defunct.
# def getBoardObject(isTemporary: bool) -> object:
#     if isTemporary is True:
#         return BOARD_TEMPORARY
#     else:
#         return BOARD_ACTUAL


def loadShelveFile():
    shelveFile = "".join([appPath, "dictionary.shelve"])
    return shelve.open(shelveFile)
    pass


# list to hold the letters from the bag
RACK = []
