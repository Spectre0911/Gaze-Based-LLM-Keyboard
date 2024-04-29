import json
from constants import prechosen


def spellWord(word, K):
    """
    Processes a single word, replacing each character not in the set K with '%'.

    Args:
        word (str): The word to be processed.
        K (set): A set of characters that are allowed to appear in the processed word.

    Returns:
        str: The processed word where each character not in K is replaced with '%'.
    """
    # Initialise a string to store the normalised word
    normalisedWord = ""
    # Build the normalised word by retaining allowed characters or replacing others with '%'
    normalisedWord = "".join([c if c in K else "%" for c in word])
    # Return the normalised word
    return normalisedWord


def spellSentence(sentence):
    """
    Processes an entire sentence, replacing each word in the sentence with a spelt word.

    Args:
        sentence (str): The sentence to be processed.

    Returns:
        str: The fully processed sentence with words spelt according to allowed characters.
    """
    # Initialise a list to collect the processed words
    speltSentence = []
    # Split the sentence into words and process each word using spellWord
    for word in sentence.split():
        # Process each word and store the result
        nw = spellWord(word, prechosen)
        # Append the normalised word to the list
        speltSentence.append(nw)
    # Join the list of processed words back into a single string and return it
    return " ".join(speltSentence)


def process_file(input_file_path):
    """
    Reads a file line by line, processes each line as a sentence, and constructs
    a structured JSON representation for each line.

    Args:
        input_file_path (str): The path to the input file to be processed.

    Returns:
        None: Writes the structured data directly to a JSON file for use in fine-tuning.
    """
    # Initialise a list to store the structured conversations
    output_data = []
    # Open the input file for reading
    with open(input_file_path, "r") as file:
        # Process each line in the file
        for line in file:
            # Strip newline characters from the line
            sentence = line.strip()
            # Process the sentence to spell it using prechosen letters
            speltSentence = spellSentence(sentence)
            # Create a structured conversation object for the line
            conversation = {
                "messages": [
                    {"role": "system", "content": "You are playing a variation on hangman where you try to guess a sentence, YOU HAVE ALREADY GUESSED 'r', 'e', 'l', 'a', 't', 'i', 'o', 'n', 's' DO NOT REUSE ANY OF THEM."},
                    {"role": "user", "content": f"Current sentence: {speltSentence}. What do you think the sentence says? "},
                    {"role": "assistant", "content": f"Based on the sentence and the available letters, it appears that the sentence might say:  \"{sentence}\"."}
                ]
            }
            # Append the new conversation to the output list
            output_data.append(conversation)
    # Open a new file to write the JSON data
    with open("fineTuneReady.json", "w") as json_file:
        # Write each conversation to the file as a separate JSON object
        for conversation in output_data:
            json_file.write(json.dumps(conversation) + '\n')


process_file('Wordlist/normalisedPhrases.txt')

print(spellSentence("hello world"))
