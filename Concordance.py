import streamlit as st
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.text import Text
import requests
import nltk

# Download nltk resources
nltk.download('punkt')

def get_context_sentences(text, target_word, context_lines=2):
    sentences = sent_tokenize(text)
    context_sentences = []

    # Find sentences containing the target word
    for i, sentence in enumerate(sentences):
        if target_word in word_tokenize(sentence):
            start_index = max(0, i - context_lines)
            end_index = min(len(sentences), i + context_lines + 1)
            context_sentences.extend(sentences[start_index:end_index])

    return context_sentences

def perform_concordance(text, target_word):
    context_sentences = get_context_sentences(text, target_word)

    # Print concordance results with context sentences
    for i, sentence in enumerate(context_sentences, start=1):
        # Highlight the target word with a color
        highlighted_sentence = sentence.replace(target_word, f"<span style='color: red'>{target_word}</span>")
        st.write(f"Context Sentence {i}: {highlighted_sentence}", unsafe_allow_html=True)

def main():
    # Displaying heading
    st.title("Concordance Analyzer - Adi Parva")

    # URLs of the text files
    file_paths = [
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
        'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
    ]
    text_names = ['BD1', 'KMG1', 'MND1']

    target_word = st.text_input("Enter the word for concordance analysis: ")

    if st.button('Perform Concordance Analysis'):
        for file_path, text_name in zip(file_paths, text_names):
            response = requests.get(file_path)
            text = response.text
            st.write(f"\nConcordance Analysis for {text_name}:")
            perform_concordance(text, target_word)

if __name__ == "__main__":
    main()

