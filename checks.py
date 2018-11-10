#1234567890123456789012345678901234567890123456789012345678901234567890123456789
# contains the checks used while searching Words or converting Plays.
import settings as S
#from logic import convertCoordinateToPosition, convertPositionToCoordinate
import logic as L


def checkIsPositionValid(positionString:str) -> bool:
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

def checkIsCoordinateValid(x:int, y:int) -> bool:
    """
    Takes x,y-coordinate, returns True if the coordinate is on the board.
    """
    if (x < S.SIZEHORIZONTAL and x >= 0) and (
        y < S.SIZEVERTICAL and y >= 0):
        return True
    else: 
        return False

def checkIsPositionEmpty(position:str, isTemporary:bool=False) -> bool:
    """
    Takes a position (optionally on the temporary board), 
    returns True if the Square is empty.
    """
    x, y = L.convertPositionToCoordinate(position)

    functionBoard = S.getBoardObject(isTemporary)
    
    if len(functionBoard[y][x]) == 0:
        return True
    else:
        return False
