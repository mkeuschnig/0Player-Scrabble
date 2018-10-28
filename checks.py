# contains the checks used while searching Words or converting Plays.
import settings as S
#from logic import convertCoordinateToPosition, convertPositionToCoordinate
import logic as L


def checkIsPositionValid(positionString) -> bool:
    """
    Takes a position, returns True if the position is on the board.
    "A1" --> True
    "Y28" --> False
    """
    x, y = L.convertPositionToCoordinate(positionString)
    if x is None or y is None:
        return False
    else:
        return True
    #if checkIsCoordinateValid(x, y) is True:
    #    return True
    #else:
    #    return False

def checkIsCoordinateValid(x, y):
    """
    Takes x,y-coordinate, returns True if the coordinate is on the board.
    """
    if (x < S.SIZEHORIZONTAL and x >= 0) and (
        y < S.SIZEVERTICAL and y >= 0):
        return True
    else: 
        return False

def checkIsPositionEmpty(position, temporaryBoard = False):
    """
    Takes a position (optionally on the temporary board), returns True if the Square is empty.
    """
    x, y = L.convertPositionToCoordinate(position)

    if temporaryBoard is True:
        functionBoard = S.BOARD_TEMPORARY
    else:
        functionBoard = S.BOARD_ACTUAL    
    
    if functionBoard[y][x] == "0":
        return True
    else:
        return False
