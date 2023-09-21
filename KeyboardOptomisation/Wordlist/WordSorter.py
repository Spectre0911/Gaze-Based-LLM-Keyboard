import nltk
nltk.download('words')
from nltk.corpus import words
import re

def process_words(filename):
    word_sets = {}  # Dictionary to hold sets for each k-length word
    with open(filename, 'r') as file:
        words = file.read().split()
    
    english_alphabet_pattern = re.compile(r'^[a-zA-Z]+$')
    
    with open("all-normalized-words.txt", 'a') as all_words_file:  # Open the file for writing all normalized words
        for index, word in enumerate(words):
            k = len(word)
            if word.startswith('#!comment:') or word.startswith('http') or word.startswith('-') or k > 18 or not english_alphabet_pattern.match(word):
                continue

            word = word.lower()
            output_filename = f"{k}_length.txt"

            # Initialize set for k-length words if not already present
            if k not in word_sets:
                word_sets[k] = set()

            # Skip duplicate words
            if word in word_sets[k]:
                print(f"Skipping duplicate word: {word}")
                continue

            # Add word to set and write to file
            word_sets[k].add(word)
            with open(output_filename, 'a') as output_file:
                output_file.write(f"{word}\n")
            
            # Write the word to all-normalized-words.txt
            all_words_file.write(f"{word}\n")

    print("Processing complete!")

process_words("wiki-100k.txt")
