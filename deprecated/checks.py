#1234567890123456789012345678901234567890123456789012345678901234567890123456789
# contains the checks used while searching Words or converting Plays.
import settings as S
#from logic import convert_coordinate_to_position, convert_position_to_coordinate
from deprecated import logic_old as L


def is_position_valid(positionString:str) -> bool:
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
    #if is_coordinate_valid(x, y) is True:
    #    return True
    #else:
    #    return False

def is_coordinate_valid(x:int, y:int) -> bool:
    """
    Take x,y-coordinate, return True if the coordinate is on the board.
    """
    if (x < S.SIZEHORIZONTAL and x >= 0) and (
        y < S.SIZEVERTICAL and y >= 0):
        return True
    else: 
        return False

def is_position_empty(position:str, isTemporary:bool=False) -> bool:
    """
    Take a position (optionally on the temporary board), 
    return True if the Square is empty.
    """
    x, y = L.convertPositionToCoordinate(position)

    functionBoard = S.getBoardObject(isTemporary)
    
    if len(functionBoard[y][x]) == 0:
        return True
    else:
        return False

def checkEndPositionAndAxisNotNone(endPosition:str, axis:str) -> bool:
    """
    Take endPosition and an axis, raise an Error if both are None. 
    Return True otherwise.
    """
    if axis is None and endPosition is None:
        raise AttributeError("""
        Either axis or endPosition must be given.
        """)
    else:
        return True
