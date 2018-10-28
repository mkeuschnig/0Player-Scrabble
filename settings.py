# Globals and Settings go here.





# ***SETTINGS***
# TODO: create switch for setting language/modes
searchPrecision = 0 # default: 100, 0 = search all words.


# LANGUAGE AND LETTER DISTRIBUTION
LANGUAGE = "german"



global BOARD_ACTUAL

BOARD_ACTUAL = [
                # A    B    C    D    E    F    G    H    I    J    K    L    M    N    O
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 1
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 2
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 3
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 4
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 5
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 6
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 7
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 8
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 9
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 10
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 11
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 12
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 13
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # 14
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']  # 15
                ]

# Temporary board
global BOARD_TEMPORARY

BOARD_TEMPORARY = BOARD_ACTUAL[:]

# list for temporary Positions




global SIZEHORIZONTAL
SIZEHORIZONTAL = len(BOARD_ACTUAL)
global SIZEVERTICAL
SIZEVERTICAL = len(BOARD_ACTUAL[0])


# Point-values for letters:
# Keys are letters, values are point-values in the game. 
# German: https://en.wikipedia.org/wiki/Scrabble_letter_distributions#German
LETTERSGERMAN = {"E":1, "N":1, "S":1, "I":1, "R":1, "U":1, "A":1, "D":1, "H":2, "G":2, "L":2, "O":2, "M":3, "B":3, "W":3, "Z":3, "C":4, "F":4, "K":4, "P":4, "�":6, "J":6, "�":6, "V":6, "�":8, "X":8, "Q":10, "Y":10, "?":0, "T":1}
# English: https://en.wikipedia.org/wiki/Scrabble_letter_distributions#English
LETTERSENGLISH = {"L":1, "S":1, "U":1, "N":1, "R":1, "T":1, "O":1, "A":1, "I":1, "E":1, "G":2, "D":2, "B":3, "C":3, "M":3, "P":3, "F":4, "H":4, "V":4, "W":4, "Y":4, "K":5, "J":8, "X":8, "Q":10, "Z":10, "?":0}

# Letter distribution
# German:
# Keys are letters, values are the amount of that letter in the bag at the start of the game.
AMOUNTGERMAN = {"E": 15, "N": 9, "S": 7, "I": 6, "R": 6, "U": 6, "A": 5, "D": 4, "H": 4, "G": 3, "L": 3, "O": 3, "M": 4, "B": 2, "W": 1, "Z": 1, "C": 2, "F": 2, "K": 2, "P": 1, "�": 1, "J": 1, "�": 1, "V": 1, "�": 1, "X": 1, "Q": 1, "Y": 1, "?": 2}
# English:
AMOUNTENGLISH = {"L":4, "S":4, "U":4, "N":6, "R":6, "T":6, "O":8, "A":9, "I":9, "E":12, "G":3, "D":4, "B":2, "C":2, "M":2, "P":2, "F":2, "H":2, "V":2, "W":2, "Y":2, "K":1, "J":1, "X":1, "Q":1, "Z":1, "?":2}



# MODE
# scrabble/super-scrabble/etc. - see https://en.wikipedia.org/wiki/Scrabble#Gameboard_formats
MODE = "scrabble"


def getGameSettings():
    global LANGUAGE, MODE
    #DEBUG: should actually be
    # a switcher (secondary dict)
    scores = LETTERSGERMAN
    bag = AMOUNTGERMAN
    return LANGUAGE, MODE, scores, bag