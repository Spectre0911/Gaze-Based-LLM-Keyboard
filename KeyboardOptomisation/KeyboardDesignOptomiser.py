import math
import string
import os

from constants import BASE_PATH
Qmap = {
    'Q': (0.00, 0), 'W': (1.00, 0), 'E': (2.00, 0), 'R': (3.00, 0), 'T': (4.00, 0), 'Y': (5.00, 0), 'U': (6.00, 0), 'I': (7.00, 0), 'O': (8.00, 0), 'P': (9.00, 0),
    'A': (0.25, 1), 'S': (1.25, 1), 'D': (2.25, 1), 'F': (3.25, 1), 'G': (4.25, 1), 'H': (5.25, 1), 'J': (6.25, 1), 'K': (7.25, 1), 'L': (8.25, 1),
    'Z': (0.50, 2), 'X': (1.50, 2), 'C': (2.50, 2), 'V': (3.50, 2), 'B': (4.50, 2), 'N': (5.50, 2), 'M': (6.50, 2)
}


def Kdist(A, B):
    a = A.upper()
    b = B.upper()
    return math.sqrt((Qmap[a][0] - Qmap[b][0])**2 + (Qmap[a][1] - Qmap[b][1])**2)


def avgKDist(word):
    dist = 0
    for i in range(len(word)-1):
        dist += Kdist(word[i], word[i+1])
    return (dist / len(word))


def avgBDistance(filename):
    """Opens a file, parses it, and prints every word without trailing special characters."""
    avg = 0
    wordCount = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
                for word in words:
                    word = word.rstrip(string.punctuation)

                    if word:
                        wordCount += 1
                        avg += avgKDist(word)

            print(avg / wordCount)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")


filename = f"{BASE_PATH}/google-10000-english-usa.txt"
avgBDistance(filename)
