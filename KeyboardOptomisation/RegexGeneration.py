import re


def regexGenerator(word, A, B):
    regex = ""
    diff = A - B
    for c in word:
        if c in A:
            regex += c
        else:
            regex += "{diff}"
