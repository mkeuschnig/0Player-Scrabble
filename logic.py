#1234567890123456789012345678901234567890123456789012345678901234567890123456789
# contains the logic to search Words and convert Words to plays
# TODO: import functions and clean them up
# TODO: __init.py__ to handle the importing of modules (perhaps in settings.py)
# TODO: handling for differently-sized board (super scrabble)
# TODO: instead of using functionBoard[y][x] (a somewhat backwards approach),
#       use a minor function to set something to X and Y on the given board
# IDEA: Maybe "isTemporary" is too ambiguous. useTemporaryBoard?


# TODO: make proper Path
#import sys
#sys.path.insert(0, 'E:/Projekte/0Player-Scrabble/')

import settings as S
import checks as C

global GAMESETTINGS


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
        # Find next index of substring, by starting after its 
        # last known position
        last_found = wordToSearch.find(letterToFind, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found


def convertCoordinateToPosition(x:int, y:int) -> str:
    """
    Convert the x/y-value of 0-14 to Letters A to O, returns a single String.
    Returns None if the given x/y-value is invalid.

    0, 0    -> "A1"
    14, 14  -> "O15"
    26, 65  -> None
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
    """
    Convert the given Position-String of a square back to x/y-coordinates.
    Returns None if the Position is invalid.

    "A1" -> 0,0
    "O15" -> 14,14
    "Z65" -> None, None
    """
    # ord("A") = 65
    x = int(ord(positionString[0])-65)
    y = int(positionString[1:])-1
    if C.checkIsCoordinateValid(x, y) is False:
        return None, None
    else:
        return x, y
    
def getValueFromBoard(boardObject:object, 
                 x:int=None, y:int=None,
                 position:str=None) -> str:
    """
    Return the value of a given position/coordinate from a given board
    (BOARD_ACTUAL, BOARD_TEMPORARY, BOARD_MODIFIERS).
    """
    if position is not None:
        x, y = convertPositionToCoordinate(position)
    return boardObject[y][x]

def setValueToBoard(value:str,
               boardObject:object, 
               x:int=None, y:int=None,
               position:str=None):
    """
    Set a value to a given position/coordinate onto the given board
    (BOARD_ACTUAL, BOARD_TEMPORARY, BOARD_MODIFIERS).
    """
    if position is not None:
        x, y = convertPositionToCoordinate(position)
    boardObject[y][x] = value


def getModifiedPosition(position:str, modByX=0, modByY=0) -> str:
    """
    Take a position-string, Return a position-string with the X/Y value changed.
    Return None if the resulting position is invalid.

    "H8", -7, -7 -> "A1" 
    "A1", -20, -20 -> None
    """
    if position is None: return None # return invalid position

    x, y = convertPositionToCoordinate(position)
    newCoordinate = (x + modByX, y + modByY)
 
    if C.checkIsCoordinateValid(newCoordinate[0],newCoordinate[1]) is True:
        return convertCoordinateToPosition(newCoordinate[0],newCoordinate[1])
    else:
        return None

def getOrientation(startPosition:str, endPosition:str) -> str:
    if startPosition[0] == endPosition[0]: # Vertical orientation
        return "Y"
    elif startPosition[1:] == endPosition[1:]: # Horizontal orientation
        return "X"
    else:
        print(f"""
        Error: convertPositionsToList: 
        \t {startPosition} and {endPosition} are not on the same X or Y-Axis.
        """)

def convertPositionsToList(startPosition:str, endPosition:str=None) -> list:
    """
    Create a list of Positions between startPosition and endPosition (inclusive).

    A1", "A5" -> ["A1", "A2", "A3", "A4", "A5"]
    """   
    resultList = []

    startX, startY = convertPositionToCoordinate(startPosition)
    
    if endPosition is None:
        return [startPosition]
    else:
        endX, endY = convertPositionToCoordinate(endPosition)

    if getOrientation(startPosition, endPosition) == "Y": # Vertical
        # endY+1 so the ending coordinate is included
        for currentY in range(startY, endY+1): 
            resultList.append(convertCoordinateToPosition(startX,currentY))
    elif getOrientation(startPosition, endPosition) == "X": # Horizontal
        for currentX in range(startX, endX+1): 
            resultList.append(convertCoordinateToPosition(currentX,startY))
    else:
        print(f"""
        Error: convertPositionsToList: 
        \t {startPosition} and {endPosition} are not on the same X or Y-Axis.
        """)
        return []

    return resultList

def getLetterFromPosition(position:str, 
                          isTemporary:bool=False,
                          showJoker:bool=False) -> str: 
    """
    Return a Letter from a given position (optionally from the temporary board).
    If the position contains a joker, showJoker = True returns "?" 
    instead of the letter, and the regular Letter otherwise.
    """
    x, y = convertPositionToCoordinate(position)

    if x is None or y is None: 
        return None
    else:
        functionBoard = S.getBoardObject(isTemporary)
        positionValue = getValueFromBoard(functionBoard, x, y)
        # length of the returned Value is 2 if there's a Joker on it.
        if len(positionValue) == 2:
            if showJoker is True:
                # Joker is always on index 0 on a Square.
                return positionValue[0]
            else:
                return positionValue[1]
        else:
            return positionValue

def deleteLetterFromPosition(position:str=None, 
                            x:int=None, y:int=None,
                            isTemporary:bool=False):
    """
    Write an empty string to the position of a board
    (either S.BOARD_TEMPORARY or S.BOARD_ACTUAL).
    """
    functionBoard = S.getBoardObject(isTemporary)
    if position is not None:
        x, y = convertPositionToCoordinate(position)
        #functionBoard[y][x] = ''
        setValueToBoard('', functionBoard, x, y)

def setLetterToPosition(position, letterToPlace, isTemporary=False):
    """
    Write a letter to a position on the actual or temporary board.
    Does not remove a letter from the player's Rack.
    """
    functionBoard = S.getBoardObject(isTemporary)

    x, y = convertPositionToCoordinate(position)

    if C.checkIsPositionEmpty(position, isTemporary) is True:
        #functionBoard[y][x] = letterToPlace
        setValueToBoard(letterToPlace, functionBoard, x, y)
        if isTemporary is True: 
            addTemporaryPosition(position)
    else:
        print(f"setLetterToPosition: position {position} is not empty, taken up by {functionBoard[y][x]}")

def getFilledPositionList(startPosition:str, endPosition:str=None, 
                          isTemporary:bool=False, 
                          returnLetters:bool=False,
                          entireAxis:str=None) -> list:
    """
    Return a list with positions of non-empty squares,
    given startPosition to endPosition (optionally from the temporary board).
    If no endPosition is given and entireAxis is given "X" or "Y", 
    return non-empty positions from entire row (x)/column (y) of startPosition.

    If returnLetters is True, return list of letters on non-empty squares.

    Example:
    word "TESTING" from A1 to A7 (vertical, along column "A"):
    "A1", "A10" -> ["A1, "A2, "A3", "A4", "A5", "A6", "A7"]
    "A1", "A4" -> ["A1, "A2, "A3", "A4"]
    "A1", wholeRowOrColumn = "row" -> ["A1"]
    """  
    resultList = []

    x, y = convertPositionToCoordinate(startPosition)
    
    #guard clause: invalid positions of start and end.
    if C.checkIsCoordinateValid(x, y) is False:
        return []

    if endPosition is not None:
        if C.checkIsPositionValid(endPosition) is False:
            return []
    
    if entireAxis is not None:
        if entireAxis == "X":
            #startPosition and endPosition become the outermost squares.
            startPosition = convertCoordinateToPosition(0, y)
            endPosition = convertCoordinateToPosition(S.SIZEHORIZONTAL-1, y)
            positionsToCheck = convertPositionsToList(startPosition, 
                                                      endPosition)
        elif entireAxis == "Y":
            startPosition = convertCoordinateToPosition(x, 0)
            endPosition = convertCoordinateToPosition(x, S.SIZEVERTICAL-1)
            positionsToCheck = convertPositionsToList(startPosition, 
                                                      endPosition)
        else:
            raise ValueError("entireAxis takes either 'X' or 'Y' (case-sensitive).")

    else: # entireAxis IS None:
        if endPosition is None:
            endPosition = startPosition

        positionsToCheck = convertPositionsToList(startPosition, 
                                                      endPosition)

    for currentPosition in positionsToCheck:
        if C.checkIsPositionEmpty(currentPosition, isTemporary) is False:
            if returnLetters is True:
                resultList.append(getLetterFromPosition(currentPosition,
                                                        isTemporary))
            else:
                resultList.append(currentPosition)

    return resultList

def addTemporaryPosition(position:str):
    """
    Write a position to the global list of temporary positions.
    """
    S.RECENT_POSITIONS_TEMPORARY.append(position)

def clearAllTemporaryPositions():
    """
    Set positions on the temporary board to empty strings, using entries 
    from global RECENT_POSITIONS_TEMPORARY.

    Do not remove positions that are on the actual board.
    """
    # guard clause: list can't be empty.
    if len(S.RECENT_POSITIONS_TEMPORARY) == 0:
        return

    for tempPos in S.RECENT_POSITIONS_TEMPORARY:
        letterTemporary = getLetterFromPosition(tempPos, isTemporary = True)
        letterActual = getLetterFromPosition(tempPos, isTemporary = False)
        if  letterTemporary == letterActual:
            continue
        else:
            deleteLetterFromPosition(tempPos, isTemporary = True)

    S.RECENT_POSITIONS_TEMPORARY.clear()

def getEndPosition():
    pass

def getWordFromPosition(startPosition:str, endPosition:str, 
                        isTemporary:bool=False,
                        showJoker=False) -> str:
    """
    Return a string from startPosition to endPosition on the actual
    or temporary board.

    Word "TESTING" from A1 to A7 (vertical, along column "A"):
    "A1", "A4" -> "TEST"
    """
    positionList = convertPositionsToList(startPosition, endPosition)
    resultString = ""

    if len(positionList) == 0:
        return resultString

    for position in positionList:
        resultString += getLetterFromPosition(position, isTemporary, showJoker)

    return resultString


def setWordToPosition(wordToSet:str, 
                      startPosition:str, 
                      endPosition:str=None,
                      orientation:str=None,
                      jokerReplacement:str='',
                      isTemporary=False):
    """
    Place a Word onto the board, given the word-string and a startPosition.
    Either endPosition or orientation is required.

    If jokers are in wordToSet, the same number of jokerReplacements is needed.
    jokerReplacement(s) are placed alongside their jokers into a Position.

    Example:
    Set word "STAR" from A1 to A4:
    "STAR", "A1", "A4"
    "STAR", "A1", orientation = "X"
    "ST?R", "A1", "A4", jokerReplacements = "A" -> A3 contains "?A"
    """
    # IDEA: print a warning-message if the endPosition gets overwritten.
    # this is quite a cumbersome solution...

    # handling a joker-character: (?)
    # check if number of jokers and replacements match
    if "?" in wordToSet:
        if jokerReplacement is None or wordToSet.count("?") != len(jokerReplacement):
            raise ValueError(f"""
                Mismatch: 
                Jokers: {wordToSet.count("?")}
                Replacement letters: {len(jokerReplacement)}
                """)

    #-1 because wordLength starts counting at 1.
    endOffset = len(wordToSet)-1

    # index of jokerReplacement
    jokersUsedIndex = 0

    if orientation is None:
        if endPosition is None:
            raise AttributeError("""
            Either orientation or endPosition must be given.
            """)
        else:
            orientation = getOrientation(startPosition, endPosition)
   
    if orientation == "X":
        endPosition = getModifiedPosition(startPosition, modByX = endOffset)
    elif orientation == "Y":
        endPosition = getModifiedPosition(startPosition, modByY = endOffset)
    else:
        raise ValueError("orientation takes either 'X' or 'Y'.")

    positionList = convertPositionsToList(startPosition, endPosition)

    for index, currentPosition in enumerate(positionList):
        currentLetter = wordToSet[index]
        if currentLetter == "?":
            # join the intended letter for the word to the right of the joker.
            currentLetter += ''.join(jokerReplacement[jokersUsedIndex])
            jokersUsedIndex += 1
        setLetterToPosition(currentPosition, currentLetter)

def getWordModifier(startPosition:str, endPosition:str=None) -> int:
    """
    Return the total Word-Multiplier for the area from startPosition to endPosition.
    Word-modifiers stack multiplicatively and each can only be used once.
    """
    modifier = 1

    if endPosition is None or endPosition == startPosition:
        field = getValueFromBoard(S.BOARD_MODIFIERS, 
                                  position = startPosition)
        modifier *= S.MODIFIER_WORD.get(field)
    else:
        positionList = convertPositionsToList(startPosition, endPosition)
        for currentPosition in positionList:
            field = getValueFromBoard(  S.BOARD_MODIFIERS,
                                        position = currentPosition)
            if len(field) == 0: # "" is returned on an empty field.
                continue
            else:
                modifier *= S.MODIFIER_WORD.get(field)

    return modifier

def getLetterModifier(position:str) -> int:
    """
    Return the Letter-Multiplier for a position.
    Letter-multipliers are counted before word-modifiers and can 
    only be used once.
    """
    modifier = 1
    field = getValueFromBoard(S.BOARD_MODIFIERS, position = position)
    modifier *= S.MODIFIER_LETTER.get(field)
    return modifier

def scoreLetter(letter:str, position:str, isTemporary:bool=False) -> int:
    """
    Return the Points from a Letter on a Position.
    """
    if letter == "?":
        return 0
     # TODO: make Gamesettings a proper Dict
     # DEBUG
    if C.checkIsPositionEmpty(position, isTemporary) is True:
        points = GAMESETTINGS[2].get(letter)
        multiplier = getLetterModifier(position=position)
        return points * multiplier
    else:
        letter = L.getLetterFromPosition(position, isTemporary)
        points = GAMESETTINGS[2].get(letter)
        return points

def scoreWord(word:str, 
              startPosition:str, endPosition:str=None, 
              isTemporary:bool=False):
    """
    Return the total score of a word placed on a board (temporary or actual).
    """
    letterList = list(word)
    if endPosition is None:
        endPosition = getModifiedPosition(startPosition, len(word))
    positionList = convertPositionsToList(startPosition, endPosition)
    #checking for orientation might not be necessary.
    # YES IT IS
    # TODO: ADD TINY FUNCTION FOR GRABBING THE POSITION OF THE LAST LETTER OF A GIVEN WORD
    #if orientation == "X":
    #    endPosition = getModifiedPosition(startPosition, modByX = endOffset)
    #elif orientation == "Y":
    #    endPosition = getModifiedPosition(startPosition, modByY = endOffset)
    #else:
    #    raise ValueError("orientation takes either 'X' or 'Y'.")


def scoreWord(word, startPosition, horizontalOrVertical = "H"):
    # TODO: in order to not have to evaluate every single combination of words 
    # on the entire board, calculate the highest-scoring word for a row/column 
    # - if that word is already in the suggestions, skip evaluating that row/col.

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
    startX,startY = positionToCoord(startPosition)
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
    #print(f"Total Score for {word} on {startPosition}: {wordScore * wordMultiplier}")
    return wordScore * wordMultiplier
