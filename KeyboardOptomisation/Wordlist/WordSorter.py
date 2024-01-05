import re


def process_words(filename):
    count = 0
    word_sets = {}  # Dictionary to hold sets for each k-length word
    with open(filename, 'r') as file:
        words = file.read().split()

    english_alphabet_pattern = re.compile(r'^[a-zA-Z]+$')

    # Open the file for writing all normalized words
    with open("all-normalized-words.txt", 'a') as all_words_file:
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
                continue

            # Add word to set and write to file
            word_sets[k].add(word)
            with open(output_filename, 'a') as output_file:
                count += 1
                output_file.write(f"{word}\n")

            # Write the word to all-normalized-words.txt
            all_words_file.write(f"{word}\n")
    print(count)
    print("Processing complete!")


process_words("wiki-100k.txt")
