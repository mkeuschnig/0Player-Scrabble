import settings as S
import checks as C
import logic as L

def unit_tests():
    # checks.py
    assert C.checkIsPositionValid("A1") is True
    assert C.checkIsPositionValid("O15") is True
    assert C.checkIsPositionValid("B52") is False
    assert C.checkIsPositionValid("Z6") is False

    assert C.checkIsCoordinateValid(0,0) is True
    assert C.checkIsCoordinateValid(99,99) is False
    assert C.checkIsCoordinateValid(75,0) is False
    assert C.checkIsCoordinateValid(-1,-1) is False

    assert C.checkIsPositionEmpty("A1") is True
    assert C.checkIsPositionEmpty("A2") is True
    assert C.checkIsPositionEmpty("A3") is True
    assert C.checkIsPositionEmpty("A4") is True
    assert C.checkIsPositionEmpty("O15") is True

    # logic.py
    assert list(L.findIndexesOfLetterInWord("A", "ABRACADABRA")) == [0,3,5,7,10]
    assert list(L.findIndexesOfLetterInWord("Z", "BANANA")) == []

    assert L.convertCoordinateToPosition(0, 0) == "A1"
    assert L.convertCoordinateToPosition(14, 14) == "O15"
    assert L.convertCoordinateToPosition(62, 52) is None
    assert L.convertCoordinateToPosition(2, 52) is None
    assert L.convertCoordinateToPosition(52, 2) is None

    assert L.convertPositionToCoordinate("A1") == (0, 0)
    assert L.convertPositionToCoordinate("O15") == (14, 14)
    assert L.convertPositionToCoordinate("Ö92") == (None, None)
    assert L.convertPositionToCoordinate("A92") == (None, None)
    assert L.convertPositionToCoordinate("Z6") == (None, None)

    assert L.getModifiedPosition("H8", -7, -7) == "A1"
    assert L.getModifiedPosition("A1", +7, +7) == "H8"
    assert L.getModifiedPosition("O15", -14, -14) == "A1"
    assert L.getModifiedPosition("H8", -10, -10) is None
    assert L.getModifiedPosition("B1", -4, -4) is None

    assert L.convertPositionsToList("A1", "A5") == ["A1", "A2", "A3", "A4", "A5"]
    assert L.convertPositionsToList("A1", "F1") == ["A1", "B1", "C1", 
                                                    "D1", "E1", "F1"]
    assert L.convertPositionsToList("A1", "A1") == ["A1"]
    assert L.convertPositionsToList("A1") == ["A1"]
    assert L.convertPositionsToList("A1", "B2") == [] 

    # Place "ERNST" on actual board
    L.setLetterToPosition("A1", "E")
    L.setLetterToPosition("B1", "R")
    L.setLetterToPosition("C1", "N")
    L.setLetterToPosition("D1", "S")
    L.setLetterToPosition("E1", "T")

    w = ""
    for currentPosition in L.convertPositionsToList("A1", "E1"):
        w += "".join(L.getLetterFromPosition(currentPosition, 
                                                isTemporary = False))
    #print(w)
    assert w == "ERNST"

    # Place "TEMPOR�R" on temporary board
    # global recent temp. Positions are added automatically.
    L.setLetterToPosition("A1", "T", isTemporary = True)
    L.setLetterToPosition("B1", "E", isTemporary = True)
    L.setLetterToPosition("C1", "M", isTemporary = True)
    L.setLetterToPosition("D1", "P", isTemporary = True)
    L.setLetterToPosition("E1", "O", isTemporary = True)
    L.setLetterToPosition("F1", "R", isTemporary = True)
    L.setLetterToPosition("G1", "Ä", isTemporary = True)
    L.setLetterToPosition("H1", "R", isTemporary = True)

    w = ""
    for currentPosition in L.convertPositionsToList("A1", "H1"):
        w += "".join(L.getLetterFromPosition(currentPosition, 
                                             isTemporary = True))
    #print(w)
    assert w == "TEMPORÄR"

    # get filled positions from both boards in various ways.
    assert L.getFilledPositionList("A1") == ["A1"]
    assert L.getFilledPositionList("A1","A0") == []
    assert L.getFilledPositionList("A1", entireAxis = "X")
    assert L.getFilledPositionList("A1", entireAxis = "Y")
    assert L.getFilledPositionList("A1", 
                            entireAxis = "X",
                            isTemporary = True)
    assert L.getFilledPositionList("A1", 
                            entireAxis = "Y",
                            isTemporary = True)
    assert L.getFilledPositionList("A1", 
                            entireAxis = "X",
                            isTemporary = True,
                            returnLetters = True)
    assert L.getFilledPositionList("A1", 
                            entireAxis = "Y",
                            isTemporary = True,
                            returnLetters = True)
    assert L.getFilledPositionList(startPosition = "A1", 
                            isTemporary = True,
                            returnLetters = True,
                            entireAxis = "X") == list("TEMPORÄR")
    assert L.getFilledPositionList("A1", "E1", 
                            returnLetters = True) == list("ERNST")
    assert L.getFilledPositionList("A1", "A10", returnLetters = True) == ["E"]
    assert L.getFilledPositionList("A1", "A10", returnLetters = True) == ["E"]
    assert L.getFilledPositionList("A1", "A10", 
                            returnLetters = True, entireAxis = "X") == list("ERNST")

    # see if "TEMPOR�R" is still in the global variable.
    w = ""
    for tempPosition in S.RECENT_POSITIONS_TEMPORARY:
        w += ''.join(L.getLetterFromPosition(tempPosition, isTemporary = True))
    #print(w)

    # clear the recent temporary positions.
    assert len(S.RECENT_POSITIONS_TEMPORARY) > 0
    L.clearAllTemporaryPositions()
    assert len(S.RECENT_POSITIONS_TEMPORARY) == 0
    # check if everything on the temporary Board is empty.
    assert L.getFilledPositionList("A1", isTemporary = True, entireAxis = "X") == []
    assert L.getFilledPositionList("A1", isTemporary = True, entireAxis = "Y") == []

    # getWordFromPosition
    assert L.getWordFromPosition("A1","E1") == "ERNST"
    assert L.getWordFromPosition("A1","A15") == "E"
    assert L.getWordFromPosition("A0","B12") == ""

    # modifier-fields
    assert L.getWordMultiplier("A1", "A15") == 27
    assert L.getWordMultiplier("A1", "O1") == 27
    assert L.getWordMultiplier("A1", "A8") == 9
    assert L.getWordMultiplier("A1") == 3
    assert L.getWordMultiplier("A2") == 1
    assert L.getWordMultiplier("B2", "N2") == 4
    assert L.getWordMultiplier("B6") == 1

    assert L.getLetterMultiplier("B2") == 1
    assert L.getLetterMultiplier("F2") == 3
    assert L.getLetterMultiplier("B6") == 3
    assert L.getLetterMultiplier("B1") == 1

    # set entire words:
    L.setWordToPosition("ERNST","A2","E2")
    L.setWordToPosition("ER?ST","A3","E3",
                        jokerReplacement = "N")
    L.setWordToPosition("ER??T","A4","E4",
                        jokerReplacement = "NS")
    L.setWordToPosition("?????","A5","E5",
                        jokerReplacement = "ERNST")
    # set word with wrong endPosition: should still only place from A8 to D8
    L.setWordToPosition("EINS","A8","O8","X")
    
    # read entire words
    assert L.getWordFromPosition("A2","E2") == "ERNST"
    assert L.getWordFromPosition("A8","O8") == "EINS"

    # read jokers
    assert L.getLetterFromPosition("A5", showJoker = False) == "E"
    assert L.getLetterFromPosition("A5", showJoker = True) == "?"
    
    assert L.getWordFromPosition("A3","E3", showJoker = True) == "ER?ST"
    assert L.getWordFromPosition("A4","E4", showJoker = True) == "ER??T"
    assert L.getWordFromPosition("A5","E5", showJoker = True) == "?????"
    assert L.getWordFromPosition("A5","E5", showJoker = False) == "ERNST"

    # score letters
    assert L.scoreLetter("E", "O1") == 1
    assert L.scoreLetter("Q", "O1") == 10
    assert L.scoreLetter("Q", "M7") == 20
    assert L.scoreLetter("K", "N6") == 12

    # score Words
    assert L.scoreWord("ERNST", "A1", "E1") == 15
    assert L.scoreWord("ERNST", "A1", axis = "X") == 15
    assert L.scoreWord("WIEDERKEHRENDER", "O1", axis = "Y") == 621
# end of unit_tests()