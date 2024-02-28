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

    # Print concordance results in groups of three occurrences
    group_index = 0
    occurrences_count = 0
    while True:
        group_found = False
        for i, (concordance_list, file_name) in enumerate(concordance_lists):
            if group_index < len(concordance_list):
                entry = concordance_list[group_index]
                left_context = " ".join(entry.left)
                right_context = " ".join(entry.right)
                line_number = text.count('\n', 0, entry.offset) + 1  # Calculate line number

                # Highlight the target word with a color
                highlighted_text = f"{left_context} <span style='color: red'>{target_word}</span> {right_context}"
                st.write(f"Line {line_number} ({file_name}): {highlighted_text}", unsafe_allow_html=True)
                
                group_found = True
                occurrences_count += 1

        if not group_found:
            break

        group_index += 1

        # Add a symbol after each group of three occurrences
        if occurrences_count % 3 == 0:
            st.write("***")

def main():
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
