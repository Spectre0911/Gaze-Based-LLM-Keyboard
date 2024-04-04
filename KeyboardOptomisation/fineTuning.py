import json
from constants import prechosen


def spellWord(word, characterSet):

    normalisedWord = ""
    normalisedWord = "".join(
        [c if c in characterSet else "%" for c in word])
    return normalisedWord


def spellSentence(sentence):
    speltSentence = []
    for word in sentence.split():
        nw = spellWord(word, prechosen)
        speltSentence.append(nw)
    return " ".join(speltSentence)


def process_file(input_file_path):
    output_data = []  # This will be a list of conversations

    with open(input_file_path, "r") as file:
        for line in file:
            sentence = line.strip()
            speltSentence = spellSentence(sentence)

            # Create a new conversation for each line
            conversation = {
                "messages": [
                    {"role": "system", "content": "You are playing a variation on hangman where you try to guess a sentence, YOU HAVE ALREADY GUESSED 'a', 't', 'r', 'l', 'e', 's', 'o', 'n' DO NOT REUSE ANY OF THEM"},
                    {"role": "user", "content": f"Current sentence: {speltSentence}"},
                    {"role": "assistant", "content": f"Based on the sentence and the available letters, it appears that the sentence might say:  \"{sentence}\" "}
                ]
            }

            # Append the new conversation to the list of conversations
            output_data.append(conversation)

    # Writing the structured data to a JSON file
    with open("fineTuneReady.json", "w") as json_file:
        # Ensure each conversation object is written to the file as a separate line for GPT fine-tuning
        for conversation in output_data:
            json_file.write(json.dumps(conversation) + '\n')


process_file('Wordlist/trainingSentences.txt')

print(spellSentence("hello world"))
