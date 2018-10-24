# contains the logic to search Words and convert Words to plays



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
# Official Notation is A-O on the Y-axis, 1-15 on the X-axis
# X = 0 and Y = 0 returns the top-left field.
# convert x,y-values to Scrabble-Notation
def coordToPosition(x,y):
    #
    # convert the x-value of 0-14 to Letters A to O, returns a single String
    # chr(65) = "A"
    resultX = chr(x+65)
    resultY = str(y+1)
    if x > 14 or y > 14 or x < 0 or y < 0:
        #print(f"Invalid coordinate {(x,y)}in coordToPosition")
        return None # invalid coordinate on the board.
    return str(resultX+resultY)


# Convert Scrabble-Notation to x,y-values
def positionToCoord(positionString):
    # returns coordinates x and y from given Scrabble-Notation, input "A1" would return 0,0, 
    # ord("A") = 65
    resultX = ord(positionString[0])-65
    resultY = int(positionString[1::])-1
    if resultX < 0 or resultY < 0 or resultX > 14 or resultY > 14:
        #print(f"Invalid position {positionString} in positionToCoord")
        return None # invalid coordinate on the board.
    return int(resultX), int(resultY)


def getFromPosition(startPosition, endPosition = None, horizontalOrVertical = "0", mode = None, temporary = False):
    # collective function to access things on the (temporary or actual) board
    
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
    # iterate through the board, return a list of positions with already-placed letters
    global fixedPositions
    fixedPositions = []
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
            #pass
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
