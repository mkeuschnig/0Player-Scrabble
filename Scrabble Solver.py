# TODO: Remove Letters from Rack when they're placed on the board
# TODO: using threading-module to make the program multithreaded (optional).
# TODO: culling for play-suggestions - when the Row already has 15 Letters, no play can be made
#       when "BIENENHAUSES" is already in a (say, horizontal) row, reverse the lookup:
#       Look at the wordlist and look for words that contains BIENENHAUSES in its entirety
#       probably requires a Rework of the WordList to allow for word-searching
#       idea: optional parameter "search", return the list of words of that letter that contain the "search" term
# TODO: Performance improvements - searching the words is painfully slow ATM
# TODO: Handling for the JOKER-character --> on it
#       idea: add "Flags" to a play if: 
#       * all rack-letters are used
#       * jokers are used
#       would improve readability a bit
# TODO: at least one letter from the rack must be used
# TODO: Rework of searchWords so it does actually run through at least 2 times to create shorter words too
# TODO: Culling of available plays - if a play using all rack-letters can be found, discard the others that dont use all of the rack
# TODO: searchWords needs function arguments
# TODO: Rework getting/setting letters/words into the normal and temporary boards
# TODO: create function for logging - move away from print-statements --> use the logging-module: https://opensourcehacker.com/2016/05/22/python-standard-logging-pattern/
# TODO: Move all Settings to either a separate file or to the top of a document
# TODO: use OS to setup the shelve-file in the same folder as the Solver
# also: general cleanup: split source into different files




# mainProgram allows placement of Words and returns scores accordingly.
# user input should be reduced to telling which suggested word should be written to the position, according to the score.



# a Program to show suggestions for any given situation of a scrabble board.
# using no special words provided in the UK or other versions.
# Information based off of: https://de.wikipedia.org/wiki/Scrabble#Spielmaterial
# Warning: contains benign commentary.

import random, pprint, re, os, shelve, copy
from collections_extended import frozenbag


##PREPARATION AND VARIABLES


# ***Distribution of letters:***
# a. define Letters and their Point-Values (in a dict with the letter as the key, and the value as the score.)

# GERMAN:
lettersDict = {"E":1, "N":1, "S":1, "I":1, "R":1, "U":1, "A":1, "D":1, "H":2, "G":2, "L":2, "O":2, "M":3, "B":3, "W":3, "Z":3, "C":4, "F":4, "K":4, "P":4, "Ä":6, "J":6, "Ü":6, "V":6, "Ö":8, "X":8, "Q":10, "Y":10, "?":0, "T":1}
#sorted letters: sletters = pprint.pformat(letters)

# b. define the amount of each letter in the letterBag
bagDict = {"E": 15, "N": 9, "S": 7, "I": 6, "R": 6, "U": 6, "A": 5, "D": 4, "H": 4, "G": 3, "L": 3, "O": 3, "M": 4, "B": 2, "W": 1, "Z": 1, "C": 2, "F": 2, "K": 2, "P": 1, "Ä": 1, "J": 1, "Ü": 1, "V": 1, "Ö": 1, "X": 1, "Q": 1, "Y": 1, "?": 2} #default Joker: 2
#bagDict = {"E": 15, "N": 9, "S": 7, "I": 6, "R": 6, "U": 6, "A": 5, "D": 4, "H": 4, "G": 3, "L": 3, "O": 3, "M": 4, "B": 2, "W": 1, "Z": 1, "C": 2, "F": 2, "K": 2, "P": 1, "Ä": 0, "J": 1, "Ü": 0, "V": 1, "Ö": 0, "X": 1, "Q": 1, "Y": 1, "Joker": 0} #default Joker: 2
# sorted letterBag = sorted pprint.pformat(letterBag)

# create the letterBag for the letters to be put in
letterBag = []

# put the letters in the letterBag:
for letter, amount in bagDict.items(): # iterate over the entire dict, keys are the letters, values are the amounts to be put into the letterBag
    for i in range(0, amount):
        letterBag.append(letter)

# mix the letters in the letterBag around
random.shuffle(letterBag)

# ***Playing field:***
# define the board, to be printed to the console in its own function
# legend: 
# e - empty, 
# c - center, 
# DW - double word score, 
# TW - triple word score, 
# DL - double letter score, 
# TL - triple letter score

