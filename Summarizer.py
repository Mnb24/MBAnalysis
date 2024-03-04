import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import requests

st.title('Text Summarizer - Adi Parva')

nltk.download('punkt')
nltk.download('stopwords')

def get_section(content, section_number):
    sections = re.split(r'Section \d+', content)
    if section_number <= len(sections) and section_number > 0:
        return sections[section_number - 1] 
    else:
        return "Section not found."

def truncate_text(text, word_limit):
    words = word_tokenize(text)
    truncated_text = ' '.join(words[:word_limit])
    return truncated_text

def build_similarity_matrix(sentences, stop_words):
    clean_sentences = [sentence.lower() for sentence in sentences if sentence not in stop_words]
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 != idx2:
                similarity_matrix[idx1][idx2] = sentence_similarity(clean_sentences[idx1], clean_sentences[idx2])
    return similarity_matrix

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

def pagerank(similarity_matrix, damping=0.85, epsilon=1.0e-8, max_iterations=100):
    n = similarity_matrix.shape[0]
    p = np.ones(n) / n  
    
    for _ in range(max_iterations):
        new_p = np.ones(n) * (1 - damping) / n + damping * similarity_matrix.T.dot(p)
        if abs(np.sum(new_p - p)) < epsilon:
            return new_p
        p = new_p
    return p

def generate_summary(file_content, section_number, word_limit=200, top_n=5):
    section = get_section(file_content, section_number)
    if section == "Section not found.":
        return section

    if len(word_tokenize(section)) > word_limit:
        section = truncate_text(section, word_limit)

    sentences = sent_tokenize(section)
    stop_words = set(stopwords.words('english'))

    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)
    scores = pagerank(sentence_similarity_matrix)
    scores = scores.flatten()
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[::-1][:top_n]]
    summary = ' '.join(ranked_sentences)

    return summary

if __name__ == "__main__":
    file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
                  'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
                  'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt']

    section_number = st.number_input("Enter the section number:", min_value=1, step=1)

    if st.button('Summarize'):
        for i, file_path in enumerate(file_paths):
            response = requests.get(file_path)
            if response.status_code == 200:
                file_content = response.text
                st.write(f"{'Bibek Debroy\'s' if i == 0 else 'KM Ganguly\'s' if i == 1 else 'MN Dutt\'s'} Summary for {file_path}:")
                summary = generate_summary(file_content, section_number)
                st.write(summary)
                st.write("-" * 50)
