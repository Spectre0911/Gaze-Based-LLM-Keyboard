import string
from dotenv import load_dotenv
import os
from Trie import Trie  
from constants import BASE_PATH, alphabet
import requests
import json
import csv
import openai

load_dotenv()


openai.api_key = os.getenv("GPT_API_KEY")
keyboards = [
    {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'd', 'e'},
    # {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'd', 'e'},
    # {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'd', 'e'},
    # {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'b', 'd', 'e'},
    # {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'b', 'd', 'e', 'h'},
    # {'o', 'r', 'n', 'a', 'i', 'c', 't', 's', 'l', 'm', 'p', 'b', 'd', 'e', 'g', 'h'},
    # {'i', 'c', 'l', 'p', 'd', 'e', 'o', 'r', 'n', 'a', 's', 't', 'm', 'b', 'f', 'g', 'h'},
    # {'i', 'c', 'w', 'l', 'p', 'd', 'e', 'o', 'r', 'n', 'a', 's', 't', 'm', 'b', 'f', 'g', 'h'},
]

def process_text(sentence):
    # Remove punctuation
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    # Convert to lower case
    sentence = sentence.lower()
    return sentence

def decodeSentence(speltSentence, unknownChars):
    data = {
        "role": "user",
        "content": f"Spelt sentence: {speltSentence}, Unknown {unknownChars} What is sentence? Think first and preface sentence with Decoded:",
    }
    result = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[data])
    if 'choices' in result and len(result['choices']) > 0:
        resultContent = result['choices'][0]['message']["content"].strip().split(":")[1].lstrip()
        processedContent = process_text(resultContent)
        
        return processedContent
    else:
        return "No response from API."
    

    

def scoreSentence(gptSentence, actualSentence):
    gptWords = gptSentence.split()
    actualWords = actualSentence.split()
    score = 0
    
    for gWord, aWord in zip(gptWords, actualWords):
        if gWord == aWord:
            score += 1
            
    return score

def spellSentences(filename, keyboards):
    try:
        with open(filename, 'r') as file, open("Keyboard11Results.csv", 'w', newline='') as result_file:
            csv_writer = csv.writer(result_file)
            csv_writer.writerow(["Spelt Sentence", "GPT Sentence", "Actual Sentence", "Score", "Average"])
            
            for keyboard in keyboards:
                file.seek(0)
                for line in file:
                    speltWords = []
                    words = line.strip().split()
                    for word in words:
                        speltWord = Trie().spellWord(word, keyboard)
                        speltWords.append(speltWord)
                    speltSentence = " ".join(speltWords)
                    unknownChars = str(set(alphabet) - set(keyboard))
                    gpt_sentence = decodeSentence(speltSentence, unknownChars)
                    score = scoreSentence(gpt_sentence, line.strip())
                    
                    csv_writer.writerow([speltSentence, gpt_sentence, line.strip(), score, score/len(line.strip().split())])
                    
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        
# filename = f"{BASE_PATH}/sentences.txt"
# spellSentences(filename, keyboards)

def calculate_average_score(filename):
    total_score = 0
    num_rows = 0
    
    with open(filename, 'r') as result_file:
        csv_reader = csv.DictReader(result_file)
        
        for row in csv_reader:
            total_score += float(row['Average'])
            num_rows += 1
    
    if num_rows == 0:
        return 0
    
    return total_score / num_rows

# Example usage
filename = "Keyboard11Results.csv"
averageScore = calculate_average_score(filename)
print(f"{averageScore}")