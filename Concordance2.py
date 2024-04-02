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
    # Print concordance results with context paragraphs for each text
    for text_index, text in enumerate(texts):
        st.write(f"\nConcordance Analysis for Text {text_index + 1}:")
        context_sentences = get_context_sentences(text, target_word)
        for sentence_index, (sentence_number, context) in enumerate(context_sentences):
            st.write(f"Line {sentence_number} ({text_index}):")
            for line in context:
                st.write(line.strip())
            st.write("")

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
