import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.text import Text
import requests

# Download NLTK resources
nltk.download('punkt')

def perform_concordance(text, target_word):
    tokens = word_tokenize(text)
    text_object = Text(tokens)

    st.write(f"\nConcordance Analysis for '{target_word}':")
    concordance_results = text_object.concordance_list(target_word)

    # Print concordance results with line numbers
    for entry in concordance_results:
        left_context = " ".join(entry.left)
        right_context = " ".join(entry.right)
        line_number = text.count('\n', 0, entry.offset) + 1  # Calculate line number

        st.write(f"Line {line_number}: {left_context} {target_word} {right_context}")

def main():
    # URLs of the text files
    file_paths = [
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
    ]
    text_names = ['BD1', 'MND1', 'KMG1']

    target_word = st.text_input("Enter the word for concordance analysis: ")

    if st.button('Perform Concordance Analysis'):
        for file_path, text_name in zip(file_paths, text_names):
            response = requests.get(file_path)
            text = response.text
            st.write(f"\nConcordance Analysis for {text_name}:")
            perform_concordance(text, target_word)

if __name__ == "__main__":
    main()


