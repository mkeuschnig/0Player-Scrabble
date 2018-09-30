from collections_extended import frozenbag
import timeit



def lettersCanBuildWord(wordToCheck, lettersGiven):
    #
    # since this function is called inside a nested for-loop, wordToCheck.unique_elements(): is the same every time and doesnt need to be re-established every time - rework!
    wordToCheck = frozenbag(wordToCheck)
    
    # handling the joker-character:
    # count the jokers in lettersGiven (= the rack)
    jokers = lettersGiven.count("?")
    lettersGiven = lettersGiven.replace("?","",jokers)

    lettersGiven = frozenbag(lettersGiven) # = letters on the board + letters on the rack


    
    # counts every unique letter in wordToCheck, returns TRUE if all lettersGiven are contained in at least the same amount in wordToCheck.
    # the count of the unique letters must be equal or less to the unique letters in wordToCheck

    # Letters in ERNSTHA+EE:
    # E: 3, R: 1, N: 1, S: 1, T: 1, H: 1, A: 1
    # checking for "THREATENERS":
    # T: 2 vs T: 1 - return False (more in wordToCheck than in lettersGiven)
    # checking for "REST":
    # R: 1, E: less than 3, S: 1, T: 1 - return True
    
    for letter in wordToCheck.unique_elements():
        #DEBUG:
        #print(f"letter: {letter}, amount in word '{wordToCheck}': {wordToCheck.count(letter)}")
        #print(f"available in {lettersGiven}: {lettersGiven.count(letter)}")
        if(wordToCheck.count(letter) > lettersGiven.count(letter)):
            if jokers > 0:
                #print("Joker used")
                jokers -= 1
                continue
            else:
                #print("Word can't be built")
                return False # quits the function in the middle.
    return True


def buildWordAlt(wordToCheck, lettersGiven):
    #implementation of the word-building check without frozenbag
    #fixedPositionsInRange = list(set(wordRange).intersection(fixedPositions))
    listWordTarget = list(wordToCheck)
    listWordSource = list(lettersGiven)
    numJokers = lettersGiven.count("?")

    for letter in set(listWordTarget):
        #print(letter)
        #print("Count in ListWordTarget:", listWordTarget.count(letter))
        #print("Count in ListWordSource:", listWordSource.count(letter))
        countSource = listWordSource.count(letter)
        countTarget = listWordTarget.count(letter)
        if countSource < countTarget:
            # try to use the joker(s) on the first missing letter
            # must have at least 1 joker, and the number of Letters in Source need to be equal to counted letters + number of jokers
            if numJokers > 0 and countSource+numJokers >= countTarget:
                #print(f"{countSource} + {numJokers}=", countSource + numJokers)
                #print(f"Letter {letter} is a Joker")
                numJokers -= 1
                continue
            return False
        else:
            continue
    return True

def buildWord(wordToCheck, lettersGiven):
    #testing if not converting to lists makes it faster
    #listWordTarget = list(wordToCheck)
    #listWordSource = list(lettersGiven)
    numJokers = lettersGiven.count("?")

    for letter in set(wordToCheck):
        #print(letter)
        #print("Count in ListWordTarget:", listWordTarget.count(letter))
        #print("Count in ListWordSource:", listWordSource.count(letter))
        countSource = lettersGiven.count(letter)
        countTarget = wordToCheck.count(letter)
        if countSource < countTarget:
            # try to use the joker(s) on the first missing letter
            # must have at least 1 joker, and the number of Letters in Source need to be equal to counted letters + number of jokers
            if numJokers > 0 and countSource+numJokers >= countTarget:
                #print(f"{countSource} + {numJokers}=", countSource + numJokers)
                #print(f"Letter {letter} is a Joker")
                numJokers -= 1
                continue
            return False
        else:
            continue
    return True

rack = ['?', 'S', 'B', 'M', 'N', 'M', 'F']
allLetters = "".join(rack) + "A"
timeTakenA = 0
timeTakenB = 0
timeTakenC = 0
# SHOWDOWN

for i in range(0,10):
    TimeA = timeit.Timer(lambda: lettersCanBuildWord("BESAMEN", allLetters))
    timeTakenA += TimeA.timeit(number = 100000)

    TimeB = timeit.Timer(lambda: buildWord("BESAMEN", allLetters))
    timeTakenB += TimeB.timeit(number = 100000)
    
    TimeC = timeit.Timer(lambda: buildWordAlt("BESAMEN", allLetters))
    timeTakenC += TimeC.timeit(number = 100000)



print(f"Average Time for TimeA: {timeTakenA/(i+1)}")
lettersCanBuildWord("BESAMEN", allLetters)
print(f"Average Time for TimeB: {timeTakenB/(i+1)}")
buildWord("BESAMEN", allLetters)
print(f"Average Time for TimeC: {timeTakenC/(i+1)}")
buildWordAlt("BESAMEN", allLetters)

for i in range(0,10):
    TimeA = timeit.Timer(lambda: lettersCanBuildWord("FASANMMB", allLetters))
    timeTakenA += TimeA.timeit(number = 100000)

    TimeB = timeit.Timer(lambda: buildWord("FASANMMB", allLetters))
    timeTakenB += TimeB.timeit(number = 100000)
    
    TimeC = timeit.Timer(lambda: buildWordAlt("FASANMMB", allLetters))
    timeTakenC += TimeC.timeit(number = 100000)



print(f"Average Time for TimeA: {timeTakenA/(i+1)}")
lettersCanBuildWord("FASANMMB", allLetters)
print(f"Average Time for TimeB: {timeTakenB/(i+1)}")
buildWord("FASANMMB", allLetters)
print(f"Average Time for TimeC: {timeTakenC/(i+1)}")
buildWordAlt("FASANMMB", allLetters)