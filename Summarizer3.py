import streamlit as st
import requests
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import re

# Streamlit UI
st.title('Document Summarizer (LSA) - Adi Parva')

# Function to extract a section from the content
def get_section(file_content, section_number):
    sections = file_content.split('\nSection ')
    for section in sections:
        lines = section.strip().split('\n')
        current_section_number = lines[0].split(' ')[0]
        if current_section_number == str(section_number):
            return '\n'.join(lines[1:])  # Exclude the section number line
    return "Section not found."

# Preprocess text
def preprocess_text(text):
    # Remove special characters and digits
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    # Lowercase the text
    text = text.lower()
    return text

# Function to summarize using Latent Semantic Analysis (LSA)
def lsa_summary(sentences, num_sentences=5):
    # Preprocess sentences
    clean_sentences = [preprocess_text(sentence) for sentence in sentences]

    # Create TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(clean_sentences)
    
    # Apply Truncated SVD (LSA)
    lsa = TruncatedSVD(n_components=num_sentences, random_state=42)
    lsa_matrix = lsa.fit_transform(tfidf_matrix)
    
    # Get top sentences
    top_sentence_indices = lsa_matrix.argmax(axis=0)
    top_sentences = [sentences[i] for i in top_sentence_indices]
    summary = ' '.join(top_sentences)
    
    return summary

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

file_names = ['BD1', 'KMG1']

# Allow user to input section number
section_number = st.number_input('Enter the section number (1 to 236):', min_value=1, step=1)

# Display both buttons side by side
col1, col2 = st.columns(2)

# View Section button
if col1.button('View Section'):
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        section_content = get_section(file_content, section_number)
        st.markdown(f"## Section {section_number} from {file_name}:")
        st.write(section_content)

# Summarize Section button using LSA
if col2.button('Summarize Section (LSA)'):
    for file_path in file_paths:
        response = requests.get(file_path)
        file_content = response.text
        sentences = sent_tokenize(get_section(file_content, section_number))
        summary = lsa_summary(sentences)
        st.markdown(f"## Summary for Section {section_number}:")
        st.write(summary)
