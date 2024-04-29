from collections import defaultdict, OrderedDict
import math
import random
from KeyboardCharacterOptomiser import createWordTries
from Trie import Trie
from constants import BASE_PATH, alphabet, prechosen
import matplotlib.pyplot as plt
import numpy as np


keyboards = [prechosen]


def plot_nested_dict(d):
    keys = sorted(d.keys())
    sub_keys = sorted(set(k for sub_d in d.values() for k in sub_d.keys()))

    ind = np.arange(len(keys))
    width = 0.35

    plt.figure(figsize=(15, 10))

    bottom_values = np.zeros(len(keys))
    for sub_key in sub_keys:
        values = [d[k].get(sub_key, 0) for k in keys]
        plt.bar(ind, values, width,
                label=f'Word Length {sub_key}', bottom=bottom_values)
        bottom_values += values

    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.title('Frequency by Word Count and Word Length')
    plt.xticks(ind, keys)
    plt.legend()

    plt.show()


def getAllWords():
    """
    Get all words from the files based on their length.

    Returns:
        list: List of all words.
    """
    allWords = []
    for i in range(1, 19):
        with open(f"{BASE_PATH}{i}_length.txt", 'r') as file:
            words = file.read().split()
            allWords.extend(words)
    return allWords


def getAverageKeyStrokeScore(halfs, wordList):
    # Store the average number of key strokes with respect to word length
    total = 0
    for word in wordList:
        count = 0
        # Keep track of current half of the switch board
        currentHalf = 0
        for c in word:
            nextHalf = 1 if currentHalf == 0 else 0
            c = c.upper()
            # If the character is in the other half, add 2 to the count and switch the current half
            if c in halfs[nextHalf]:
                count += 2
                currentHalf = nextHalf
            # If the character is in the current half or not on keyboard at all, add 1 to the count
            else:
                count += 1

        total += (count / len(word))
    return total / len(wordList)


def mutateHalves(halfs):
    newHalfs = [halfs[0].copy(), halfs[1].copy()]
    halfOneChar = random.choice(list(newHalfs[0]))
    halfTwoChar = random.choice(list(newHalfs[1]))
    newHalfs[0].remove(halfOneChar)
    newHalfs[0].add(halfTwoChar)
    newHalfs[1].remove(halfTwoChar)
    newHalfs[1].add(halfOneChar)
    return newHalfs


def simulatedAnnealing(halfs, wordList):
    T = 1000.0  # initial temperature
    T_min = 50  # minimum temperature
    alpha = 0.99  # cooling rate

    globalCurMinHalfs = halfs
    globalCurMinScore = getAverageKeyStrokeScore(globalCurMinHalfs, wordList)

    curMinHalfs = halfs
    curMinScore = globalCurMinScore

    while T > T_min:
        tempHalf = mutateHalves(curMinHalfs)
        tempScore = getAverageKeyStrokeScore(tempHalf, wordList)
        deltaE = tempScore - curMinScore

        if deltaE < 0:
            curMinScore = tempScore
            curMinHalfs = tempHalf
            if curMinScore < globalCurMinScore:
                globalCurMinScore = curMinScore
                globalCurMinHalfs = curMinHalfs.copy()

        elif random.random() < math.exp(-(deltaE * 10000) / T):
            curMinScore = tempScore
            curMinHalfs = tempHalf
        print(
            f"Temp: {T}, CurMin: {curMinScore}, GlobalMin: {globalCurMinScore},  GlobalMinHalfs: {globalCurMinHalfs}")
        T *= alpha
    return globalCurMinHalfs, globalCurMinScore


def prettyPrintNestedDict(d):
    nestedKeys, columnTotals, grandTotal = set(), {}, 0

    for val in d.values():
        if isinstance(val, dict):
            nestedKeys.update(val.keys())

    columnTotals = {key: 0 for key in d.keys()}

    print("Row Key", end="\t")
    print("\t".join(map(str, d.keys())), "Total")

    for nestedKey in sorted(nestedKeys):
        rowTotal = 0
        print(nestedKey, end="")
        for col, val in d.items():
            cellValue = val.get(nestedKey, 0) if isinstance(val, dict) else 0
            rowTotal += cellValue
            columnTotals[col] += cellValue
            print(f"\t{cellValue if cellValue else '-'}", end="")
        grandTotal += rowTotal
        print(f"\t{rowTotal}")

    print("Total", end="")
    for total in columnTotals.values():
        print(f"\t{total}", end="")
    print(f"\t{grandTotal}")

    print("CT", end="")
    runningVal = 0
    for total in columnTotals.values():
        runningVal += total
        print(f"\t{runningVal}", end="")
    print(f"\t{runningVal}")


def getKeyboardData(allWordTries, sampleWords):
    count = [10000000] * len(keyboards)
    wordCountFrequency = [defaultdict(
        lambda: defaultdict(int)) for _ in range(len(keyboards))]

    for j, keyboard in enumerate(keyboards):
        unknownCharacterSet = alphabet - keyboard
        tempCount = 0
        for word in sampleWords:
            wordLength = len(word)
            searchRes = allWordTries[wordLength].searchR(
                word, unknownCharacterSet, keyboard)
            wordCount = searchRes[0][0]
            tempCount += wordCount
            wordCountFrequency[j][wordCount][wordLength] += 1

        count[j] = tempCount

    for i in range(len(count)):
        print(
            f"Keyboard: {keyboards[i]}, Returned: {count[i]}, SSS: {sum(wordCountFrequency[i][1].values())/len(sampleWords)}, SST: {sum(wordCountFrequency[i][1].values())/count[i]}")

        sortedDict = OrderedDict(sorted(wordCountFrequency[i].items()))
        for wordCount, lengthDict in sortedDict.items():
            sorted_length_dict = OrderedDict(sorted(lengthDict.items()))
            sortedDict[wordCount] = dict(sorted_length_dict)

        print("Freqs:")
        prettyPrintNestedDict(dict(sortedDict))
        print("\n")

    return count


# getKeyboardData(createWordTries(), getAllWords())
# halfs = [set(['S', 'R', 'A', 'T', 'E']), set(['N', 'D', 'I', 'L', 'O'])]
# wordList = getAllWords()

# print(getAverageKeyStrokeScore(halfs, wordList))
# globalMinHalves, globalMinScore = simulatedAnnealing(halfs, wordList)
# print(globalMinScore == getAverageKeyStrokeScore(globalMinHalves, wordList))


allWordTries = createWordTries()
letterCount = defaultdict(int)
# Count the frequency of each letter
allWords = getAllWords()
totalCharacter = 0
for word in allWords:
    totalCharacter += len(word)
    for letter in word:
        if letter in prechosen:
            letterCount[letter.upper()] += 1
        else:
            # All non-prechosen letters are counted under '%'
            letterCount["%"] += 1

# Define the specific order for the letters
order = ['R', 'E', 'L', 'A', 'T', 'I', 'O', 'N', 'S', '%']

# Reorder the data according to the specified order
letters = order
frequencies = [letterCount[letter] / totalCharacter for letter in letters]

plt.figure(figsize=(10, 5))
plt.bar(letters, frequencies, color='skyblue')
plt.xlabel('Letters')
plt.ylabel('Frequency (%)')
plt.title('Relative Frequency of Selected Letters in Wordlist')
plt.show()
