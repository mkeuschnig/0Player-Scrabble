# contains the logic to search Words and convert Words to plays
# TODO: import functions and clean them up
# TODO: handling for differently-sized board (super scrabble)
# TODO: Helper-function for checking validity of given Position/Coord

# TODO: make proper Path
import sys
sys.path.insert(0, 'E:/Projekte/0Player-Scrabble/')

import settings as S
import checks as C


def findIndexesOfLetterInWord(letterToFind, wordToSearch):
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
        last_found = word.find(letter, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found


def convertCoordinateToPosition(x: int, y: int) -> str:
    """
    Convert the x/y-value of 0-14 to Letters A to O, returns a single String.
    Returns None if the given x/y-value is invalid.
    0,0 --> "A1"
    14,14 --> "O15"
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



def convertPositionToCoordinate(positionString):
    # TODO - handle sizeVertical and sizeHorizontal with globals
    """
    Convert the given Position-String of a square back to x,y-coordinates.
    Returns None if the Position is invalid.
    "A1" --> 0,0
    "O15" --> 14,14
    """
    # ord("A") = 65
    resultX = int(ord(positionString[0])-65)
    resultY = int(positionString[1:])-1

    if C.checkIsCoordinateValid(resultX,resultY) is True:
        return resultX, resultY
    else:
        return None
    



def convertPositionsToList(startPosition, endPosition, horizontalOrVertical):
    # TODO: Add handling for omitting horizontalOrVertical (positions can only be on one axis anyway)
    """
    Returns a list of Positions between startPosition and endPosition (inclusive).
    "A1", "A5" --> ["A1", "A2", "A3", "A4", "A5"]
    """
    resultList = []
    # convert positions to coordinates
    startX, startY = positionToCoord(startPosition)
    endX, endY = positionToCoord(endPosition)

    if horizontalOrVertical.upper() == "H":
        for currentX in range(startX, endX+1): #+1 so the ending coordinate is included
            resultList.append(coordToPosition(currentX,startY))

    elif horizontalOrVertical.upper() == "V":
        for currentY in range(startY, endY+1): #+1 so the ending coordinate is included
            resultList.append(coordToPosition(startX,currentY))
    else: 
        print("horizonalOrVertical in getFixedPositions not given or wrong.")
        return

    return resultList



def getFilledPositions(position, horizontalOrVertical = "0"):
    # TODO: don't modify a global in a minor function.
    # iterate through the board, return a list of positions with already-placed letters
    #global fixedPositions
    #fixedPositions = []
    x,y = positionToCoord(position)

    # iterate the row square by square, return the already-placed letters on the board in a list

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

