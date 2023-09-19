from collections import defaultdict
from KeyboardCharacterOptomiser import createWordTries
from constants import BASE_PATH, alphabet

keyboards = [
    {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'd', 'e'},
    {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'd', 'e'},
    {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'd', 'e'},
    {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'b', 'd', 'e'},
    {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'b', 'd', 'e', 'h'},
    {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'b', 'd', 'e', 'g', 'h'},
    {'i', 'c', 'l', 'p', 'd', 'e', 'o', 'r', 'n', 'a', 's', 't', 'm', 'b', 'f', 'g', 'h'},
    {'i', 'c', 'w', 'l', 'p', 'd', 'e', 'o', 'r', 'n', 'a', 's', 't', 'm', 'b', 'f', 'g', 'h'},
]

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


def getKeyboardData(allWordTries, sampleWords):
    count = [10000000] * len(keyboards)
    cSet = [None] * len(keyboards)
    singleCount = [0] * len(keyboards)
    wordCountFrequency = [defaultdict(int) for _ in range(len(keyboards))]  # Initialize defaultdicts for each keyboard
    
    for j, keyboard in enumerate(keyboards):
        unknownCharacterSet = alphabet - keyboard
        tempCount = 0
        tempSingleWord = 0
        for word in sampleWords:
            wordLength = len(word)
            wordCount = allWordTries[wordLength].searchR(
                word, unknownCharacterSet, keyboard)[0][0]
            tempCount += wordCount
            
            if wordCount == 1:
                tempSingleWord += 1
            
            # Increment frequency of each wordCount value
            wordCountFrequency[j][wordCount] += 1

        if tempCount < count[j]:
            count[j] = tempCount 
            cSet[j] = keyboard
            singleCount[j] = tempSingleWord

    for i in range(len(count)):
        print(f"Keyboard {cSet[i]} has an average of {count[i]}")
        print(f"Freqs: {dict(wordCountFrequency[i])}")
        print("\n")

    return count

getKeyboardData(createWordTries(), getAllWords())