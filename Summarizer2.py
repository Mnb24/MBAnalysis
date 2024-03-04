import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy as np
import networkx as nx
import re
import requests

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Remove special characters and digits
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    # Lowercase the text
    text = text.lower()
    return text

def build_similarity_matrix(sentences):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
    # Preprocess sentences
    clean_sentences = [preprocess_text(sentence) for sentence in sentences]

    # Build similarity matrix
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(clean_sentences[i], clean_sentences[j])

    # Normalize similarity matrix
    similarity_matrix = similarity_matrix / similarity_matrix.sum(axis=1, keepdims=True)
    return similarity_matrix

def sentence_similarity(sent1, sent2):
    # Tokenize sentences
    words1 = set(word_tokenize(sent1))
    words2 = set(word_tokenize(sent2))

    # Compute Jaccard similarity
    return len(words1.intersection(words2)) / len(words1.union(words2))

def textrank_summary(sentences, top_n=5):
    # Build similarity matrix
    similarity_matrix = build_similarity_matrix(sentences)

    # Apply PageRank algorithm
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)

    # Sort sentences by score and pick top sentences
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
    summary = ' '.join([sentence for score, sentence in ranked_sentences[:top_n]])
    return summary

# Streamlit UI
st.title('Text Summarizer - TextRank Algorithm')

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

# File names
file_names = ["Bibek Debroy's", "KM Ganguly's"]

# Allow user to input section number
section_number = st.number_input('Enter the section number (1 to 236):', min_value=1, step=1)

# View Section button
if st.button('View Section'):
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        section_content = get_section(file_content, section_number)
        st.markdown(f"## Section {section_number} from {file_name}:")
        st.write(section_content)

# Summarize Section button using TextRank
if st.button('Summarize Section (TextRank)'):
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        sentences = sent_tokenize(get_section(file_content, section_number))
        summary = textrank_summary(sentences)
        st.markdown(f"## Summary for Section {section_number} from {file_name}:")
        st.write(summary)
