def convert_to_lowercase(input_file_path, output_file_path):
    """Convert all text in the file to lowercase."""
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        processed_lines = [line.lower() for line in lines]

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(processed_lines)

        print("All text has been converted to lowercase.")

    except FileNotFoundError:
        print("The specified file does not exist.")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")


def analyse_text_data(input_file_path):
    """
    Analyses text data from a given file, providing statistics on word counts per line and distinct words.

    Parameters:
        input_file_path (str): Path to the text file.

    Prints statistics on average, maximum, and minimum words per line, and the number of distinct words.

    Handles FileNotFoundError for missing files and IOError for read errors.
    """
    try:
        # Open the text file with UTF-8 encoding to handle various character sets
        with open(input_file_path, 'r', encoding='utf-8') as file:
            # Read all lines from the file into a list
            lines = file.readlines()

        # Initialise counters and sets for various statistics
        total_words = 0
        max_words = 0
        # Start with infinity to find the minimum effectively
        min_words = float('inf')
        distinct_words = set()  # Use a set to count distinct words without duplicates

        # Process each line in the list of lines
        for line in lines:
            # Strip whitespace and split the line into words
            words = line.strip().split()
            # Count the number of words in the current line
            word_count = len(words)
            # Add to the total word count
            total_words += word_count
            # Add words to the set of distinct words
            distinct_words.update(words)

            # Update the maximum words in a line if the current count is higher
            if word_count > max_words:
                max_words = word_count

            # Update the minimum words in a line if the current count is lower and the line is not empty
            if word_count < min_words and word_count > 0:
                min_words = word_count

        # Calculate the average words per line, avoiding division by zero
        average_words = total_words / len(lines) if lines else 0
        # Ensure min_words is zero if no lines contained words (all were empty)
        min_words = min_words if min_words != float('inf') else 0

        # Output the calculated statistics
        print(f"Average words per line: {average_words:.2f}")
        print(f"Max words per line: {max_words}")
        print(f"Min words per line: {min_words}")
        print(f"Number of distinct words: {len(distinct_words)}")

    # Handle the case where the file path is incorrect or the file is missing
    except FileNotFoundError:
        print("The specified file does not exist.")
    # Handle other I/O errors, such as permission issues
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")


# Example usage
input_file = 'normalisedPhrases.txt'
# output_file = 'normalisedPhrases.txt'

analyse_text_data(input_file)
# process_text_file(input_file, output_file)
