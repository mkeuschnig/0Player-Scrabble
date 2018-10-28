# contains the logic to search Words and convert Words to plays
# TODO: import functions and clean them up
# TODO: handling for differently-sized board (super scrabble)
# TODO: Helper-function for checking validity of given Position/Coord

# TODO: make proper Path
#import sys
#sys.path.insert(0, 'E:/Projekte/0Player-Scrabble/')

import settings as S
import checks as C


def findIndexesOfLetterInWord(letterToFind:str, wordToSearch:str) -> list:
    # search_substring_indices from StackExchange
    #https://codereview.stackexchange.com/questions/146834/function-to-find-all-occurrences-of-substring
    """ 
    Generate indices of where substring begins in string
    >>> list(find_substring('me', "The cat says meow, meow"))
    [13, 19]

    Returns -1 if no letter is found.
    """
    last_found = -1  # Begin at -1 so the next position to search from is 0
    while True:
        # Find next index of substring, by starting after its last known position
        last_found = wordToSearch.find(letterToFind, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found


def convertCoordinateToPosition(x:int, y:int) -> str:
    """
    Convert the x/y-value of 0-14 to Letters A to O, returns a single String.
    Returns None if the given x/y-value is invalid.
    convertCoordinateToPosition(0, 0)    -> "A1"
    convertCoordinateToPosition(14, 14)  -> "O15"
    convertCoordinateToPosition(26, 65)  -> None
    """
    # invalid coordinate on the board.
    # TODO - handle sizeVertical and sizeHorizontal with globals
    if C.checkIsCoordinateValid(x, y) is False:
        return None
    else:    
        # chr(65) = "A"
        resultX = chr(x+65)
        resultY = str(y+1)
    
    return str(resultX+resultY)


def convertPositionToCoordinate(positionString:str) -> tuple:
    # TODO - handle sizeVertical and sizeHorizontal with globals
    """
    Convert the given Position-String of a square back to x,y-coordinates.
    Returns None if the Position is invalid.
    convertPositionToCoordinate("A1") -> 0,0
    convertPositionToCoordinate("O15") -> 14,14
    convertPositionToCoordinate("Z65") -> None, None
    """
    # ord("A") = 65
    x = int(ord(positionString[0])-65)
    y = int(positionString[1:])-1
    if C.checkIsCoordinateValid(x, y) is False:
        return None, None
    else:
        return x, y
    

def getModifiedPosition(position:str, modByX=0, modByY=0) -> str:
    """
    Takes a position-string, Returns a position-string with the X/Y value changed.
    getModifiedPosition("H8", -7, -7) -> "A1" 
    """
    # 
    if position is None: return None # return invalid position

    x, y = convertPositionToCoordinate(position)
 
    if C.checkIsCoordinateValid(x + modByX, y + modByY) is True:
        return convertCoordinateToPosition(x + modByX, y + modByY)
    else:
        return None


def convertPositionsToList(startPosition:str, endPosition:str=None) -> list:
    """
    Returns a list of Positions between startPosition and endPosition (inclusive).
    convertPositionsToList("A1", "A5") -> ["A1", "A2", "A3", "A4", "A5"]
    """
    
    resultList = []

    startX, startY = convertPositionToCoordinate(startPosition)
    
    if endPosition is None:
        return [startPosition]
    else:
        endX, endY = convertPositionToCoordinate(endPosition)

    if startPosition[0] == endPosition[0]: # Vertical orientation
        for currentY in range(startY, endY+1): # +1 so the ending coordinate is included
            resultList.append(convertCoordinateToPosition(startX,currentY))
    elif startPosition[1:] == endPosition[1:]: # Horizontal orientation
        for currentX in range(startX, endX+1): 
            resultList.append(convertCoordinateToPosition(currentX,startY))
    else:
        print(f"Error: convertPositionsToList: \t {startPosition} and {endPosition} are not on the same X or Y-Axis.")
        return []

    return resultList


def getLetterFromPosition(position, temporaryBoard=False): 
    """
    Returns a Letter from a given position (optionally from the temporary board).
    """
    if temporaryBoard is True:
        functionBoard = S.BOARD_TEMPORARY
    else:
        functionBoard = S.BOARD_ACTUAL

    x, y = convertPositionToCoordinate(position)

    if x is None or y is None: 
        return None
    else:
        return functionBoard[y][x]



def setLetterToPosition(position, letterToPlace, temporaryBoard=False):
    # collective function to write things into the board (temporary or actual)
    if temporaryBoard is True:
        functionBoard = S.BOARD_TEMPORARY

    else:
        functionBoard = S.BOARD_ACTUAL

    x, y = convertPositionToCoordinate(position)

    if C.checkIsPositionEmpty(position) is True:
        functionBoard[y][x] = letterToPlace
    else:
        print(f"setLetterToPosition: position {position} is not empty, taken up by {functionBoard[y][x]}")


# MERGE: merge from local on desktop (orientation should be clear from startPos and EndPos)
def getFilledPositions(startPosition:str, endPosition:str=None, temporaryBoard:bool=False, horizontalOrVertical="0"):
    # iterate through the board, return a list of positions with already-placed letters
    resultList = []
    positionsToCheck = convertPositionsToList(startPosition, endPosition)
 
    if temporaryBoard is True:
        functionBoard = S.BOARD_TEMPORARY
    else:
        functionBoard = S.BOARD_ACTUAL

    for currentPosition in positionsToCheck:
        if C.checkIsPositionEmpty(currentPosition, temporaryBoard) is False:
            resultList.append(getLetterFromPosition(currentPosition))

    return resultList


def removeTemporaryLetters():
    # access the temporary board and the list with the temporary positions
    global temporaryBoard, temporaryPositions

    #guard clause: temporaryPositions must be longer than 0
    if len(temporaryPositions) is 0:
        return

    # iterate through the already existing temporary letters on their position
    for entry in temporaryPositions:
        x,y = positionToCoord(entry)
        # remove them only if the square on the actual board is empty
        if temporaryBoard[y][x] != lettersOnBoard[y][x]:
            #print(f"Removing from temporaryBoard: {temporaryBoard[y][x]}")
            temporaryBoard[y][x] = "0"
        else:
            #print(f"NOT removing temporaryBoard: {temporaryBoard[y][x]} ({lettersOnBoard[y][x]} already on the board)")
            #pass
            continue
    temporaryPositions.clear()


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
    global gameTurn
    # multiplies the current Word-modifier by one or more word-modifiers in boardValues
    # TODO: check whether there's a letter already on the board. 
    # ALSO TODO - check if the position can actually be played
    if position is not None:
        x,y = positionToCoord(position)
    position = coordToPosition(x,y)

    if boardValues[y][x] == "TW" and isPositionEmpty(position):
        currentModifier *= 3
    #elif (boardValues[y][x] == "DW" or boardValues[y][x] == "c") and isPositionEmpty(position):
    elif (boardValues[y][x] == "DW" or boardValues[y][x] == "c") and (isPositionEmpty(position) or gameTurn == 1):
        currentModifier *= 2
    #print("Current modifier:", currentModifier)
    return currentModifier



# create another function that returns the letter on a square.
# if there's no Letter on the board ("0"), return the modifier
def getLetterFromPosition(position = "0", x = None, y = None, lettersOnly = False, temporary = False, displayJokers = False):
    #
    global temporaryBoard, lettersOnBoard

    # returns a single Letter from a given position or x/y-value
    # if an invalid position is given, return None.
    if position is None:
        return None


    if position is not "0":
        x,y = positionToCoord(position)


    if temporary is True:
        functionBoard = temporaryBoard
    else:
        functionBoard = lettersOnBoard

    # if only the letters on the board are needed (fixed positions)
    if lettersOnBoard[y][x] == "0" and lettersOnly is False:
        return boardValues[y][x]
    else:
        letter = functionBoard[y][x]
        # for the purpose of searchWords(), a placed joker-character is used as its actual letter, not a joker.
        if len(letter) == 2:
            if displayJokers is True:
                return letter
            else:
                return letter[1]
        else:
            return letter





# function for placing a single letter into a square
# if the same letter is already in place, the play is still valid.
# this makes function setWordonBoard less cumbersome by not having to omit the already-placed letters
#def setLetterToPosition(letter, position = None, x = None, y = None, temporary = False):
#    global lettersOnBoard, temporaryBoard


#    if position is not None:
#        x,y = positionToCoord(position)

#    position = coordToPosition(x,y)

#    if temporary is True:
#        # set Letters into the temporary board
#        functionBoard = temporaryBoard
#        temporaryPositions.append(position)
#    else:
#        # set Letters into the normal board
#        functionBoard = lettersOnBoard


#    if functionBoard[y][x] == letter:
#        #print(f"Letter {letter} is already on Square {position}")
#        pass
#    elif functionBoard[y][x] == "0":
#        #print(f"Letter {letter} placed on Square {position}")
#        functionBoard[y][x] = letter
#    else:
#        #print(f"Square {position} is not empty: Taken up by {functionBoard[y][x]}. (Temporary: {temporary})")
#        pass



# function for placing a word onto the board, given a word, a starting position and horizontal/vertial alignment
def setWordOnBoard(word, position, horizontalOrVertical, temporary = False):
    x,y = positionToCoord(position)
    mod = 0

    if "?" in word:
        # wordLength is one shorter, since the ?-character and the one afterwards are placed as one
        wordLength = len(word) -1
    else:
        wordLength = len(word)


    #print(f"Placing {word} at {position}, {horizontalOrVertical}")
    # count from 0 to the length of the word
    for i in range(0,wordLength):       
        letter = word[i+mod]

        # ?-character and the one afterwards are placed as one
        if letter == "?":
            # string position is modified by 1 for the rest of the word.
            mod += 1
            letter += word[i+mod]
            #continue


        if horizontalOrVertical.upper() == "H":
            # Place the word letter by letter along the x-axis
            setLetterToPosition(letter,None, x+i, y, temporary)
            # TODO: grab letters from the rack to write
        if horizontalOrVertical.upper() == "V":
            # Place the word letter by letter along the x-axis
            setLetterToPosition(letter,None, x, y+i, temporary)


def scoreLetter(letter, position = None, x = None, y = None):
    # returns a score of a letter on a position, with modifiers.
    # check the position of the given letter in boardValues

    
    if position is not None:
        x,y = positionToCoord(position)

    # if the letter has a length of 2, str[0] is the ?, str[1] is the actual letter.
    # letter can only be a length of 2 if there's a Joker in the square.
    if len(letter) == 2: return 0

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
    
    
    # extract an eventual joker-character, the word "ST?ERN" would become "ST?RN"
    jokers = list(substring_indexes("?", word))
    if len(jokers) > 0:
      for entry in jokers:
          replaceIndex = int(entry) + 1
          word = word[:replaceIndex-1] + "?" + word[replaceIndex+1:]

    #print("SCOREWORD:",word)
    #jokers = list(substring_indexes("(", word))
    #if len(jokers) > 0:
    #    for entry in jokers:
    #        replaceIndex = int(entry) + 1 
    #        #print(word)
    #        word = word[:replaceIndex] + "?" + word[replaceIndex+1:]
    #        word = word.replace("(","")
    #        word = word.replace(")","")
            #print(word)

    # function does not actually place a word or a letter, it just returns a score for a given word on a given position.
    # the score of a word is the sum of all results of scoreLetter, modified where necessary
    startX,startY = positionToCoord(positionStart)
    wordScore = 0
    letterScore = 0
    wordLength = len(word)
    # wordMultiplier: Double Word, Triple Word
    wordMultiplier = 1



    # get modifiers first
    if horizontalOrVertical[0].upper() == "H":
        endX = startX + wordLength
        endY = startY
        for i in range(startX, endX):
            wordMultiplier = getWordModifierFromPosition(wordMultiplier, None, i, startY)
        # score the word
        for letter in range(wordLength):
            wordScore += scoreLetter(word[letter],None,startX + letter, startY)


    elif horizontalOrVertical[0].upper() == "V":
        endX = startX
        endY = startY + wordLength
        for i in range(startY, endY):
            wordMultiplier = getWordModifierFromPosition(wordMultiplier, None, startX, i)
        # score the word
        for letter in range(wordLength):
            wordScore += scoreLetter(word[letter],None,startX, startY + letter)
    else:
        pass
        #print("function scoreWord: 'H' or 'V' expected for variable 'horizontalOrVertical'.")
   
    #print("WordScore: ", wordScore)
    #print("WordModifier:", wordMultiplier)
    #print(f"Total Score for {word} on {positionStart}: {wordScore * wordMultiplier}")
    return wordScore * wordMultiplier
