from itertools import combinations
from constants import alphabet, prechosen, BASE_PATH
import random
import math
import Trie as Trie


def getWordDistribution():
    """
    Counts the number of words of each length

    Returns:
        Tuple: (Number of words, array of number of words of each length)
    """
    arr = [0 for i in range(1, 19)]
    for i in range(1, 19):
        with open(f"{BASE_PATH}{i}_length.txt", 'r') as file:
            words = file.read().split()
            arr[i-1] = len(words)
    return (sum(arr), arr)


def getWordLengthProbability():
    total, distribution = getWordDistribution()
    return [count/total for count in distribution]


def getSampleWords(k):
    """
    Get a sample of words based on word length probability.

    Args:
        k (int): Number of words to sample in total.

    Returns:
        list: List of sampled words.
    """
    probs = getWordLengthProbability()
    sampleWords = []
    for i in range(1, 19):
        prop = math.ceil(probs[i-1] * k)
        with open(f"{BASE_PATH}{i}_length.txt", 'r') as file:
            words = file.read().split()
            samples = random.choices(words, k=prop)
            sampleWords.extend(samples)
    return sampleWords


def calculateAverageWordsReturnedT(characterSets, allWordTries, sampleWords):
    frequencyMaps = createWordFrequencyMap()
    totalWordCount = sum([len(m) for m in frequencyMaps.values()])
    minWeight = sum([((totalWordCount - frequencyMaps[len(w)]
                    [w])/totalWordCount) for w in sampleWords])
    # Keeps track of the average number of words returned for the each optimal character set
    count = [10000000] * len(characterSets)
    # Keeps track of the optimal character set
    cSet = [None] * len(characterSets)

    for j, kCharSet in enumerate(characterSets):
        for characterSet in kCharSet:
            tempCount = 0
            for word in sampleWords:
                wordLength = len(word)
                returnedWords = allWordTries[wordLength].searchR(
                    word, characterSet)[0][0]
                # weightedReturnedWords = returnedWords * \
                #     (((totalWordCount) -
                #      frequencyMaps[wordLength][word])/totalWordCount)
                tempCount += returnedWords
            currentCount = count[j]
            if tempCount < currentCount:
                count[j] = tempCount
                cSet[j] = characterSet

    # print("----------")
    # for i in range(len(count)):
    #     print(
    #         f"Keyboard {cSet[i]} has an frequency weighted count of {count[i]} out of a minimum of {len(sampleWords)}")
    return count


def createWordTries():
    """
    Creates tries of words for different word lengths.

    Returns:
        dict: A dictionary containing trie objects for different word lengths.
            The keys are the word lengths, and the values are the corresponding trie objects.
    """
    trieDict = {}

    for i in range(1, 19):
        trieDict[i] = Trie.Trie()

    for i in range(1, 19):
        with open(f"{BASE_PATH}{i}_length.txt", 'r') as file:
            words = file.read().split()
            for word in words:
                trieDict[i].insert(word)

    return trieDict


def createWordFrequencyMap():
    """
    Creates an map of maps where each index i represents a map of words of length i and their frequency.

    Returns:
        list: An array where each index i contains a dictionary of words of length i and their frequency.
    """
    frequencyArray = {}

    for i in range(1, 19):
        frequencyArray[i] = {}

    with open(f"{BASE_PATH}all-normalized-words.txt", 'r') as file:
        words = file.read().split()
        for lineNumber, word in enumerate(words):
            frequencyArray[len(word)][word] = lineNumber - 1

    return frequencyArray


def calculateAverageWordsReturnedIncremental(allWordTries, sampleWords, prechosen):
    initialLength = len(prechosen)
    # Keeps track of the average number of words returned for the each optimal character set
    count = [10000000] * 26
    # Keeps track of the optimal character set
    cSet = [None] * 26
    singleCount = [0] * 26

    for j in range(len(prechosen), 26):
        combs = generateKLengthCharacterSets(j, prechosen)
        for characterSet in combs:
            unknownCharacterSet = alphabet - characterSet
            tempCount = 0
            tempSingleWord = 0
            for word in sampleWords:
                wordLength = len(word)
                wordCount = allWordTries[wordLength].searchR(
                    word, unknownCharacterSet, characterSet)[0][0]
                tempCount += wordCount
                if wordCount == 1:
                    tempSingleWord += 1
            currentCount = count[j-initialLength]
            if tempCount < currentCount:
                count[j-initialLength] = tempCount
                cSet[j-initialLength] = characterSet
                singleCount[j-initialLength] = tempSingleWord
        prechosen = cSet[j-initialLength]

    # print("----------")
    for i in range(len(count)):
        print(
            f"Keyboard {cSet[i]} has an average of {count[i]} words returned where only 1 word was returned {singleCount[i]} times")
    return count


def generateKLengthCharacterSets(k, prechosen):
    consonants = ''.join(sorted(alphabet - prechosen))
    return [set(prechosen) | set(c) for c in combinations(consonants, k - len(prechosen))]


if __name__ == '__main__':
    calculateAverageWordsReturnedIncremental(
        createWordTries(), getSampleWords(10000), prechosen)
    # print("GENERATING CHARACTER SETS....")
    # arr = []
    # for i in range(len(prechosen), 26):
    #     combs = generateKLengthCharacterSets(i, prechosen)
    #     print(i, len(combs))
    #     arr.append(combs)
    # print("GENERATED CHARACTER SETS....")
    # print("GENERATING TRIES")
    # # The set of all words in the wordlist in tries
    # allWordTries = createWordTries()
    # print("GENERATED TRIES")
    # # A selection of 10000 randomly chosen words from the wordlist
    # sampleWords = getSampleWords(10000)
    # print("CALCULATING AVERAGE POSITION OF WORD FOR CHARACTER SET...")
    # count = calculateAverageWordsReturnedT(arr, allWordTries, sampleWords, prechosen)[0]
    # print("COMPLETE")
