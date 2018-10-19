# contains the checks used while searching Words or converting Plays.
import settings as S
from logic import convertCoordinateToPosition, convertPositionToCoordinate



def checkIsPositionValid(position):
    """
    Takes a position, returns True if the position is on the board.
    "A1" --> True
    "Y28" --> False
    """
    x,y = convertPositionToCoordinate(position)
    if checkIsCoordinateValid(x,y) is True:
        return True
    else:
        return False

def checkIsCoordinateValid(x,y):
    """
    Takes x,y-coordinate, returns True if the coordinate is on the board.
    """
    if (x < S.SIZEHORIZONTAL or x > 0) or (
        y < S.SIZEVERTICAL or y > 0):
        return True
    else: 
        return False

def checkIsPositionEmpty(position, temporaryBoard = False):
    """
    Takes a position (optionally on the temporary board), returns True if the Square is empty.
    """

    pass
