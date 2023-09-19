from constants import BASE_PATH
import re


def process_words(filename):
    with open(filename, 'r') as file:
        words = file.read().split()
    english_alphabet_pattern = re.compile(r'^[a-zA-Z]+$')
    # Loop through each word
    for index, word in enumerate(words):
        k = len(word)
        # Ignore lines starting with "#!comment:"
        if word.startswith('#!comment:') or word.startswith('http') or word.startswith('-') or k > 18 or not english_alphabet_pattern.match(word):
            continue

        output_filename = f"{k}_length.txt"

        # Open the output file in append mode
        with open(output_filename, 'a') as output_file:
            output_file.write(f"{word.lower()}" + '\n')

    print("Processing complete!")


process_words(f"{BASE_PATH}/wiki-100k.txt")
