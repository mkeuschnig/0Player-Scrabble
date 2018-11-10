import timeit

from sys import path as OSP
OSP.insert(0, 'E:\\Projekte\\0Player-Scrabble\\')
import settings as S
import logic as L


#wordModifiers = {"DW":2, "TW":3, "QW":4, "DL":1, "TL":1, "QL":1, "":1}
#letterModifiers = {"DW":1, "TW":1, "QW":1, "DL":2, "TL":3, "QL":4, "":1}
#wordModifiers.setdefault(d=1)

def setWordToPositionNEW(wordToSet:str, startPosition:str, endPosition:str=None, orientation:str=None, jokerLetter:str='', isTemporary=False):
    # IDEA: print a warning-message if the endPosition gets overwritten.
    if "?" in wordToSet:
        if jokerLetter is None or wordToSet.count("?") != len(jokerLetter):
            raise ValueError(f"""
                Mismatch: 
                Jokers: {wordToSet.count("?")}
                Replacement letters: {len(jokerLetter)}
                """)

    #-1 because wordLength starts counting at 1.
    endOffset = len(wordToSet)-1
    jokersUsed = 0

    if orientation is None:
        if endPosition is None:
            raise AttributeError("""
            Either orientation or endPosition must be given.
            """)
        else:
            orientation = L.getOrientation(startPosition, endPosition)

    if orientation == "X":
        endPosition = L.getModifiedPosition(startPosition, modByX = endOffset)
    elif orientation == "Y":
        endPosition = L.getModifiedPosition(startPosition, modByY = endOffset)
    else:
        raise ValueError("orientation takes either 'X' or 'Y'.")

    positionList = L.convertPositionsToList(startPosition, endPosition)
    for index, currentPosition in enumerate(positionList):
        #print(index,currentPosition)
        currentLetter = wordToSet[index]
        if currentLetter == "?":
            currentLetter += ''.join(jokerLetter[jokersUsed])
            jokersUsed += 1
        L.setLetterToPosition(currentPosition, currentLetter)
        #debug

    for delPosition in positionList:
        L.deleteLetterFromPosition(delPosition)

def setWordToPositionOLD(wordToSet:str, position:str, isTemporary=False, horizontalOrVertical = "H"):
    x,y = L.convertPositionToCoordinate(position)
    mod = 0
    positionList = []
    if "?" in wordToSet:
        # wordLength is one shorter, since the ?-character and the one afterwards are placed as one
        wordLength = len(wordToSet) -1
    else:
        wordLength = len(wordToSet)


    #print(f"Placing {word} at {position}, {horizontalOrVertical}")
    # count from 0 to the length of the word
    for i in range(0,wordLength):       
        letter = wordToSet[i+mod]
        # ?-character and the one afterwards are placed as one
        if letter == "?":
            # string position is modified by 1 for the rest of the word.
            mod += 1
            letter += wordToSet[i+mod]
            #continue


        if horizontalOrVertical.upper() == "H":
            # Place the word letter by letter along the x-axis
            currentPosition = L.convertCoordinateToPosition(x+i,y)
            # TODO: grab letters from the rack to write
        if horizontalOrVertical.upper() == "V":
            currentPosition = L.convertCoordinateToPosition(x,y+i)
            # Place the word letter by letter along the x-axis
        positionList.append(currentPosition)
        L.setLetterToPosition(currentPosition, letter, isTemporary)

    for delPosition in positionList:
        L.deleteLetterFromPosition(delPosition)



# SHOWDOWN
timeTakenA = 0
timeTakenB = 0
timeTakenC = 0

for i in range(0,10):
    TimeA = timeit.Timer(lambda: setWordToPositionNEW("FRANKENFENSTERN", "A1", "A15"))
    timeTakenA += TimeA.timeit(number = 10000)

    TimeB = timeit.Timer(lambda: setWordToPositionOLD("FRANKENFENSTERN", "A1", "A15"))
    timeTakenB += TimeB.timeit(number = 10000)
    
    #TimeC = timeit.Timer(lambda: FUNCTION)
    #timeTakenC += TimeC.timeit(number = 10000)



print(f"Average Time for TimeA: {timeTakenA/(i+1)}")

print(f"Average Time for TimeB: {timeTakenB/(i+1)}")



#timeTakenA = 0
#timeTakenB = 0
#timeTakenC = 0

#for i in range(0,10):
#    TimeA = timeit.Timer(lambda: getWordModifierIFELIF("A1"))
#    timeTakenA += TimeA.timeit(number = 10000)

#    TimeB = timeit.Timer(lambda: getWordModifierDICT("A1"))
#    timeTakenB += TimeB.timeit(number = 10000)
    
##    TimeC = timeit.Timer(lambda: buildWordAlt("FASANMMB", allLetters))
##    timeTakenC += TimeC.timeit(number = 100000)



#print(f"Average Time for TimeA: {timeTakenA/(i+1)}")
#getWordModifierIFELIF("A1")
#print(f"Average Time for TimeB: {timeTakenB/(i+1)}")
#getWordModifierDICT("A1")
##print(f"Average Time for TimeC: {timeTakenC/(i+1)}")
##buildWordAlt("FASANMMB", allLetters)