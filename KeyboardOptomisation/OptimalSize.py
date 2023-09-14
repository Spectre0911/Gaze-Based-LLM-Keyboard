import re
import random
import math
import Trie
from itertools import combinations
from constants import BASE_PATH

def get_random_word():
    """
    Gets a random word of random length.

    Returns:
        String: An english word of random length
    """
    random_word = ""
    wordLengths = [i for i in range(1, 19)]
    wordLength = random.choices(
        wordLengths, weights=getWordLengthProbability(), k=1)[0]
    with open(f"{BASE_PATH}{wordLength}_length.txt", 'r') as file:
        words = file.read().split()
        random_word = random.choice(words)
        random_word = random_word.split('.')[1]

    return random_word


def spellWord(word, characterSet):
    """
    Spells the word with the available characters in the character set

    Args:
        word (String): A word within the wordlist
        characterSet (Set): A set of characters representing the available characters on the keyboard

    Returns:
        _type_: _description_
    """
    normalisedWord = ""
    normalisedWord = "".join([c if c in characterSet else "_" for c in word])
    return normalisedWord


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



# [20697, 15943, 13391, 12029, 11202, 10676, 10376, 10199, 10089, 10038, 10013, 10008, 10000000, 10000000, 10000000]


def calculateAverageWordsReturnedT(characterSets):
    # This is the set of all letters in the alphabet
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    # The set of letters that have been prechosen
    prechosen = {'a', 'e', 'i', 'o', 'u', 't',
                 'n', 's', 'r', 'h', 'f', 'd', 'p', 'm'}
    # The letters that do not appear on the keyboard
    remainingAlphabet = alphabet - prechosen
    # The set of all words in the wordlist in tries
    allWordTries = createWordTries()
    # A selection of 10000 randomly chosen words from the wordlist
    sampleWords = getSampleWords(10000)
    # Holds 
    count = [10000000] * 15
    cSet = [None] * 15
    for j, kCharSet in enumerate(characterSets):
        print(j)
        # print(len(kCharSet))
        for characterSet in kCharSet:
            unknownCharacterSet = remainingAlphabet - characterSet
            tempCount = 0
            for word in sampleWords:
                wordLength = len(word)
                speltWord = spellWord(word, characterSet)
                tempCount += allWordTries[wordLength].searchR(
                    speltWord, unknownCharacterSet)[0][0]
            currentCount = count[j - 15]
            if tempCount < currentCount:
                count[j-15] = tempCount
                cSet[j-15] = characterSet

    # Maybe change this to calculate the average position within the returned list of words
    # print(count)
    [print(c) for c in cSet]
    return count


def getWordLengthProbability():
    total, distribution = getWordDistribution()
    return [count/total for count in distribution]


def getSampleWords(k):
    probs = getWordLengthProbability()
    sampleWords = []
    for i in range(1, 19):
        prop = math.ceil(probs[i-1] * k)
        with open(f"{BASE_PATH}{i}_length.txt", 'r') as file:
            words = file.read().split()
            samples = random.choices(words, k=prop)
            for i in samples:
                sampleWords.append(i)
    return sampleWords



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


def simulatedAnnealing(prechosen, initialMinCount):
    """
    Performs simulated annealing to find the best character set for a given word length.
    """

    count = initialMinCount
    minCharSet = prechosen
    for _ in range(10000):
        newCharSet = mutateChars(minCharSet)
        avgWords = calculateAverageWordsReturnedT([[newCharSet]])[0]
        prob = math.exp((count - avgWords) / 1000)
        if avgWords < count:
            count = avgWords
            minCharSet = newCharSet
            print(minCharSet)
            print(count)
    
        
def mutateChars(prechosen):
    """
    Update 1 character from the prechosen character set

    Args:
        prechosen (Set): The initial guess for optimal characters to be used in size 14 charset
    """

    newSet = prechosen
    allLetters = set('abcdefghijklmnopqrstuvwxyz')
    notPrechosen = allLetters - prechosen

    letterToChange = random.choice(list(prechosen))
    letterToChangeTo = random.choice(list(notPrechosen))

    newSet.remove(letterToChange)
    newSet.add(letterToChangeTo)

    return newSet


prechosen = {'a', 'e', 'i', 'o', 'u', 't',
                'n', 's', 'r', 'h', 'f', 'd', 'p', 'm'}
count = calculateAverageWordsReturnedT([[prechosen]])[0]