# printed as a nested list (2-dimensional)
# since this list is written right-side up, the x and y axes are switched.
# A2 would be board[1][0] instead of 0/1.
# makes little difference gameplay-wise, since the board is symmetrical.
boardValues = [
        # A    B    C    D    E    F    G    H    I    J    K    L    M    N    O
        ['TW', ' ', ' ', 'DL', ' ', ' ', ' ', 'TW', ' ', ' ', ' ', 'DL', ' ', ' ', 'TW'],   # 1
        [' ', 'DW', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'DW', ' '],    # 2
        [' ', ' ', 'DW', ' ', ' ', ' ', 'DL', ' ', 'DL', ' ', ' ', ' ', 'DW', ' ', ' '],    # 3
        ['DL', ' ', ' ', 'DW', ' ', ' ', ' ', 'DL', ' ', ' ', ' ', 'DW', ' ', ' ', 'DL'],   # 4
        [' ', ' ', ' ', ' ', 'DW', ' ', ' ', ' ', ' ', ' ', 'DW', ' ', ' ', ' ', ' '],      # 5
        [' ', 'TL', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'TL', ' '],    # 6
        [' ', ' ', 'DL', ' ', ' ', ' ', 'DL', ' ', 'DL', ' ', ' ', ' ', 'DL', ' ', ' '],    # 7
        ['TW', ' ', ' ', 'DL', ' ', ' ', ' ', 'c', ' ', ' ', ' ', 'DL', ' ', ' ', 'TW'],    # 8
        [' ', ' ', 'DL', ' ', ' ', ' ', 'DL', ' ', 'DL', ' ', ' ', ' ', 'DL', ' ', ' '],    # 9
        [' ', 'TL', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'TL', ' '],    # 10
        [' ', ' ', ' ', ' ', 'DW', ' ', ' ', ' ', ' ', ' ', 'DW', ' ', ' ', ' ', ' '],      # 11
        ['DL', ' ', ' ', 'DW', ' ', ' ', ' ', 'DL', ' ', ' ', ' ', 'DW', ' ', ' ', 'DL'],   # 12
        [' ', ' ', 'DW', ' ', ' ', ' ', 'DL', ' ', 'DL', ' ', ' ', ' ', 'DW', ' ', ' '],    # 13
        [' ', 'DW', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'TL', ' ', ' ', ' ', 'DW', ' '],    # 14
        ['TW', ' ', ' ', 'DL', ' ', ' ', ' ', 'TW', ' ', ' ', ' ', 'DL', ' ', ' ', 'TW']    # 15
        ]

