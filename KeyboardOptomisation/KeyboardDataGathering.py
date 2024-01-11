from collections import defaultdict, OrderedDict
from KeyboardCharacterOptomiser import createWordTries
from Trie import Trie
from constants import BASE_PATH, alphabet
import matplotlib.pyplot as plt
import numpy as np

# keyboards = [
#     {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'd', 'e'},
#     {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'd', 'e'},
# ]

keyboards = [{'n', 'l', 'r', 'a', 'e', 's', 't', 'o', 'm', 'i', 'd'},
             {'n', 'r', 'o', 'p', 's', 't', 'm', 'l', 'd', 'e', 'i', 'a'}]


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


getKeyboardData(createWordTries(), getAllWords())
