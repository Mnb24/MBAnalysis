import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.text import Text
import requests
import nltk

# Download nltk resources
nltk.download('punkt')

def perform_concordance(text, target_word):
    tokens = word_tokenize(text)
    text_object = Text(tokens)

    st.write(f"\nConcordance Analysis for '{target_word}':")
    concordance_results = text_object.concordance_list(target_word)

    # Print concordance results with context
    for entry in concordance_results:
        # Get line number and contexts
        line_number = text.count('\n', 0, entry.offset) + 1  # Calculate line number
        lines = text.split('\n')
        prev_line = lines[line_number - 2] if line_number > 1 else ""
        target_line = lines[line_number - 1]
        next_line = lines[line_number] if line_number < len(lines) else ""

        # Highlight the target word with a color
        target_line_highlighted = target_line.replace(target_word, f"<span style='color: red'>{target_word}</span>")

        # Print the previous, target, and next lines
        st.write(f"Line {line_number - 1}: {prev_line}", unsafe_allow_html=True)
        st.write(f"Line {line_number}: {target_line_highlighted}", unsafe_allow_html=True)
        st.write(f"Line {line_number + 1}: {next_line}", unsafe_allow_html=True)

def main():
    # Displaying heading
    st.title("Concordance Analyzer")

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

