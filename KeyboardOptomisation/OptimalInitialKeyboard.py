from KeyboardCharacterOptomiser import calculateAverageWordsReturnedT, createWordTries, getSampleWords
from constants import alphabet, prechosen, BASE_PATH
import random
import math
import copy

def simulatedAnnealing(prechosen, initialMinCount):
    """
    Performs simulated annealing to find the best character set for a given word length.
    """
    # The set of all words in the wordlist in tries
    allWordTries = createWordTries()
    # A selection of 10000 randomly chosen words from the wordlist
    sampleWords = getSampleWords(10000)
    count = initialMinCount
    minCharSet = prechosen
    for _ in range(10000):
        newCharSet = mutateChars(minCharSet)
        avgWords = calculateAverageWordsReturnedT([[minCharSet]], allWordTries, sampleWords, minCharSet)[0]
        deltaE = count - avgWords 
        print(deltaE)
        prob = math.exp(-deltaE)
        print(f"p: {prob}, count: {count}, avgWords: {avgWords}")
        if deltaE < 0:
            count = avgWords
            minCharSet = newCharSet
            print(minCharSet)
    print(count, minCharSet)


def mutateChars(prechosen):
    """
    Update 1 character from the prechosen character set

    Args:
        prechosen (Set): The initial guess for optimal characters to be used in size 14 charset
    """
    newSet = copy.deepcopy(prechosen)  
    notPrechosen = alphabet - prechosen

    letterToChange = random.choice(list(prechosen))
    letterToChangeTo = random.choice(list(notPrechosen))

    newSet.remove(letterToChange)
    newSet.add(letterToChangeTo)
    print(len(prechosen), len(newSet), letterToChange, letterToChangeTo)

    return newSet

simulatedAnnealing(prechosen, 100000000)

