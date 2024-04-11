from flask import Flask, jsonify, request
import google.generativeai as genai
from flask_cors import CORS
import csv
import os

from KeyboardCharacterOptomiser import createWordFrequencyMap, createWordTries
from GPTAlgorithm import gptWrapper
from constants import prechosen, alphabet

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

alphabet = set('abcdefghijklmnopqrstuvwxyz')
allWordTries = createWordTries()
frequencyMaps = createWordFrequencyMap()


@app.route('/api/onSpace', methods=['POST'])
def onSpace():
    data = request.json
    # Get the current word
    currentWord = data["currentWord"].lower()
    # Get the words of that length
    wordTrie = allWordTries[len(currentWord)]
    # Get all possible words, that match the spelt word
    alternatives = wordTrie.searchR(
        currentWord, prechosen)[1]
    # Check if single word replacement is possible
    replacedWord, replaced = wordTrie.singleWordReplacement(
        currentWord, prechosen)
    if replaced == False:
        freqMap = frequencyMaps[len(currentWord)]
        alternatives = sorted(
            alternatives, key=lambda x: freqMap[x])
        if len(alternatives) > 0:
            replacedWord = alternatives[0]
        else:
            # Need to add some additional functionality here to handle the case where the word is not in wordlist
            pass

    return jsonify(replacedWord.upper(), alternatives)


@app.route('/api/onPeriod', methods=['POST'])
def onPeriod():
    data = request.json
    sentence = data["sentence"]
    duration = data["duration"]
    trialMode = data["trialMode"]
    correctionsMade = data["correctionsMade"]
    gptSentence = sentence
    print(sentence)
    if not trialMode:
        gptSentence = gptWrapper(sentence)
    else:
        trialSentence = data["trialSentence"]
        trialWords = trialSentence.split(" ")
        sentenceWords = sentence.split(" ")
        # Initialise counters for correct matches and total letters
        correct_matches = 0
        # Total letters in trialWords
        total_letters = sum(len(word) for word in trialWords)
        # Iterate over each word pair
        for trialWord, sentenceWord in zip(trialWords, sentenceWords):
            sentenceWord = sentenceWord.lower()
            trialWord = trialWord.lower()
            # Iterate over each letter in the words, up to the length of the shorter word
            for trialLetter, sentenceLetter in zip(trialWord, sentenceWord):
                if trialLetter == sentenceLetter or trialLetter not in prechosen and sentenceLetter == "%":
                    correct_matches += 1

        # Calculate letter-level accuracy
        letter_accuracy = correct_matches / total_letters
        print(f"SENTENCE ACCURACY: {letter_accuracy}")
    print(f"Corrections made: {correctionsMade}")
    print(f"DURATION: {duration}")
    return jsonify(gptSentence)


@app.route('/api/logCalibration', methods=['POST'])
def log_calibration():
    data = request.json
    mode = data[0]['mode']
    file_path = f"data/calibration_{mode}_log.csv"
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Round', 'Average', 'Calibration'])

        for item in data:
            writer.writerow(
                [item['round'], item['average'], item['calibration']])

    return jsonify({"message": "Data logged successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