lettersOnBoard = [
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

# create the rack to draw letters onto.
rack = []

# Words from the dictionary get split into a list by length, since we need to look for words with specific lengths

wordListCombined = []

# getLettersRow: Fixed positions for found letters in a row
fixedPositions = []

# list to put playable words into  
buildableWords = []

# list for words that can be placed to a position
availablePlays = []

scoredPlays = []

# list of the highest-scoring words
bestPlays = []

# letters entered into the temporary Board are placed here and removed with removeTemporary()
temporaryPositions = []


# vertical size
sizeV = len(lettersOnBoard)
# horizontal size
sizeH = len(lettersOnBoard[0])







# search_substring_indices from StackExchange
#https://codereview.stackexchange.com/questions/146834/function-to-find-all-occurrences-of-substring
def substring_indexes(letter, word):
    #
    #substring_indexes(substring, string):
    """ 
    Generate indices of where substring begins in string

    >>> list(find_substring('me', "The cat says meow, meow"))
    [13, 19]
    """
    last_found = -1  # Begin at -1 so the next position to search from is 0
    while True:
        # Find next index of substring, by starting after its last known position
        last_found = word.find(letter, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found


# create the X/Y-Coordinate-system on the board:
# Official Notation is A-O on the X-axis, 1-15 on the Y-axis
# X = 0 and Y = 0 returns the top-left field.
# convert x,y-values to Scrabble-Notation
def coordToPosition(x,y):
    #
    # convert the x-value of 0-14 to Letters A to O, returns a single String
    # chr(65) = "A"
    resultX = chr(x+65)
    resultY = str(y+1)
    if x > 14 or y > 14 or x < 0 or y < 0:
        #DEBUG
        #print(f"Invalid coordinate {(x,y)}in coordToPosition")
        return None # invalid coordinate on the board.
    return str(resultX+resultY)

# Convert Scrabble-Notation to x,y-values
def positionToCoord(positionString):
    # returns coordinates x and y from given Scrabble-Notation, input "A1" would return 0,0 
    # ord("A") = 65
    resultX = ord(positionString[0])-65
    resultY = int(positionString[1::])-1 # 1 is index 0
    if resultX < 0 or resultY < 0 or resultX > 14 or resultY > 14:
        #DEBUG
        #print(f"Invalid position {positionString} in positionToCoord")
        return None, None # invalid coordinate on the board.
    return int(resultX), int(resultY)

def getFromPosition(startPosition, endPosition = None, horizontalOrVertical = "0", mode = "letter", temporary = False):
    # collective function to access things on the (temporary or actual) board
    
    
    startX, startY = positionToCoord(startPosition)
    #if startX is None or startY is None: return None


    if endPosition is None:
    # if no endPosition is given, its equal to startPosition
        endX, endY = positionToCoord(startPosition)
    else:
        endX, endY = positionToCoord(endPosition)


    # Guard clause: invalid position, return None:
    if startX is None or endX is None or startX < 0 or startX > (sizeH-1) or startY < 0 or startY > (sizeV-1) or endX < 0 or endX > (sizeH-1) or endY < 0 or endY > (sizeV-1):
        return None
    
    # Guard clause: no mode: crash, 
    
    # orientation not H or V: crash, 
    
    # modes: 
    # "letter" - gets letter(s) from position, returns string
    # "modifier" - returns integer for word and letter-modifiers
    # "empty" - returns True if the given position(s) are empty, False otherwise.
    # "fixed" - returns a list of positions with letters already on them
    # "range" - returns list of positions: "A1, A5": ["A1", "A2", "A3", "A4", "A5"]

    # temporary:
    # True - temporary board gets asked instead of the actual board.
    # temporaryBoard resets itself each time something is set to it.
    # temporaryBoard gets updated after each play and is otherwise identical to lettersOnBoard.
    pass

def setToPosition(startPosition, endPosition = None, horizontalOrVertical = "0", mode = None, temporary = False):
    # collective function to write things into the board (temporary or actual)

    #
    
    pass


def modifyPosition(position, modX = 0, modY = 0, horizontalOrVertical = "0"):
    # returns a position-string with the X/Y value changed.
    if position is None: return None # return invalid position

    x,y = positionToCoord(position)
 
    if horizontalOrVertical[0].upper() == "H":
        # horizontal: Y-modified value is ignored
        return coordToPosition(x+modX,y)

    elif horizontalOrVertical[0].upper() == "V":
        # vertical: X-modified value is ignored
        return coordToPosition(x,y+modY)

    else:
        return coordToPosition(x+modX,y+modY)


def getPositionRange(startPosition, endPosition, horizontalOrVertical):
    # returns a list of positions betweeen startPosition and endPosition
    resultList = []
    # convert positions to coordinates
    startX, startY = positionToCoord(startPosition)
    endX, endY = positionToCoord(endPosition)

    if horizontalOrVertical.upper() == "H":
        # count from starting coordinate to ending coordinage along the X-Axis
        for counter in range(startX, endX+1): #+1 so the ending coordinate is included
            #lettersRow += "".join(lettersOnBoard[y][counter])
            resultList.append(coordToPosition(counter,startY))

    elif horizontalOrVertical.upper() == "V":
        # count from starting coordinate to ending coordinage along the Y-Axis
        for counter in range(startY, endY+1):
            #lettersRow += "".join(lettersOnBoard[counter][x])
            resultList.append(coordToPosition(startX,counter))
    else: 
        print("horizonalOrVertical in getFixedPositions not given or wrong.")
        return

    return resultList


def getFixedPositions(position, horizontalOrVertical = "0"):
    # iterate through the board, note the positions of the already-placed letters
    global fixedPositions
    fixedPositions = []
    x,y = positionToCoord(position)

    # iterate the row letter by letter, return the already-placed letters on the board in a list

    if horizontalOrVertical.upper() == "H":
        for counter in range(0, sizeH):
            #lettersRow += "".join(lettersOnBoard[y][counter])
            if lettersOnBoard[y][counter] is not "0": fixedPositions.append(coordToPosition(counter,y))

    elif horizontalOrVertical.upper() == "V":
        for counter in range(0, sizeV):
            #lettersRow += "".join(lettersOnBoard[counter][x])
            if lettersOnBoard[counter][x] is not "0": fixedPositions.append(coordToPosition(x,counter))

    else: 
        print("horizonalOrVertical in getFixedPositions not given or wrong.")

    return fixedPositions




def removeTemporaryLetters():
    global temporaryBoard, temporaryPositions
    #guard clause: temporaryPositions must be longer than 0
    if len(temporaryPositions) is 0:
        return

    # iterate through the already existing temporary letters on their position
    for entry in temporaryPositions:
        x,y = positionToCoord(entry)
        # remove them only if the square on the actual board is empty
        if temporaryBoard[y][x] is not lettersOnBoard[y][x]:
            #print(f"Removing from temporaryBoard: {temporaryBoard[y][x]}")
            temporaryBoard[y][x] = "0"
        else:
            #print(f"NOT removing temporaryBoard: {temporaryBoard[y][x]} ({lettersOnBoard[y][x]} already on the board)")
            pass
    temporaryPositions.clear()


def isPositionEmpty(positionStart, positionEnd = None, horizontalOrVertical = None):
# function to check if a Square (or line) contains no letters.
# if horizontal, check along lettersOnBoard[number][x]
# if vertical, check along lettersOnBoard[x][number]: 

    startX,startY = positionToCoord(positionStart)
    numChecked = 0
    if positionEnd is None and horizontalOrVertical is None:
        if lettersOnBoard[startY][startX] == "0":
            return True
        else:
            return False
    else:
        endX, endY = positionToCoord(positionEnd)
        if horizontalOrVertical[0].upper() == "H":
            endY = startY
            for i in range(startX, endX+1):
                numChecked += 1
                if lettersOnBoard[startY][i] is not "0":
                    #print(f"Square {coordToPosition(startX,startY)} to {coordToPosition(endX,endY)} not empty. ")
                    #print(f"Square {coordToPosition(i,startY)} taken up by: {lettersOnBoard[startY][i]}")
                    return False
            #print(f"isPositionEmpty from {coordToPosition(startX,startY)} to {coordToPosition(endX,endY)}. Checked {numChecked} Positions.")
            return True
        if horizontalOrVertical[0].upper() == "V":
            endX = startX
            for i in range(startY, endY+1):
                numChecked += 1
                if lettersOnBoard[i][startX] is not "0":
                    #print(f"Square {coordToPosition(startX,startY)} to {coordToPosition(endX,endY)} not empty. ")
                    #print(f"Square {coordToPosition(i,startY)} taken up by: {lettersOnBoard[i][startX]}")
                    return False
            #print(f"isPositionEmpty from {coordToPosition(startX,startY)} to {coordToPosition(endX,endY)}. Checked {numChecked} Positions.")
            return True
        else:
            #print("function isPositionEmpty: 'H' or 'V' expected for variable 'horizontalOrVertical'.")
            pass
            return None




def getWordFromPositions(positionStart, positionEnd, horizontalOrVertical = "0", temporary = False):
    #
    # returns a string from the letters in positionStart to positionEnd.
    global lettersOnBoard, temporaryBoard

    if temporary is True:
        # set Letters into the temporary board
        functionBoard = temporaryBoard
    else:
        # set Letters into the normal board
        functionBoard = lettersOnBoard
    
    # prepare empty string, convert positions
    resultString = ""
    startX,startY = positionToCoord(positionStart)
    endX, endY = positionToCoord(positionEnd)


    if horizontalOrVertical.upper() == "H":
        #endY = startY
        for i in range(startX, endX+1):
            resultString += "".join(functionBoard[startY][i])


    elif horizontalOrVertical.upper() == "V":
        #endX = startX
        for i in range(startY, endY+1):
            resultString += "".join(functionBoard[i][startX])
    else: 
        print("function getWordFromPositions: 'H' or 'V' expected for variable 'horizontalOrVertical'.")
        return None

    return resultString




def getWordModifierFromPosition(currentModifier, position = None, x = None, y = None):
    # multiplies the current Word-modifier by one or more word-modifiers in boardValues
    # TODO: check whether there's a letter already on the board. 
    # ALSO TODO - check if the position can actually be played
    if position is not None:
        x,y = positionToCoord(position)
    position = coordToPosition(x,y)

    if boardValues[y][x] == "TW" and isPositionEmpty(position):
        currentModifier *= 3
    elif (boardValues[y][x] == "DW" or boardValues[y][x] == "c") and isPositionEmpty(position):
        currentModifier *= 2
    #print("Current modifier:", currentModifier)
    return currentModifier



# create another function that returns the letter on a square.
# if there's no Letter on the board ("0"), return the modifier
def getLetterFromPosition(position = "0", x = None, y = None, lettersOnly = False, temporary = False):
    #
    global temporaryBoard

    # returns a single Letter from a given position or x/y-value
    if position is None:
        return None
    if position is not "0":
        x,y = positionToCoord(position)
    if lettersOnBoard[y][x] == "0" and lettersOnly is False:
        return boardValues[y][x]
    else:
        if temporary is True:
            return temporaryBoard[y][x]
        else:
            return lettersOnBoard[y][x]





# function for placing a single letter into a square
# if the same letter is already in place, the play is still valid.
# this makes function setWordonBoard less cumbersome by not having to omit the already-placed letters
def setLetterToPosition(letter, position = None, x = None, y = None, temporary = False):
    global lettersOnBoard, temporaryBoard


    if position is not None:
        x,y = positionToCoord(position)

    position = coordToPosition(x,y)

    if temporary is True:
        # set Letters into the temporary board
        functionBoard = temporaryBoard
        temporaryPositions.append(position)
    else:
        # set Letters into the normal board
        functionBoard = lettersOnBoard


    if functionBoard[y][x] == letter:
        #print(f"Letter {letter} is already on Square {position}")
        pass
    elif functionBoard[y][x] == "0":
        #print(f"Letter {letter} placed on Square {position}")
        functionBoard[y][x] = letter
    else:
        #print(f"Square {position} is not empty: Taken up by {functionBoard[y][x]}. (Temporary: {temporary})")
        pass



# function for placing a word onto the board, given a word, a starting position and horizontal/vertial alignment
def setWordOnBoard(word, position, horizontalOrVertical, temporary = False):
    wordlength = len(word)
    x,y = positionToCoord(position)
    #print(f"Placing {word} at {position}, {horizontalOrVertical}")
    for i in range(0,len(word)):
        if horizontalOrVertical.upper() == "H":
            # Place the word letter by letter along the x-axis
            setLetterToPosition(word[i],None, x+i, y, temporary)
            # TODO: grab letters from the rack to write
        if horizontalOrVertical.upper() == "V":
            # Place the word letter by letter along the x-axis
            setLetterToPosition(word[i],None, x, y+i, temporary)


def scoreLetter(letter, position = None, x = None, y = None):
    # returns a score of a letter on a position, with modifiers.
    # check the position of the given letter in boardValues
    if position is not None:
        x,y = positionToCoord(position)
    position = coordToPosition(x,y)
    modifier = 1
    # getting a value from a dict: dict.get("Key")
    if boardValues[y][x] == "DL" and isPositionEmpty(position):
        modifier = 2
    elif boardValues[y][x] == "TL" and isPositionEmpty(position):
        modifier = 3
    #print("Score current letter:", lettersDict.get(letter) * modifier)
    return lettersDict.get(letter) * modifier



def scoreWord(word, positionStart, horizontalOrVertical = "H"):
    # TODO: in order to not have to evaluate every single combination of words on the entire board, calculate the highest-scoring word for a row/column - if that word is already in the suggestions, skip evaluating that row/col.

    # check if the word is placed on a word-modifier - if yes, collect the score of the single letters
    # and modify the score of the entire word. A word can have more than one multiplier.
    
    
    # extract an eventual joker-character
    jokers = list(substring_indexes("(", word))
    if len(jokers) > 0:
        for entry in jokers:
            replaceIndex = int(entry) + 1 
            #print(word)
            word = word[:replaceIndex] + "?" + word[replaceIndex+1:]
            word = word.replace("(","")
            word = word.replace(")","")
            #print(word)

    # function does not actually place a word or a letter, it just returns a score for a given word on a given position.
    # the score of a word is the sum of all results of scoreLetter, modified where necessary
    startX,startY = positionToCoord(positionStart)
    wordScore = 0
    letterScore = 0
    wordLength = len(word)
    wordModifier = 1



    # get modifiers first
    if horizontalOrVertical[0].upper() == "H":
        endX = startX + wordLength
        endY = startY
        for i in range(startX, endX):
            wordModifier = getWordModifierFromPosition(wordModifier, None, i, startY)
        # score the word
        for letter in range(wordLength):
            wordScore += scoreLetter(word[letter],None,startX + letter, startY)


    elif horizontalOrVertical[0].upper() == "V":
        endX = startX
        endY = startY + wordLength
        for i in range(startY, endY):
            wordModifier = getWordModifierFromPosition(wordModifier, None, startX, i)
        # score the word
        for letter in range(wordLength):
            wordScore += scoreLetter(word[letter],None,startX, startY + letter)
    else:
        print("function scoreWord: 'H' or 'V' expected for variable 'horizontalOrVertical'.")
   
    #print("WordScore: ", wordScore)
    #print("WordModifier:", wordModifier)
    #print(f"Total Score for {word} on {positionStart}: {wordScore * wordModifier}")
    return wordScore * wordModifier






# ***Finding matching words***

# load a dictionary to match the possible combinations from the rack with words in the dictionary
def prepareDictionary():
    #TODO: use OS.path to place the file relative to the script
    #testfile = open(r"D:\Projekte\Scrabble Solver\0Player-Scrabble\deutsch.txt")
    testfile = open(f"E:\Projekte\0Player-Scrabble\deutsch.txt")

    filewords = "".join(str(testfile.read().upper()))
    
    # List for regular expressions for words; starting with 2 letters, up to 15 letters.
    regExListLength = [
        re.compile(r"(^\w{2}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{3}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{4}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{5}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{6}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{7}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{8}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{9}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{10}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{11}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{12}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{13}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{14}$)",re.VERBOSE | re.MULTILINE),
        re.compile(r"(^\w{15}$)",re.VERBOSE | re.MULTILINE)
        ]

    # iterate through the regex-list (words by length, starting with 2 letters)
    for i in range(0,len(regExListLength)):
  
        # create temporary list of words to iterate by containing letter
        tempWords = regExListLength[i].findall(filewords)

        # append 1st dimension to the list 
        wordListCombined.append([])
        

        # iterate through alphabet
        for j in range(0, 26): #ORG: 26
       
            # append 2nd dimension to the list
            wordListCombined[i].append([])

             # chr(65) = "A"
            currentLetter = chr(65+j)
            # A = 0 as index in the wordLists

            # handle Umlauts:
            if currentLetter == "A":    currentLetter = "A|Ä" # containing letter can be "A" OR "Ä"
            if currentLetter == "O":    currentLetter = "O|Ö"
            if currentLetter == "U":    currentLetter = "U|Ü"
        
            # create RegEx from the letter
            regExContains = re.compile(r"\w*"+currentLetter+r"\w*", re.VERBOSE | re.MULTILINE)


            # iterate through the words in the temporary list
            for word in tempWords:
                
                # if the Regex has a match (read: if currentLetter is contained in the current word), append it to the wordList at length[wordlength][letterInAlphabet]
                if regExContains.match(word) is not None: wordListCombined[i][j].append(word)
           
            #wordListByLength.append() # Append the matches of the combined length (2-15) and letter (0-25)
            #wordListCombined[i].append(["?"])
            #print(f"Words with {i+2} letters, Letter {currentLetter}: {len(wordListCombined[i][j])}")
            

    # add the joker-letter with empty lists
    #for i in range(0,len(regExListLength)):
    #    wordListCombined.append(["?"])
        

    # write the completed wordlist to the shelve-file.
    d["wordListCombined"] = wordListCombined
    d.close()



def getFromWordList(length, letter):
    # wordListCombined[0][0] returns Words with the letter A with 2 Letters: subtract 2 from the given length
    if length > 15: length = 15
    # convert the given letter back to a number ("A" would be 0)
    
    # LAZY HACK: STOPGAP-MEASURE TO USE UMLAUTS
    if letter == "Ä":    letter = "A" # containing letter can be "A" OR "Ä" (which is also used in prepareDictionary)
    if letter == "Ö":    letter = "O"
    if letter == "Ü":    letter = "U"
    if letter == "?":    return [0][""]
    
    numLetter = ord(letter)-65


    return wordListCombined[length-2][numLetter]



def getLettersRow(position, horizontalOrVertical = "0"):
    # letters on Board: take a row (or column), parse them them to a String
       
    x,y = positionToCoord(position)
    
    lettersRow = ""
    # iterate the row letter by letter, return the placed letters as string, empty spaces on the board with 0s.

    if horizontalOrVertical.upper() == "H":
        for counter in range(0, sizeH):
            lettersRow += "".join(lettersOnBoard[y][counter])
            #if lettersOnBoard[y][counter] is not "0": fixedPositions.append(coordToPosition(counter,y))

    elif horizontalOrVertical.upper() == "V":
        for counter in range(0, sizeV):
            lettersRow += "".join(lettersOnBoard[counter][x])
            #if lettersOnBoard[counter][x] is not "0": fixedPositions.append(coordToPosition(x,counter))

    else: 
        print("horizonalOrVertical in getLettersRow not given or wrong.")

    #print(fixedPositions)
    return lettersRow


def searchWords(position, lettersRow, horizontalOrVertical):
    #
    #global buildableWords
    global rack

    functionWords = []
    combinedRack = "".join(rack) + lettersRow.replace("0","")
    combinedRackLength = len(combinedRack)

    #print(combinedRack)
    # generate a list of possible words from the combined rack    
    # grab the row of letters on the board
    # Iterate by length of the words, starting with the longest possible
    
    if combinedRackLength > 15: combinedRackLength = 15
    
    wordLengthTarget = 0

    for wordLength in range(combinedRackLength,wordLengthTarget,-1): # count backwards, 2 as the last length    
        if len(functionWords) > 0:
            #wordLengthTarget += int(combinedRackLength/3)
            #wordLengthTarget += 1
            #continue
            pass
        # Iterate by letter in the rack + letters in the fixed positions
        for letter in set(rack):
            #print(set(rack))
            # skip creating a Generator if the letter is a joker
            if letter == "?": 
                continue

            cutoffNumberOfWords = 50 # max number of words for each letter in the rack

            buildableGenerator = (word for word in getFromWordList(wordLength,letter) if lettersCanBuildWord(word, combinedRack) is True)

            for uniqueWord in buildableGenerator:
                if uniqueWord not in functionWords and cutoffNumberOfWords >= 0: 
                    #print("Cutoff Number:",cutoffNumberOfWords)
                    functionWords.append(uniqueWord)
                    #cutoffNumberOfWords -= 1

                #print(f"Words in buildableGenerator for Letter {letter} with {wordLength+2} letters:  ",len(wordListCombined[wordLength][numletter]))
                #print(f"read: wordListCombined[{wordLength}][{numletter}]")
    
                #pprint.pprint(sorted(buildableWords))
    #print("buildable Words:",len(buildableWords))            
    return functionWords



def convertWordToPlay(word, fixedPositions, horizontalOrVertical):
    global availablePlays, temporaryBoard, lettersOnBoard
    #functionPlays = []
    #resetBoard = copy.deepcopy(temporaryBoard)
    

    # guard clauses: 0 fixedPositions, HoV not given or wrong
    if len(horizontalOrVertical) == 0 or horizontalOrVertical is None:
        #print("horizontalOrVertical is wrong: 'H' or 'V' expected")
        return

    if len(fixedPositions) == 0: return


    # ALSO TODO: a string-function that returns the indices of given Letters from a word, should there be more than one.
    # right now, check1 gets confu
    # sed if a Letter occurs more than once in a string.

    # takes a word, checks if it can be played in a row/column, returns starting positions for a play (e.g. ("HEILER", H8, V))
    

    # iterate through the already-placed letters on the board
    
    
    # grab number of jokers on the rack
    numJokers = rack.count("?")

    #print(f"Converting {word} into available play(s)...")
    for position in fixedPositions:
        
        check1 = False
        check2 = False
        check3 = False
        check4 = False

        startPos = 0
        # convert the fixed position to its corresponding letter
        letter = getLetterFromPosition(position)

        # check for an occurence of a fixed position-letter in the word
        # TODO: create function to return a list of occurences of a substring in a string
        #positionInString = word.find(letter)

        
        #testing
        fixedLetterInWord = list(substring_indexes(letter,word))

        #before:
        # if positionInString is not -1:

        if len(fixedLetterInWord) is not 0:
            print("\n")

            #iterate though every occurence of the fixed position in the given word
            for index in fixedLetterInWord:       
            
                # reset temporary board before starting the Checks.
                #print(f"Number of TemporaryPositions: {len(temporaryPositions)}")
                removeTemporaryLetters() 

                # the starting position is (FixedPosition minus index of FixedPosition) in word       


                # Check 1: The coordinates must be A-O, and 0-15 for a starting postion     
                #convert position to coordinate to do the math
                x,y = positionToCoord(position)
                # Horizontal
                if horizontalOrVertical[0] == "H":  
                    startPos = coordToPosition(x - index, y)
                    endPos = modifyPosition(startPos, len(word)-1, 0, horizontalOrVertical)
                    #print("Ending Position:",endPos)
                # Vertical 
                if horizontalOrVertical[0] == "V":  
                    startPos = coordToPosition(x, y - index)
                    endPos = modifyPosition(startPos, 0, len(word)-1, horizontalOrVertical)
                    #print("Ending Position:",endPos)
                # coordToPosition returns None if it's given invalid coordinates.
                #print(f"Starting Position for {word}: {startPos}")
            
                if startPos is not None and endPos is not None:
                    #print("Check 1 (Positions) passed.")
                    check1 = True
                else:
                    #print("!!Check 1 (Positions) failed.")
                    continue
            
            
                # Check 2: the letters on the rack must be able to make the play
                # get a list of positions from Start to End
                wordRange = getPositionRange(startPos,endPos,horizontalOrVertical)

                #if a fixed Position is in the wordRange, add the letter from that fixed position to additionalLetters
                additionalLetters = ""

                #reduce the list to only the fixed positions in the wordRange
                fixedPositionsInRange = list(set(wordRange).intersection(fixedPositions))

                # iterate through the fixed positions
                for counterPosition in fixedPositionsInRange:
                    additionalLetters += "".join(getLetterFromPosition(counterPosition, lettersOnly = True))
                #print("Additional Letters:", additionalLetters)

                # check if the letters on the rack and the additional fixed positions can spell the word.
                if lettersCanBuildWord(word, "".join(rack) + additionalLetters) == True: 
                    #print("Check 2 (buildable from rack) passed.")
                    check2 = True
                else:
                    #print("!!Check 2 (buildable from rack) failed")
                    continue



                # Check 3: the letters from starting position to ending position must actually spell the word.
                # Place Letters into temporary Board
                setWordOnBoard(word, startPos, horizontalOrVertical, temporary = True)

                # Check if the letters from StartingPosition to ending Position are equal to the word
                checkWord = getWordFromPositions(startPos, endPos, horizontalOrVertical, temporary = True)
                #print("CheckWord:", checkWord)
                if word == checkWord:
                    #print("Check 3 (word placed equals word searched) passed.")
                    check3 = True
                else:
                    #print("!!Check 3 (word placed equals word searched) failed.")
                    continue



                # Check 4: before and after the word is an empty space (ie the word doesn't actually collide with other words)
                # exception: the starting position is A or 0, or the ending position is O or 15 (in which case getLetterFromPosition returns None)
                if horizontalOrVertical[0] == "H":
                    squareBefore = getLetterFromPosition(modifyPosition(startPos, -1, 0, horizontalOrVertical), lettersOnly = True, temporary = False)
                    squareAfter = getLetterFromPosition(modifyPosition(endPos, +1, 0, horizontalOrVertical), lettersOnly = True, temporary = False)
                if horizontalOrVertical[0] == "V": 
                    squareBefore = getLetterFromPosition(modifyPosition(startPos, 0, -1, horizontalOrVertical), lettersOnly = True, temporary = False)
                    squareAfter = getLetterFromPosition(modifyPosition(endPos, 0, +1, horizontalOrVertical), lettersOnly = True, temporary = False)

                # if squareBefore is outside of the board (StartPos is either Column A or Row 1)...
                if squareBefore is None:
                    # ...only the square after the word needs to be empty.
                    if squareAfter == "0":
                        #print("Check 4 (Square before/after is empty) passed.")
                        check4 = True
                    else:
                        #print("!!Check 4 (Square before/after is empty) failed.")
                        continue
                # if squareAfter is outside of the board (EndPos is either Column O or Row 15)...
                elif squareAfter is None:
                    # ...only the square before the word needs to be empty.
                    if squareBefore == "0":
                        #print("Check 4 (Square before/after is empty) passed.")
                        check4 = True
                    else:
                        #print("!!Check 4 (Square before/after is empty) failed.")
                        continue
                else:
                    #if the square before and after are inside the board (read: valid positions), then they must both be empty.
                    if squareAfter == "0" and squareBefore == "0":
                        #print("Check 4 (Square before/after is empty) passed.")
                        check4 = True
                    else:
                        #print("!!Check 4 (Square before/after is empty) failed.")
                        continue


                # figure out which letter(s) of the word is/are used by the joker(s) - modify the word before adding it to available plays.
                if numJokers > 0:   
                    word = convertWordToJoker(word,"".join(rack) + additionalLetters)

                # if all checks are True, append the (unique) play to the list functionPlays
                if check1 is True and check2 is True and check3 is True and check4 is True:
                    #if [word, startPos, horizontalOrVertical] not in functionPlays:
                    #    functionPlays.append([word, startPos, horizontalOrVertical])
                    if [word, startPos, horizontalOrVertical] not in availablePlays:
                        availablePlays.append([word, startPos, horizontalOrVertical])
        
        # reset temporary board after each iteration
            #removeTemporaryLetters()   
        #temporaryBoard = copy.deepcopy(resetBoard)
        #print(availablePlays)
    #return functionPlays





#TODO
def checkPlay():
    pass
    # check if the available play neighbors another word or extends an existing word - if the word exists, the play is OK and that neighboring word is scored as well.
    # if the neighboring word doesn't exist, the play is not possible.


def lettersCanBuildWord(wordToCheck, lettersGiven):
    #testing if not converting to lists makes it faster
    #listWordTarget = list(wordToCheck)
    #listWordSource = list(lettersGiven)
    numJokers = lettersGiven.count("?")

    for letter in set(wordToCheck):
        #print(letter)
        #print("Count in ListWordTarget:", listWordTarget.count(letter))
        #print("Count in ListWordSource:", listWordSource.count(letter))
        countSource = lettersGiven.count(letter)
        countTarget = wordToCheck.count(letter)
        if countSource < countTarget:
            # try to use the joker(s) on the first missing letter
            # must have at least 1 joker, and the number of Letters in Source need to be equal to counted letters + number of jokers
            if numJokers > 0 and countSource+numJokers >= countTarget:
                #print(f"{countSource} + {numJokers}=", countSource + numJokers)
                #print(f"Letter {letter} is a Joker")
                numJokers -= 1
                continue
            return False
        else:
            continue
    return True


def convertWordToJoker(wordToCheck, lettersGiven):
    # like lettersCanBuildWord, but returns the Word with Jokers replacing the missing letters
    jokerWord = str(wordToCheck)
    
    wordToCheck = frozenbag(wordToCheck)
    
    lettersGiven = frozenbag(lettersGiven) # = letters on the board + letters on the rack

    
    # handling the joker-character:
    # count the jokers in lettersGiven (= the rack)
    jokers = lettersGiven.count("?") # either 1 or 2 when this function is called.
    
    
    for letter in wordToCheck.unique_elements():
        #DEBUG:
        #print(f"letter: {letter}, amount in word '{wordToCheck}': {wordToCheck.count(letter)}")
        #print(f"available in {lettersGiven}: {lettersGiven.count(letter)}")
        if jokers > 0:
            if(wordToCheck.count(letter) > lettersGiven.count(letter)):
                jokerLetter = letter
                jokers -= 1
        # replace a single letter with a joker
                jokerWord = jokerWord.replace(letter,"("+letter+")",1)
    return jokerWord


# ***Playing the game***
# draw 7 letters from the letterBag and place them on the rack one by one, removing the letter from the letterBag (letterBag.pop(index))
# shuffle the letterBag each time a letter is drawn
def drawLettersFromBag():
    for i in range(len(rack),7):
        if len(letterBag) > 0:
            rack.append(letterBag.pop(random.randint(0,(len(letterBag)-1))))
            random.shuffle(letterBag)






# ***DISPLAY THE ENTIRE THING***
# one square:
# +   +
#  [Q] 
# +   +

# display-mockup, "HA" is already on the board:  E R N S T [H A] F T (score)
# or, only using H: [H] E L D (score)
# turn after:  [H E L D] E N T U M (score)


def printBoard():
    

    #simple table to display the board
    print(" A \t B \t C \t D \t E \t F \t G \t H \t I \t J \t K \t L \t M \t N \t O \n")
    for row in range(len(lettersOnBoard)):
        print("+---"*15)
        for column in range(len(lettersOnBoard[0])):
            print(" " + getLetterFromPosition(y = row, x = column) + "\t", end = "")
            #print("   " + getLetterFromPosition(y = row, x = column) + "   ", end = "")
        print("   " + str(row+1))
    
    print("\n\n")
    # display the letters on the rack
    print("Rack:  ", end = "")
    for letter in rack:
        print(letter, end = "  ")
    # display the score of each letter on the rack
    print("\n")
    print("    ", end = "")
    for letter in rack:
        print(lettersDict.get(letter), end = "  ")




# ***Log the plays.###

# MAIN PROGRAM
def mainProgram():
    global fixedPositions, buildableWords, lettersRow, scoredPlays
    
    #COMMANDS BEFORE THE GAME
    running = True
    score = 0
    # fill the rack with letters from the bag
    drawLettersFromBag()
    HorV = ["H", "V"]


    while running:
        #Turn occurs by selecting one of the displayed possible plays
        
        # MESSAGE
        printBoard()
        print("\n")
        print("\n")
        
        temporaryBoard = copy.deepcopy(lettersOnBoard)
        
        # THINKING

        for orientation in HorV:
            print(orientation)
            # go over each row (A1-A15), horizontal
            for i in range(0,15):
                if orientation == "H":
                    loopPosition = coordToPosition(0,i)
                else:
                    loopPosition = coordToPosition(i,0)

                # get the fixed positions of that row
                fixedPositions = getFixedPositions(loopPosition,orientation)
                lettersRow = getLettersRow(loopPosition,orientation)

                # get the words buildable from the rack with the fixed letters
                buildableWords = searchWords(loopPosition, lettersRow, orientation)
                #pprint.pprint(buildableWords)
                
                # convert them to plays
                for entry in buildableWords:
                    #availablePlays
                    
                    convertWordToPlay(entry, fixedPositions, orientation)
                
                # score the plays

            
            # select the 10 highest-scoring plays, add those to Moves (name pending)

            # reset the buildableWords and fixedPositions
            #pprint.pprint(buildableWords)
            pprint.pprint(availablePlays)


        for play in availablePlays:
            a,b,c = play[0], play[1], play[2]
            d = scoreWord(a,b,c)

            #if len(scoredPlays) <= 10:
                #scoredPlays.append([a,b,c,d])
            #else:
                #continue
            scoredPlays.append([a,b,c,d])

        running = False
        
        print("\n")
        printBoard()
        print("\n")

        #pprint.pprint(availablePlays)
        print("\n")
        pprint.pprint(scoredPlays)

        #buildableWords.clear()
        #availablePlays.clear()
        #scoredPlays.clear()
        pprint.pprint(buildableWords)

        pprint.pprint(availablePlays)

        input("All done, press Enter...")
        

# COMMANDS
# check if the shelve-file already exists
#DictionaryShelve = d = shelve.open(r"D:\Projekte\Scrabble Solver\0Player-Scrabble\dictionary.shelve", writeback = True)
DictionaryShelve = d = shelve.open(r"E:\Projekte\0Player-Scrabble\dictionary.shelve", writeback = True)
#d.close()
#wordListCombined = d.get("wordListCombined")
if d.get("wordListCombined") is None: 
    prepareDictionary()
else:
    wordListCombined = d.get("wordListCombined")
    #print(wordListCombined[0][0])
    d.close()

temporaryBoard = copy.deepcopy(lettersOnBoard)

setWordOnBoard("ERNST", "E8", "H")
setWordOnBoard("AUFPASSEN", "E1", "V")

#setWordOnBoard("BANANENHAUS", "A1", "H")
#setWordOnBoard("FRANKENFENSTERN", "A15", "H")

#temporaryBoard = copy.deepcopy(lettersOnBoard)

#rack.append(list("?SBMNMF"))
#rack = list("?SBMNMF")


#mainProgram()
drawLettersFromBag()
printBoard()

input("PRESS ENTER")

#mainProgram()

print(getFromPosition("A0"))
print(getFromPosition("Y23"))
print(getFromPosition("F4"))