import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.text import Text
import requests
import nltk

# Download nltk resources
nltk.download('punkt')

def perform_concordance(texts, target_word):
    # Initialize concordance lists for each text
    concordance_lists = []
    file_names = ['BD', 'KMG', 'MND']
    for text, file_name in zip(texts, file_names):
        tokens = word_tokenize(text)
        text_object = Text(tokens)
        concordance_lists.append((text_object.concordance_list(target_word), file_name))

    # Print concordance results with context
    for concordance_list, file_name in concordance_lists:
        for entry in concordance_list:
            left_context = " ".join(entry.left[-2:])
            right_context = " ".join(entry.right[:2])
            line_number = text.count('\n', 0, entry.offset) + 1  # Calculate line number

            # Highlight the target word with a color
            highlighted_text = f"{left_context} <span style='color: red'>{target_word}</span> {right_context}"
            st.write(f"Line {line_number} ({file_name}): {highlighted_text}", unsafe_allow_html=True)
            st.write("\n")

    # Add extra lines at the end for readability
    st.write("\n\n")


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
