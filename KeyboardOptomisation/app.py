from flask import Flask, jsonify, request
from flask_cors import CORS

from KeyboardCharacterOptomiser import createWordFrequencyMap, createWordTries
from keyboardTests import gptWrapper
from constants import prechosen, alphabet

app = Flask(__name__)
CORS(app)


alphabet = set('abcdefghijklmnopqrstuvwxyz')
allWordTries = createWordTries()
frequencyMaps = createWordFrequencyMap()


@app.route('/api/onSpace', methods=['POST'])
def onSpace():
    data = request.json

    print(data)
    currentWord = data["currentWord"].lower()
    currentSentence = data["currentSentence"].lower()
    print(f"EXTRACTED {currentWord}")
    wordTrie = allWordTries[len(currentWord)]
    alternatives = wordTrie.searchR(
        currentWord, alphabet - prechosen, prechosen)[1]
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

    print(f"{replacedWord}")
    return jsonify(replacedWord.upper(), alternatives)


@app.route('/api/onPeriod', methods=['POST'])
def onPeriod():
    data = request.json
    sentence = data["sentence"]
    gptSentence = gptWrapper(sentence)
    print(f"GPT ONPERIOD: {gptSentence}")
    return jsonify(gptSentence)


if __name__ == '__main__':
    app.run(debug=True)
