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
                    wordCount = len(words)
                    if wordCount > 0:
                        speltSentence, singleWordReplaced = spellSentence(
                            allWordTries, trie, keyboard, words, wordCount)

                        speltSentenceScore = scoreSentence(
                            speltSentence, line) / wordCount
                        singleWordReplacedScore = scoreSentence(
                            singleWordReplaced, line) / wordCount

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


def singleWordReplacement(speltWord, keyboard, wordTrie):
    searchRes = wordTrie.searchR(
        speltWord, alphabet - keyboard, keyboard)
    wordCount = searchRes[0][0]
    words = searchRes[1]
    if wordCount == 1:
        return words[0]
    return speltWord


def spellSentence(allWordTries, trie, keyboard, words, wordCount):
    speltWords = [trie.spellWord(word, keyboard) for word in words]
    replacedWords = []
    for i in range(wordCount):
        wordTrie = allWordTries[len(speltWords[i])]
        replacedWord = wordTrie.singleWordReplacement(
            speltWords[i], keyboard)
        # replacedWord = singleWordReplacement(
        #     speltWords[i], keyboard, wordTrie)
        replacedWords.append(replacedWord)
    speltSentence = " ".join(speltWords)
    singleWordReplaced = " ".join(replacedWords)
    return speltSentence, singleWordReplaced


def gptReplacedSentence(sentence):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are playing a variation on hangman where you try to guess a sentence and you only have one more guess. "},
            {"role": "user", "content": "Current sentence: %is stand %% routine %as hilarious i %as laughing so %ard i almost %ried. You have yet to guess from this set: {'v', 'x', 'b', 'y', 'c', 'j', 'f', 'w', 'u', 'q', 'z', 'h', 'p', 'k'}. What do you think the sentence says? Take a deep breath and think about it."},
            {"role": "assistant", "content": "Based on the sentence and the available letters, it appears that the sentence might say: \"His stand-up routine was hilarious; I was laughing so hard I almost cried.\" The words \"His,\" \"stand-up,\" \"was,\" \"I,\" and \"cried\" seem to fit in the context of the sentence, and the remaining letters are not needed to complete this sentence."},
            {"role": "user", "content": f"Current sentence: {sentence}"},
        ]
    )
    print(response)


def main():
    gptReplacedSentence(
        "%ars boomed %% on t%e %ig%%a%ea%% one a capsule o% individual li%es and stories %et to %e told")
    # unknown = alphabet - prechosen
    # print(unknown)
    # allWordTries = createWordTries()
    # spellSentences(f"{BASE_PATH}/sentences.txt", [prechosen], allWordTries)


if __name__ == "__main__":
    main()
