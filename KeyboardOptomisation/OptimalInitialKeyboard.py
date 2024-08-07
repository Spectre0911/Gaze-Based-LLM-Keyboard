import string
from KeyboardCharacterOptomiser import calculateAverageWordsReturnedT, createWordTries, getSampleWords
from constants import alphabet, prechosen, BASE_PATH
import random
import math
import copy
import time


def simulatedAnnealing(prechosen, allWordTries, sampleWords):
    print("Iterating")
    T = 1000.0  # initial temperature
    T_min = 50  # minimum temperature
    alpha = 0.98  # cooling rate

    curMinCharSet = prechosen
    curMinCount = calculateAverageWordsReturnedT(
        [[curMinCharSet]], allWordTries, sampleWords)[0]

    globalMinCharSet = curMinCharSet
    globalMinCount = curMinCount

    while T > T_min:
        newCharSet = mutateChars(curMinCharSet)
        avgWords = calculateAverageWordsReturnedT(
            [[newCharSet]], allWordTries, sampleWords)[0]

        deltaE = avgWords - curMinCount
        if deltaE < 0:
            if avgWords < globalMinCount:
                globalMinCount = avgWords
                globalMinCharSet = newCharSet
                print(globalMinCount, globalMinCharSet)
            curMinCount = avgWords
            curMinCharSet = newCharSet

        elif random.random() < math.exp(-deltaE / (T * 20)):
            curMinCount = avgWords
            curMinCharSet = newCharSet
        T *= alpha
    print(globalMinCount, globalMinCharSet)
    return globalMinCharSet


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

    return newSet


def generate_random_charset(k):
    all_characters = string.ascii_lowercase
    random_set = set()
    while len(random_set) < k:
        random_set.add(random.choice(all_characters))
    return random_set


allWordTries = createWordTries()
sampleWords = getSampleWords(100000)
keyboards = []
for i in range(10):
    vals = simulatedAnnealing(
        {'a', 'e', 'i', 'o', 'u', 't', 'h'}, allWordTries, sampleWords)
    print(vals)
    keyboards.append(vals)
    prechosen = generate_random_charset(len(prechosen))


# keyboards = [{'t', 'e', 'r', 'o', 'l', 's', 'a', 'n', 'i'},
#              {'t', 'e', 'r', 'u', 'l', 's', 'a', 'n', 'i'},
#              {'t', 'e', 'r', 'u', 'o', 'l', 's', 'a', 'n'},
#              {'t', 'e', 'r', 'd', 'o', 'l', 's', 'a', 'i'},
#              {'t', 'e', 'r', 'd', 'l', 's', 'a', 'n', 'i'},
#              {'t', 'e', 'm', 'r', 'o', 'l', 's', 'a', 'n'},
#              {'t', 'e', 'r', 'd', 'l', 's', 'a', 'c', 'i'},
#              {'t', 'e', 'r', 'd', 'o', 'l', 's', 'a', 'n'}]


# [calculateAverageWordsReturnedT([[board]],
#                                 allWordTries, sampleWords) for board in keyboards]


# 831884 {'l', 'i', 'e', 'a', 'r', 'o', 's'}
# 778500 {'l', 'i', 'e', 'n', 'a', 'r', 's'}
# 753076 {'l', 'e', 'n', 'a', 'r', 'o', 's'}
