from itertools import combinations
from constants import alphabet, prechosen, BASE_PATH
import random
import math
import Trie

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

def calculateAverageWordsReturnedT(characterSets, allWordTries, sampleWords, prechosen):
    # The letters that do not appear on the keyboard
    remainingAlphabet = alphabet - prechosen
    # Keeps track of the average number of words returned for the each optimal character set
    count = [10000000] * len(characterSets) 
    # Keeps track of the optimal character set 
    cSet = [None] * len(characterSets) 
    
    for j, kCharSet in enumerate(characterSets):
        print(j)
        for characterSet in kCharSet:
            unknownCharacterSet = remainingAlphabet - characterSet
            tempCount = 0
            for word in sampleWords:
                wordLength = len(word)
                tempCount += allWordTries[wordLength].searchR(
                    word, unknownCharacterSet, characterSet)[0][0]
            currentCount = count[j]
            if tempCount < currentCount:
                count[j] = tempCount 
                cSet[j] = characterSet

    # print("----------")
    for i in range(len(count)):
        print(f"Keyboard {cSet[i]} has an average of {count[i]} words returned")
    return count

def createWordTries():
    """
    Creates tries of words for different word lengths.

    Returns:
        dict: A dictionary containing trie objects for different word lengths.
            The keys are the word lengths, and the values are the corresponding trie objects.
    """
    trie_dict = {}

    for i in range(1, 19):
        trie_dict[i] = Trie.Trie()

    for i in range(1, 19):
        with open(f"{BASE_PATH}{i}_length.txt", 'r') as file:
            words = file.read().split()
            for word in words:
                trie_dict[i].insert(word)

    return trie_dict

def calculateAverageWordsReturnedIncremental( allWordTries, sampleWords, prechosen):
    initialLength = len(prechosen)
    # The letters that do not appear on the keyboard
    remainingAlphabet = alphabet - prechosen
    # Keeps track of the average number of words returned for the each optimal character set
    count = [10000000] * 26
    # Keeps track of the optimal character set 
    cSet = [None] * 26
    singleCount = [0] * 26
        
    for j in range(len(prechosen), 26):
        print("Here")
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
        print(f"Keyboard {cSet[i]} has an average of {count[i]} words returned where only 1 word was returned {singleCount[i]} times")
    return count



def generateKLengthCharacterSets(k, prechosen):
    consonants = ''.join(sorted(alphabet - prechosen))
    return [set(prechosen) | set(c) for c in combinations(consonants, k - len(prechosen))]

if __name__ == '__main__':
    calculateAverageWordsReturnedIncremental(createWordTries(), getSampleWords(10000), prechosen)
    # print("GENERATING CHARACTER SETS....")
    # arr = []
    # for i in range(len(prechosen), 26):
    #     combs = generateKLengthCharacterSets(i)
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
 


