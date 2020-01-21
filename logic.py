# contains the logic to search Words and convert Words to plays
# TODO: grab functions and clean them up
# TODO: __init.py__ to handle the importing of modules (perhaps in settings.py)
# TODO: handling for differently-sized board (super scrabble)
# IDEA: Maybe "isTemporary" is too ambiguous. useTemporaryBoard?


# TODO: make proper Path
# import sys
# sys.path.insert(0, 'E:/Projekte/0Player-Scrabble/')

import checks as C
import settings as S

# from main import GAMESETTINGS
rack = S.RACK


def findIndexesOfLetterInWord(letterToFind: str, wordToSearch: str) -> list:
    # search_substring_indices from StackExchange
    # https://codereview.stackexchange.com/questions/146834/function-to-find-all-occurrences-of-substring
    """ 
    Generate indices of where substring begins in string
    >>> find_substring('me', "The cat says meow, meow"))
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


def convertCoordinateToPosition(x: int, y: int) -> str:
    """
    Convert the x/y-value of 0-14 to Letters A to O, returns a single String.
    Returns None if the given x/y-value is invalid.

    0, 0    -> "A1"
    14, 14  -> "O15"
    26, 65  -> None
    """
    if C.is_coordinate_valid(x, y) is False:
        return None
    else:
        # chr(65) = "A"
        resultX = chr(x + 65)
        resultY = str(y + 1)

    return str(resultX + resultY)


def convertPositionToCoordinate(positionString: str) -> tuple:
    """
    Convert the given Position-String of a square back to x/y-coordinates.
    Returns None if the Position is invalid.

    "A1" -> 0,0
    "O15" -> 14,14
    "Z65" -> None, None
    """
    # ord("A") = 65
    x = int(ord(positionString[0]) - 65)
    y = int(positionString[1:]) - 1
    if C.is_coordinate_valid(x, y) is False:
        return None, None
    else:
        return x, y


def getValueFromBoard(boardObject: object,
                      x: int = None, y: int = None,
                      position: str = None) -> str:
    """
    Return the value of a given position/coordinate from a given board
    (BOARD_ACTUAL, BOARD_TEMPORARY, BOARD_MODIFIERS).
    """
    if position is not None:
        x, y = convertPositionToCoordinate(position)
    return boardObject[y][x]


def setValueToBoard(value: str,
                    boardObject: object,
                    x: int = None, y: int = None,
                    position: str = None):
    """
    Set a value to a given position/coordinate onto the given board
    (BOARD_ACTUAL, BOARD_TEMPORARY, BOARD_MODIFIERS).
    """
    if position is not None:
        x, y = convertPositionToCoordinate(position)
    boardObject[y][x] = value


def getModifiedPosition(position: str,
                        modByX: int = 0,
                        modByY: int = 0) -> str:
    """
    Take a position-string, Return a position-string with the X/Y value changed.
    Return None if the resulting position is invalid.

    "H8", -7, -7 -> "A1" 
    "A1", -20, -20 -> None
    """
    if position is None: return None  # return invalid position

    x, y = convertPositionToCoordinate(position)
    newX = x + modByX
    newY = y + modByY

    if C.is_coordinate_valid(newX, newY) is True:
        return convertCoordinateToPosition(newX, newY)
    else:
        return None


def getAxis(startPosition: str, endPosition: str) -> str:
    if startPosition[0] == endPosition[0]:  # Vertical axis
        return "Y"
    elif startPosition[1:] == endPosition[1:]:  # Horizontal axis
        return "X"
    else:
        print(f"""
        Warning: getAxis({startPosition}, {endPosition}): 
        \t {startPosition} and {endPosition} are not on the same X or Y-Axis.
        """)
        return None


def getEndPosition(word: str, startPosition: str, axis: str) -> str:
    # -1 since we already know the startPosition
    offset = len(word) - 1

    if axis == "X":
        endPosition = getModifiedPosition(startPosition, modByX=offset)
    elif axis == "Y":
        endPosition = getModifiedPosition(startPosition, modByY=offset)
    else:
        raise ValueError("axis takes either 'X' or 'Y'.")
    if C.is_position_valid(endPosition):
        return endPosition
    else:
        return None


def getEndPositionAndAxis(word: str,
                          startPosition: str, endPosition: str,
                          axis: str) -> tuple:
    """
    Determine the endPosition and axis of a word, given its starting position
    and either the intended axis or the endPosition.

    Returning: endPosition, axis

    "TEST", "A1", axis = "X"-> "D1", "X"
    "TEST", "A1", "A4"      -> "A4", "Y"
    """
    # guard clause: endPosition and axis are already given.
    if endPosition is not None and axis is not None:
        return endPosition, axis

    if C.checkEndPositionAndAxisNotNone(endPosition, axis) is True:
        if axis is None:
            axis = getAxis(startPosition, endPosition)
            return endPosition, axis
        if endPosition is None:
            endPosition = getEndPosition(word, startPosition, axis)
            return endPosition, axis


def convertPositionsToList(startPosition: str, endPosition: str = None) -> list:
    """
    Create a list of Positions from startPosition to endPosition (inclusive).

    A1", "A5" -> ["A1", "A2", "A3", "A4", "A5"]
    """
    resultList = []

    startX, startY = convertPositionToCoordinate(startPosition)

    if endPosition is None:
        return [startPosition]
    else:
        endX, endY = convertPositionToCoordinate(endPosition)

    axis = getAxis(startPosition, endPosition)

    if axis == "Y":  # Vertical
        # endY+1 so the ending coordinate is included
        for currentY in range(startY, endY + 1):
            resultList.append(convertCoordinateToPosition(startX, currentY))
    elif axis == "X":  # Horizontal
        for currentX in range(startX, endX + 1):
            resultList.append(convertCoordinateToPosition(currentX, startY))
    else:
        print(f"""
        Warning: convertPositionsToList({startPosition}, {endPosition}): 
        \t {startPosition} and {endPosition} are not on the same X or Y-Axis.
        """)
        return []

    return resultList


def getLetterFromPosition(position: str,
                          isTemporary: bool = False,
                          showJoker: bool = False) -> str:
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


def deleteLetterFromPosition(position: str = None,
                             x: int = None, y: int = None,
                             isTemporary: bool = False):
    """
    Write an empty string to the position of a board
    (either S.BOARD_TEMPORARY or S.BOARD_ACTUAL).
    """
    functionBoard = S.getBoardObject(isTemporary)
    if position is not None:
        x, y = convertPositionToCoordinate(position)
        # functionBoard[y][x] = ''
        setValueToBoard('', functionBoard, x, y)


def setLetterToPosition(position, letterToPlace, isTemporary=False):
    """
    Write a letter to a position on the actual or temporary board.
    Does not remove a letter from the player's Rack.
    """
    functionBoard = S.getBoardObject(isTemporary)

    x, y = convertPositionToCoordinate(position)

    if C.is_position_empty(position, isTemporary) is True:
        # functionBoard[y][x] = letterToPlace
        setValueToBoard(letterToPlace, functionBoard, x, y)
        if isTemporary is True:
            addTemporaryPosition(position)
    else:
        print(f"setLetterToPosition: position {position} is not empty, taken up by {functionBoard[y][x]}")


def getFilledPositionList(startPosition: str,
                          endPosition: str = None,
                          isTemporary: bool = False,
                          returnLetters: bool = False,
                          entireAxis: str = None) -> list:
    """
    Return a list with positions of non-empty squares,
    given startPosition to endPosition (optionally from the temporary board).
    If no endPosition is given and entireAxis is given "X" or "Y", 
    return non-empty positions from entire row (X) / column (Y) of startPosition.

    If returnLetters is True, return list of letters on non-empty squares.

    Example:
    word "TESTING" from A1 to A7 (vertical, along column "A"):
    "A1", "A10" -> ["A1, "A2, "A3", "A4", "A5", "A6", "A7"]
    "A1", "A4" -> ["A1, "A2, "A3", "A4"]
    "A1", entireAxis = "X" -> ["A1"]
    """

    resultList = []

    x, y = convertPositionToCoordinate(startPosition)

    # guard clause: invalid positions of start and end.
    if C.is_coordinate_valid(x, y) is False:
        return []

    if endPosition is not None:
        if C.is_position_valid(endPosition) is False:
            return []

    if entireAxis is not None:
        if entireAxis == "X":
            # startPosition and endPosition become the outermost squares.
            startPosition = convertCoordinateToPosition(0, y)
            endPosition = convertCoordinateToPosition(S.SIZEHORIZONTAL - 1, y)
            positionsToCheck = convertPositionsToList(startPosition,
                                                      endPosition)
        elif entireAxis == "Y":
            startPosition = convertCoordinateToPosition(x, 0)
            endPosition = convertCoordinateToPosition(x, S.SIZEVERTICAL - 1)
            positionsToCheck = convertPositionsToList(startPosition,
                                                      endPosition)
        else:
            raise ValueError("entireAxis takes either 'X' or 'Y' (case-sensitive).")

    else:  # entireAxis IS None:
        if endPosition is None:
            endPosition = startPosition
        positionsToCheck = convertPositionsToList(startPosition,
                                                  endPosition)

    for currentPosition in positionsToCheck:
        if C.is_position_empty(currentPosition, isTemporary) is False:
            if returnLetters is True:
                resultList.append(getLetterFromPosition(currentPosition,
                                                        isTemporary))
            else:
                resultList.append(currentPosition)

    return resultList


def addTemporaryPosition(position: str):
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
        letterTemporary = getLetterFromPosition(tempPos, isTemporary=True)
        letterActual = getLetterFromPosition(tempPos, isTemporary=False)
        if letterTemporary == letterActual:
            continue
        else:
            deleteLetterFromPosition(tempPos, isTemporary=True)

    S.RECENT_POSITIONS_TEMPORARY.clear()


def getWordFromPosition(startPosition: str,
                        endPosition: str,
                        isTemporary: bool = False,
                        showJoker: bool = False) -> str:
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
        resultString = "".join([resultString,
                                getLetterFromPosition(position, isTemporary, showJoker)])
        # resultString += get_letter_from_position(position, isTemporary, showJoker)
    return resultString


def setWordToPosition(wordToSet: str,
                      startPosition: str,
                      endPosition: str = None,
                      axis: str = None,
                      jokerReplacement: str = '',
                      isTemporary: bool = False):
    """
    Place a Word onto the board, given the word-string and a startPosition.
    Either endPosition or axis is required.

    If jokers are in wordToSet, the same number of jokerReplacements is needed.
    jokerReplacement(s) are placed alongside their jokers into a Position.

    Example:
    Set word "STAR" from A1 to A4:
    "STAR", "A1", "A4"
    "STAR", "A1", axis = "X"
    "ST?R", "A1", "A4", jokerReplacements = "A" -> A3 contains "?A"
    """
    # IDEA: print a warning-message if the endPosition gets overwritten.
    # this is quite a cumbersome solution...

    # handling a joker-character: (?)
    # check if number of jokers and replacements match
    if "?" in wordToSet:
        if jokerReplacement is None or (
                wordToSet.count("?") != len(jokerReplacement)):
            raise ValueError(f"""
                Mismatch: 
                Jokers: {wordToSet.count("?")}
                Replacement letters: {len(jokerReplacement)}
                """)

    # -1 because wordLength starts counting at 1.
    endOffset = len(wordToSet) - 1

    # index of jokerReplacement
    jokersUsedIndex = 0

    endPosition, axis = getEndPositionAndAxis(wordToSet,
                                              startPosition, endPosition, axis)

    positionList = convertPositionsToList(startPosition, endPosition)

    for positionIndex, currentLetter in enumerate(wordToSet):
        if currentLetter == "?":
            # join the intended letter for the word to the right of the joker.
            currentLetter += ''.join(jokerReplacement[jokersUsedIndex])
            jokersUsedIndex += 1
        currentPosition = positionList[positionIndex]
        setLetterToPosition(currentPosition, currentLetter, isTemporary)


def getWordMultiplier(startPosition: str, endPosition: str = None) -> int:
    """
    Return the total Word-Multiplier for the area from startPosition to endPosition.
    Word-multipliers stack multiplicatively and each can only be used once.

    "A1", "A15" -> 27 (3 * 3 * 3)
    """
    multiplier = 1

    if endPosition is None or endPosition == startPosition:
        field = getValueFromBoard(S.board_modifiers,
                                  position=startPosition)
        multiplier *= S.MODIFIER_WORD.get(field)
    else:
        positionList = convertPositionsToList(startPosition, endPosition)
        for currentPosition in positionList:
            field = getValueFromBoard(S.board_modifiers,
                                      position=currentPosition)
            if len(field) == 0:  # "" is returned on an empty field.
                continue
            else:
                multiplier *= S.MODIFIER_WORD.get(field)
    return multiplier


def getLetterMultiplier(position: str) -> int:
    """
    Return the Letter-Multiplier for a position.
    Letter-multipliers are counted before word-multipliers and can 
    only be used once.
    """
    multiplier = 1
    field = getValueFromBoard(S.board_modifiers, position=position)
    multiplier *= S.MODIFIER_LETTER.get(field)
    return multiplier


def scoreLetter(letter: str, position: str, isTemporary: bool = False) -> int:
    """
    Return the Score of a single Letter on a Position (temporary or actual board).
    """
    if letter == "?":
        return 0
    if C.is_position_empty(position, isTemporary) is True:
        points = S.GAMESETTINGS["letterScore"].get(letter)
        multiplier = getLetterMultiplier(position=position)
        return points * multiplier
    else:
        letter = getLetterFromPosition(position, isTemporary)
        points = S.GAMESETTINGS["letterScore"].get(letter)
        return points


def scoreWord(word: str,
              startPosition: str,
              endPosition: str = None,
              axis: str = None,
              isTemporary: bool = False):
    """
    Return the total score of a word placed on a board (temporary or actual).
    """
    endPosition, axis = getEndPositionAndAxis(word,
                                              startPosition, endPosition, axis)

    positionList = convertPositionsToList(startPosition, endPosition)

    wordScore = 0
    wordMultiplier = getWordMultiplier(startPosition, endPosition)

    for positionIndex, currentLetter in enumerate(word):
        currentPosition = positionList[positionIndex]
        wordScore += scoreLetter(currentLetter, currentPosition, isTemporary)
    return wordScore * wordMultiplier


# def createWordShelve():
#     # Postponed for now.
#     # Idea: make List sorted by Length (as before), use dict{} of letters to
#     # return the desired List.
#     # Dictionary[2-2].get("Q"): ["QI"]
#     # Dictionary[4-2].get("S"): ["STAR", SETS", "RUST"...]
#     #    """
#     #    Creates a Shelve-File for the language set in settings.py, if it
#     #    doesn't already exist.
#     #    """
#
#     #    # TODO: make sure longer words are also included (super scrabble)
#     #    # create a list with regular expressions for words with 2 letters
#     #    # up to words with 20 letters (super-scrabble)
#
#     # TODO: Simplify/Reformat
#
#     import re
#
#     # alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖ"
#
#     language = str(S.GAMESETTINGS["language"])
#     dictionaryList = []
#
#     # DEBUGPATH for the direct window (remove for release):
#     # get all of these paths from settings.py
#     # debugPath = "E:\\Projekte\\0Player-Scrabble\\"
#     debugPath = "D:\\Projekte\\Scrabble Solver\\0Player-Scrabble\\"
#     fileName = "".join([debugPath, language, ".txt"])
#     dictionaryFile = open(fileName)
#
#     regExWordLength = []
#
#     wordsInFile = "".join(dictionaryFile.read().upper())
#     # shelveFile = "".join([debugPath, "dictionary.shelve"])
#     # TODO: from here onward.
#     shelveFile = S.LANGUAGEWORDS
#
#     # create Regular Expressions for words with 2 to 20 letters.
#     # regExWordLength = []
#     for wordLength in range(2, 20 + 1):  # +1 so the last position is included.
#         regExString = "".join([r"(^\w{", str(wordLength), "}$)"])
#         regExWordLength.append(re.compile(regExString, re.MULTILINE))
#
#     # iterate through the regex-list (words by length,
#     # starting with 2 letters)
#     # for i in range(0,len(regExWordLength)):
#     for expression in regExWordLength:
#         # create temporary list of words to iterate by containing letter
#         tempWords = expression.findall(wordsInFile)
#
#         # append 1st dimension to the list
#         dictionaryList.append([])
#
#         # iterate through alphabet
#         for j in range(0, 26):  # ORG: 26
#
#             # append 2nd dimension to the list
#             dictionaryList[-1].append([])
#
#             # chr(65) = "A"
#             currentLetter = chr(65 + j)
#             # A = 0 as index in the wordLists
#
#             # handle Umlauts:
#             # containing letter can be "A" OR "Ä"
#             if currentLetter == "A":    currentLetter = "A|Ä"
#             if currentLetter == "O":    currentLetter = "O|Ö"
#             if currentLetter == "U":    currentLetter = "U|Ü"
#
#             # create RegEx from the letter
#             regExContains = re.compile(r"\w*" + currentLetter + r"\w*",
#                                        re.VERBOSE | re.MULTILINE)
#
#             # iterate through the words in the temporary list
#             for word in tempWords:
#
#                 # if the Regex has a match (read: if currentLetter
#                 # is contained in the current word), append it to
#                 # the wordList at [wordlength][letterInAlphabet]
#                 if regExContains.match(word) is not None:
#                     dictionaryList[-1][-1].append(word)
#
#             # print(f"""Words with {i+2} letters, Letter {currentLetter}:
#             # {len(wordListCombined[i][j])}""")
#
#     # write the completed wordlist to the shelve-file.
#     shelveFile[S.gameLanguage] = dictionaryList
# # d["wordListCombined"] = wordListCombined
# shelveFile.close()

def readWordsFromTextFile(filepath) -> list:
    pass


def createDictionary(language):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖ"
    wordsDict = {}

    # load dictioary-textfile
    fullWordlist = readWordsFromTextFile()
    # create 2-dimensional Dictionary, 1st key: Wordlength
    for wordLength in range(2, 20+1):

        wordsDict[int(wordLength)] = {}
        for letter in alphabet:
            pass
            # wordsDict[int(wordLength)][letter] = list of words of that length with that letter

        pass

# NEXT UP: unwrangle searchWords
# move the shelve-handling to it's own module
# refactor the shelve to be somewhat readable
# unwrangle SearchWords from the original
