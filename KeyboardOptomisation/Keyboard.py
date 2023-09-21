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
        with open(filename, 'r') as file, open('singleWordReplacementImprovement.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Original', 'SpeltSentence', 'SpeltSentenceScore', 'SingleWordReplaced', 'SingleWordReplacedScore', 'Diff'])  # Header
            sentences = []
            for keyboard in keyboards:
                file.seek(0)
                for line in file:
                    speltWords = []
                    words = line.strip().split()
                    for word in words:
                        speltWord = Trie().spellWord(word, keyboard)
                        speltWords.append(speltWord)
                    if len(words) > 0:
                        speltSentence = " ".join(speltWords)
                        sentences.append(speltSentence)
                        singleWordReplaced = singleWordReplacement(speltSentence, keyboard, allWordTries)
                        speltSentenceScore = scoreSentence(speltSentence, line)
                        singleWordReplacedScore = scoreSentence(singleWordReplaced, line)
                        
                        # Write to CSV
                        speltSentenceScoreAvg = speltSentenceScore/len(words)
                        singleWordReplacedScoreAvg = singleWordReplacedScore/len(words)
                        csvwriter.writerow([line.strip(), speltSentence, speltSentenceScoreAvg, singleWordReplaced, singleWordReplacedScoreAvg, singleWordReplacedScoreAvg - speltSentenceScoreAvg])
                        
                        print(f"O- {line.strip()}\nS- {speltSentence}\nR- {singleWordReplaced}\nDiff: {singleWordReplacedScoreAvg - speltSentenceScoreAvg}\n")
                    
            return sentences
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

        
def singleWordReplacement(speltSentence, keyboard, allWordTries):
    newWords = []
    words = speltSentence.strip().split()
    for word in words:
        searchRes = allWordTries[len(word)].searchR(word, alphabet - keyboard, keyboard)
        wordCount = searchRes[0][0]
        words = searchRes[1]
        if wordCount == 1:

            newWords.append(words[0])
        else:
            newWords.append(word)
    newSentence = " ".join(newWords)
    return newSentence
  
                    
def main():
    allWordTries = createWordTries()
    spellSentences(f"{BASE_PATH}/sentences.txt", [prechosen], allWordTries)
    
if __name__ == "__main__":
    main()