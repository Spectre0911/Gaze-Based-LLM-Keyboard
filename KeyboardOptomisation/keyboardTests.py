import csv
# from dotenv import load_dotenv
import os
from KeyboardCharacterOptomiser import createWordFrequencyMap, createWordTries
from Trie import Trie
from constants import BASE_PATH, alphabet, prechosen
import csv
from openai import OpenAI

client = OpenAI()
frequencyMaps = createWordFrequencyMap()


def scoreSentence(returnedSentence, actualSentence):
    gptWords = returnedSentence.split()
    actualWords = actualSentence.split()
    score = 0

    for gWord, aWord in zip(gptWords, actualWords):
        if gWord == aWord:
            score += 1

    return score


def spellSentences(filename, keyboards, allWordTries):
    try:
        trie = Trie()
        with open(filename, 'r') as file, open('singleWordReplacementImprovement.csv', 'w', newline='') as csvfile:
            fieldnames = ['Original', 'SpeltSentence', 'SpeltSentenceScore',
                          'SingleWordReplaced', 'SingleWordReplacedScore', 'GPT', 'GPTScore']
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writeheader()
            sentences = []

            for keyboard in keyboards:
                file.seek(0)
                for line in file:
                    words = line.strip().split()
                    wordCount = len(words)
                    if wordCount > 0:
                        speltSentence, singleWordReplaced = spellSentence(
                            allWordTries, trie, keyboard, words, wordCount)

                        speltSentenceScore = scoreSentence(
                            speltSentence, line) / wordCount

                        singleWordReplacedScore = scoreSentence(
                            singleWordReplaced, line) / wordCount

                        gptSentence = gptWrapper(
                            singleWordReplaced, allWordTries)
                        gptScore = scoreSentence(gptSentence, line) / wordCount

                        csvwriter.writerow({
                            'Original': line.strip(),
                            'SpeltSentence': speltSentence,
                            'SpeltSentenceScore': speltSentenceScore,
                            'SingleWordReplaced': singleWordReplaced,
                            'SingleWordReplacedScore': singleWordReplacedScore,
                            'GPT': gptSentence,
                            'GPTScore': gptScore,
                        })
                        sentences.append(speltSentence)

        return sentences
    except FileNotFoundError:
        print(f"File '{filename}' not found.")


def spellSentence(allWordTries, trie, keyboard, words, wordCount):
    speltWords = [trie.spellWord(word, keyboard) for word in words]
    replacedWords = []
    for i in range(wordCount):
        wordTrie = allWordTries[len(speltWords[i])]
        replacedWord = wordTrie.singleWordReplacement(
            speltWords[i], keyboard)
        replacedWords.append(replacedWord[0])
    speltSentence = " ".join(speltWords)
    singleWordReplaced = " ".join(replacedWords)
    return speltSentence, singleWordReplaced


def compareWords(tuples, keyboard):
    newTuples = []
    for (w1, w2) in tuples:
        w1 = w1.lower()
        w2 = w2.lower()

        match = True
        i = 0

        if len(w1) != len(w2):
            match = False

        while match and i < len(w1):
            wildcardPresent = w2[i] == "%"
            gptCharacterNotPossible = w1[i] in keyboard
            if wildcardPresent and gptCharacterNotPossible:
                match = False
            elif not wildcardPresent:
                if w1[i] != w2[i]:
                    match = False
            i += 1

        newTuples.append((w1, match))
    return newTuples


def gptReplacedSentence(sentence):
    #  gpt-3.5-turbo-1106
    response = client.chat.completions.create(model="gpt-4-0125-preview",
                                              messages=[
                                                  {"role": "system", "content": "You are playing a variation on hangman where you try to guess a sentence, YOU HAVE ALREADY GUESSED 'a', 'd', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't'} DO NOT REUSE ANY OF THEM"},
                                                  {"role": "user", "content": "Current sentence: %is stand %% routine %as hilarious i %as laughing so %ard i almost %ried.  What do you think the sentence says? Take a deep breath and think about it."},
                                                  {"role": "assistant", "content": "Based on the sentence and the available letters, it appears that the sentence might say: \"His stand-up routine was hilarious; I was laughing so hard I almost cried.\""},
                                                  {"role": "user",
                                                      "content": f"Current sentence: {sentence}"},

                                              ])
    response = response.choices[0].message.content
    first_quote_index = response.find('"')
    last_quote_index = response.find(
        '.')
    sentenceString = response[first_quote_index + 1: last_quote_index]
    # Remove all punctuation
    normalisedString = ''.join(
        char for char in sentenceString if (char.isalpha() or char.isspace()))
    extracted = normalisedString
    extractedWords = extracted.split()

    sentenceWords = sentence.split()

    zippedWords = list(zip(extractedWords, sentenceWords))
    reversedZippedWords = list(zip(extractedWords[::-1], sentenceWords[::-1]))

    forwardPass = compareWords(zippedWords, prechosen)
    backPass = compareWords(reversedZippedWords, prechosen)

    newSentence = sentence.split()
    for index, (w1, match) in enumerate(forwardPass):
        if match:
            newSentence[index] = w1
    for index, (w1,  match) in enumerate(backPass):
        if match:
            newSentence[-index - 1] = w1
    newSentenceString = " ".join(newSentence)
    return (newSentenceString)


allWordTries = createWordTries()


def gptWrapper(sentence, allWordTries=allWordTries):
    i = 0
    while i < 2 and "%" in sentence:
        sentence = gptReplacedSentence(sentence)
        i += 1
    if "%" in sentence:
        sentence = sentence.split()
        for index, word in enumerate(sentence):
            if "%" in word:
                freqMap = frequencyMaps[len(word)]
                alternatives = allWordTries[len(word)].searchR(
                    word, prechosen)[1]
                alternatives = sorted(
                    alternatives, key=lambda x: freqMap[x])
                if len(alternatives) > 0:
                    sentence[index] = alternatives[0]

        sentence = " ".join(sentence)
    return sentence


def main():
    allWordTries = createWordTries()
    spellSentences(f"{BASE_PATH}userGenerated.txt",
                   [prechosen], allWordTries)


if __name__ == "__main__":
    main()
