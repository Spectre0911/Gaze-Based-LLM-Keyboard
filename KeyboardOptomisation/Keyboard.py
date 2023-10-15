import csv
from dotenv import load_dotenv
import os
from KeyboardCharacterOptomiser import createWordTries
from Trie import Trie
from constants import BASE_PATH, alphabet, prechosen
import csv
import openai

load_dotenv()


openai.api_key = os.getenv("GPT_API_KEY")


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
                          'SingleWordReplaced', 'SingleWordReplacedScore', 'Diff']
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writeheader()
            sentences = []

            for keyboard in keyboards:
                file.seek(0)
                for line in file:
                    words = line.strip().split()
                    word_count = len(words)
                    if word_count > 0:
                        speltWords = [trie.spellWord(
                            word, keyboard) for word in words]
                        replacedWords = []
                        for i in range(word_count):
                            replacedWord = singleWordReplacement(
                                " ".join(replacedWords), speltWords[i], keyboard, allWordTries, 5, words[i])
                            replacedWords.append(replacedWord)
                        speltSentence = " ".join(speltWords)
                        singleWordReplaced = " ".join(replacedWords)

                        speltSentenceScore = scoreSentence(
                            speltSentence, line) / word_count
                        singleWordReplacedScore = scoreSentence(
                            singleWordReplaced, line) / word_count

                        csvwriter.writerow({
                            'Original': line.strip(),
                            'SpeltSentence': speltSentence,
                            'SpeltSentenceScore': speltSentenceScore,
                            'SingleWordReplaced': singleWordReplaced,
                            'SingleWordReplacedScore': singleWordReplacedScore,
                            'Diff': singleWordReplacedScore - speltSentenceScore
                        })
                        sentences.append(speltSentence)

        return sentences
    except FileNotFoundError:
        print(f"File '{filename}' not found.")


def singleWordReplacement(context, speltWord, keyboard, allWordTries, threshold, actualWord="None"):
    searchRes = allWordTries[len(speltWord)].searchR(
        speltWord, alphabet - keyboard, keyboard)
    wordCount = searchRes[0][0]
    words = searchRes[1]
    if wordCount == 1:
        return words[0]
    elif wordCount <= threshold:
        print(f"UNDER THRESHOLD {context} {speltWord} {words}")
    return speltWord


def main():
    unknown = alphabet - prechosen
    print(unknown)
    allWordTries = createWordTries()
    spellSentences(f"{BASE_PATH}/sentences.txt", [prechosen], allWordTries)


if __name__ == "__main__":
    main()
