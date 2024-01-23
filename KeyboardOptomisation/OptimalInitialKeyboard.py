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
        [[curMinCharSet]], allWordTries, sampleWords, curMinCharSet)[0]

    globalMinCharSet = curMinCharSet
    globalMinCount = curMinCount

    while T > T_min:
        newCharSet = mutateChars(curMinCharSet)
        avgWords = calculateAverageWordsReturnedT(
            [[newCharSet]], allWordTries, sampleWords, newCharSet)[0]
        deltaE = avgWords - curMinCount

        if deltaE < 0:
            # print("Accepting better solution")
            if avgWords < globalMinCount:
                globalMinCount = avgWords
                globalMinCharSet = newCharSet
            curMinCount = avgWords
            curMinCharSet = newCharSet

        elif random.random() < math.exp(-deltaE / T):
            # print(f"Accepting worse solution with prob {(math.exp(-deltaE / T))}")
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
sampleWords = getSampleWords(10000)
for i in range(10):
    prechosen = generate_random_charset(len(prechosen))
    minCharSet = simulatedAnnealing(prechosen, allWordTries, sampleWords)
