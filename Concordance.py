import streamlit as st
from nltk.tokenize import sent_tokenize, word_tokenize
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

def perform_concordance(text, target_word, text_name):
    context_paragraphs = get_context_paragraphs(text, target_word)

    # Print concordance results with context paragraphs
    if context_paragraphs:
        for paragraph in context_paragraphs:
            # Highlight the target word with a color
            highlighted_paragraph = paragraph.replace(target_word, f"<span style='color: red'>{target_word}</span>")
            st.write(highlighted_paragraph, unsafe_allow_html=True)
            st.write("\n")

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
            st.markdown(f"<h2 style='font-size:24px'>{text_name}</h2>", unsafe_allow_html=True)
            perform_concordance(text, target_word, text_name)

if __name__ == "__main__":
    main()

