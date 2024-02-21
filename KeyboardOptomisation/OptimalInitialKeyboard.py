import string
from KeyboardCharacterOptomiser import calculateAverageWordsReturnedT, createWordTries, getSampleWords
from constants import alphabet, prechosen, BASE_PATH
import random
import math
import copy
import time


def simulatedAnnealing(prechosen, allWordTries, sampleWords):
    T = 1000.0  # initial temperature
    T_min = 50  # minimum temperature
    alpha = 0.98  # cooling rate

    curMinCharSet = prechosen
    curMinCount = calculateAverageWordsReturnedT(
        [[curMinCharSet]], allWordTries, sampleWords)[0]

    print(f"Initial count: {curMinCount} for {curMinCharSet}")

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
# for i in range(10):
#     vals = simulatedAnnealing(
#         prechosen, allWordTries, sampleWords)
#     keyboards.append(vals)
#     prechosen = generate_random_charset(len(prechosen))

keyboards = [{'a', 't', 'r', 'l', 'e', 's', 'o', 'n'},
             {'a', 'r', 'l', 'e', 's', 'i', 'o', 'n'},
             {'a', 'r', 'l', 'e', 's', 'i', 'o', 'n'},
             {'a', 't', 'r', 'l', 'e', 's', 'o', 'n'},
             {'d', 'a', 'r', 'l', 'e', 's', 'o', 'n'},
             {'a', 't', 'r', 'l', 'e', 's', 'i', 'n'},
             {'u', 'a', 't', 'r', 'e', 's', 'o', 'n'},
             {'u', 'a', 't', 'r', 'l', 'e', 's', 'n'},
             {'a', 't', 'r', 'l', 'e', 's', 'i', 'n'},
             {'u', 'a', 'r', 'l', 'e', 's', 'o', 'n'}]

[print(board, calculateAverageWordsReturnedT([[board]],
       allWordTries, sampleWords)) for board in keyboards]
