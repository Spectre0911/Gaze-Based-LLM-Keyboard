def process_words(filename):
    with open(filename, 'r') as file:
        words = file.read().split()

    # Loop through each word
    for index, word in enumerate(words):
        k = len(word)
        # Ignore lines starting with "#!comment:"
        if word.startswith('#!comment:') or word.startswith('http') or word.startswith('-') or k > 18 or not word.isalpha():
            continue

        output_filename = f"KeyboardOptomisation/Wordlist/{k}_length.txt"

        # Open the output file in append mode
        with open(output_filename, 'a') as output_file:
            output_file.write(f"{index}.{word.lower()}" + '\n')

    print("Processing complete!")


process_words('KeyboardOptomisation/Wordlist/wiki-100k.txt')
