import streamlit as st
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Function to extract a section from the content
def get_section(file_content, section_number):
    sections = file_content.split('\n')
    found_sections = []
    for line in sections:
        if line.strip().startswith("Section"):
            current_section_number = line.strip().split(" ")[1]
            if current_section_number == str(section_number):
                found_sections.append(line)
            elif found_sections:
                break
        elif found_sections:
            found_sections.append(line)
    return '\n'.join(found_sections)

# Function to truncate text to a word limit
def truncate_text(text, word_limit):
    words = word_tokenize(text)
    truncated_text = ' '.join(words[:word_limit])
    return truncated_text

# Function to build a similarity matrix
def build_similarity_matrix(sentences, stop_words):
    clean_sentences = [sentence.lower() for sentence in sentences if sentence not in stop_words]
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 != idx2:
                similarity_matrix[idx1][idx2] = sentence_similarity(clean_sentences[idx1], clean_sentences[idx2])
    return similarity_matrix

# Function to compute sentence similarity
def sentence_similarity(sent1, sent2):
    stop_words = set(stopwords.words('english'))
    words1 = [word.lower() for word in word_tokenize(sent1) if word.lower() not in stop_words]
    words2 = [word.lower() for word in word_tokenize(sent2) if word.lower() not in stop_words]
    all_words = list(set(words1 + words2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for word in words1:
        vector1[all_words.index(word)] += 1
        
    for word in words2:
        vector2[all_words.index(word)] += 1
    
    return cosine_similarity([vector1], [vector2])[0,0]

# Function to perform PageRank
def pagerank(similarity_matrix, damping=0.85, epsilon=1.0e-8, max_iterations=100):
    n = similarity_matrix.shape[0]
    p = np.ones(n) / n  
    
    for _ in range(max_iterations):
        new_p = np.ones(n) * (1 - damping) / n + damping * similarity_matrix.T.dot(p)
        if abs(np.sum(new_p - p)) < epsilon:
            return new_p
        p = new_p
    return p

# Function to generate a summary for a given text content
def generate_summary(text_content, word_limit=200, top_n=5):
    if len(word_tokenize(text_content)) > word_limit:
        text_content = truncate_text(text_content, word_limit)

    sentences = sent_tokenize(text_content)
    stop_words = set(stopwords.words('english'))

    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)
    scores = pagerank(sentence_similarity_matrix)
    scores = scores.flatten()
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[::-1][:top_n]]
    summary = ' '.join(ranked_sentences)

    return summary

# Streamlit UI
st.title('Document Viewer - Adi Parva')

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt' 
              ]

# File names
file_names = ["Bibek Debroy's", "KM Ganguly's", "MN Dutt's"]

# Allow user to input section number
section_number = st.number_input('Enter the section number (1 to 236):', min_value=1, step=1)

if st.button('View Section'):
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        section_content = get_section(file_content, section_number)
        st.markdown(f"## Section {section_number} from {file_name}:")
        st.write(section_content)   

if st.button('Summarize'):
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        section_content = get_section(file_content, section_number)
        summary = generate_summary(section_content)
        st.markdown(f"## Summary for Section {section_number} from {file_name}:")
        st.write(summary)
