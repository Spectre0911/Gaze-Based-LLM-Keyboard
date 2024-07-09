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
    prechosenStr = str(prechosen)[1:-1]
    messagestt = [
        {"role": "system", "content": f"You are playing a variation on hangman where you try to guess a sentence, YOU HAVE ALREADY GUESSED {prechosenStr} DO NOT REUSE ANY OF THEM"},
        {"role": "user", "content": "Current sentence: %is stand %% routine %as hilarious i %as laughing so %ard i almost %ried.  What do you think the sentence says? Take a deep breath and work on this problem step-by-step."},
        {"role": "assistant", "content": "Based on the sentence and the available letters, it appears that the sentence might say: \"his stand-up routine was hilarious; i was laughing so hard i almost cried.\""},
        {"role": "user",
         "content": f"Current sentence: {sentence}. What do you think the sentence says? Take a deep breath and work on this problem step-by-step."},
    ]

    messagesntt = [
        {"role": "system", "content": f"You are playing a variation on hangman where you try to guess a sentence, YOU HAVE ALREADY GUESSED {prechosenStr} DO NOT REUSE ANY OF THEM. "},
        {"role": "user", "content": "Current sentence: %is stand %% routine %as hilarious i %as laughing so %ard i almost %ried.  What do you think the sentence says?"},
        {"role": "assistant", "content": "Based on the sentence and the available letters, it appears that the sentence might say: \"His stand-up routine was hilarious; I was laughing so hard I almost cried.\""},
        {"role": "user",
         "content": f"Current sentence: {sentence}"},
    ]
    ftMessages = [
        {"role": "system", "content": f"You are playing a variation on hangman where you try to guess a sentence, YOU HAVE ALREADY GUESSED 'r', 'e', 'l', 'a', 't', 'i', 'o', 'n', 's' DO NOT REUSE ANY OF THEM"},
        {"role": "user", "content": f"Current sentence: {sentence}. What do you think the sentence says?"}]

    firstMessage = [{"role": "user", "content": "{sentence}, replace % to make sentence coherent"},
                    ]

    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:momo:ms-relations:9G5YVIyT", messages=ftMessages)

    response = response.choices[0].message.content
    normalisedString = extractSentence(response)

    newSentence = matchWords(sentence, normalisedString)
    newSentenceString = " ".join(newSentence)

    return (newSentenceString)


def extractSentence(response):
    """
    Extract and normalise a substring from 'response' between the first quote and the first period.
`
    Args:
    - response (str): The string to process.

    Returns:
    - str: Normalised substring containing only alphabetic characters and spaces.
    """
    # Find the index of the first double quote in the string
    first_quote_index = response.find('"')
    # Find the index of the first period in the string
    last_quote_index = response.find('.')
    # Extract the substring from after the first quote to just before the first period
    sentence_string = response[first_quote_index + 1: last_quote_index]

    # Normalise the extracted substring by keeping only alphabetic characters and spaces
    normalised_string = ''.join(
        char for char in sentence_string if (char.isalpha() or char.isspace())
    )

    # Return the normalised string
    return normalised_string


def matchWords(sentence, normalisedString):
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
    return newSentence


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
                wordLength = len(word)
                freqMap = frequencyMaps[wordLength]
                alternatives = allWordTries[wordLength].searchR(
                    word.lower(), prechosen)[1]
                alternatives = sorted(
                    alternatives, key=lambda x: freqMap[x])
                if len(alternatives) > 0:
                    sentence[index] = alternatives[0]

        sentence = " ".join(sentence)
    return sentence


def main():
    allWordTries = createWordTries()
    spellSentences(f"{BASE_PATH}sentences.txt",
                   [prechosen], allWordTries)


if __name__ == "__main__":
    main()
