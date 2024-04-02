import streamlit as st
from nltk.tokenize import sent_tokenize
import requests
import nltk

# Download nltk resources
nltk.download('punkt')

def get_context_sentences(text, target_word, context_lines=2):
    sentences = sent_tokenize(text)
    context_sentences = []

    # Find sentences containing the target word
    for i, sentence in enumerate(sentences):
        if target_word in sentence:
            start_index = max(0, i - context_lines)
            end_index = min(len(sentences), i + context_lines + 1)
            context_sentences.append((i, sentences[start_index:end_index]))

    return context_sentences

def perform_concordance(texts, target_word):
    # Initialize lists to store occurrences from each text
    concordance_lists = [[] for _ in texts]

    # Get occurrences with context for each text
    for text_index, text in enumerate(texts):
        context_sentences = get_context_sentences(text, target_word)
        for sentence_index, (sentence_number, context) in enumerate(context_sentences):
            concordance_lists[text_index].append((sentence_number, context))

    # Print occurrences together from each text
    while True:
        group_found = False
        for text_index, concordance_list in enumerate(concordance_lists):
            if len(concordance_list) > 0:
                sentence_number, context = concordance_list.pop(0)
                st.write(f"Line {sentence_number} ({text_index}):")
                for line in context:
                    if target_word in line:
                        line = line.replace(target_word, f"<span style='color: red'>{target_word}</span>")
                    st.write(line.strip())
                st.write("")
                group_found = True

        if not group_found:
            break

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

