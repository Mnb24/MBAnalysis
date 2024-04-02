import streamlit as st
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.text import Text
import requests
import nltk

# Download nltk resources
nltk.download('punkt')

def get_context_paragraphs(text, target_word, context_lines=2):
    sentences = sent_tokenize(text)
    paragraphs = []

    # Find sentences containing the target word
    for i, sentence in enumerate(sentences):
        if target_word in word_tokenize(sentence):
            start_index = max(0, i - context_lines)
            end_index = min(len(sentences), i + context_lines + 1)
            context_sentences = sentences[start_index:end_index]
            context_paragraph = " ".join(context_sentences)
            paragraphs.append(context_paragraph)

    return paragraphs

def perform_concordance(texts, target_word):
    # Initialize concordance lists for each text
    concordance_lists = []
    file_names = ['BD', 'KMG', 'MND']
    for text, file_name in zip(texts, file_names):
        tokens = word_tokenize(text)
        text_object = Text(tokens)
        concordance_lists.append((text_object.concordance_list(target_word), file_name))

    # Initialize counters for each text file
    counters = [0] * len(concordance_lists)
    
    # Iterate through occurrences until we have processed all occurrences
    processed_occurrences = 0
    while True:
        for i, (concordance_list, file_name) in enumerate(concordance_lists):
            if counters[i] < len(concordance_list):
                entry = concordance_list[counters[i]]
                left_context = " ".join(entry.left)
                right_context = " ".join(entry.right)
                line_number = text.count('\n', 0, entry.offset) + 1  # Calculate line number

                # Highlight the target word with a color
                highlighted_text = f"{left_context} <span style='color: red'>{target_word}</span> {right_context}"
                st.write(f"Line {line_number} ({file_name}): {highlighted_text}", unsafe_allow_html=True)

                counters[i] += 1
                processed_occurrences += 1

                if processed_occurrences % 3 == 0:
                    st.write("***")

                if processed_occurrences % 3 == 0:
                    st.write("\n\n")
                
                if all(counter >= len(concordance_list) for counter, (concordance_list, _) in zip(counters, concordance_lists)):
                    return

def main():
    st.title("Concordance Analyzer - Adi Parva")
    # URLs of the text files
    file_paths = [
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
    ]

    texts = []
    for file_path in file_paths:
        response = requests.get(file_path)
        texts.append(response.text)

    target_word = st.text_input("Enter the word for concordance analysis: ")

    if st.button('Perform Concordance Analysis'):
        perform_concordance(texts, target_word)

if __name__ == "__main__":
    main()

