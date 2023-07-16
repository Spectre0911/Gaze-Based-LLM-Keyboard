def process_words(filename):
    with open(filename, 'r') as file:
        words = file.read().split()

    # Loop through each word
    for word in words:
        k = len(word)
        output_filename = f"{k}_length.txt"

        # Open the output file in append mode
        with open(output_filename, 'a') as output_file:
            output_file.write(word + '\n')

    print("Processing complete!")


process_words('KeyboardOptomisation/Wordlist/google-10000-english-usa.txt')
