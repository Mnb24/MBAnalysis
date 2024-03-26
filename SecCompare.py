import requests
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove punctuation except commas and full stops
    table = str.maketrans('', '', string.punctuation.replace('.', '').replace(',', ''))
    words = [w.translate(table) for w in tokens]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    return words

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

def get_common_words(text1, text2):
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)
    common_words = set(words1) & set(words2)
    return [word for word in common_words if word.isalpha()]  # Exclude non-alphabetic words

def jaccard_similarity(text1, text2):
    words1 = set(preprocess_text(text1))
    words2 = set(preprocess_text(text2))
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    return intersection / union if union != 0 else 0

# Streamlit UI
st.title('Compare Sections - Adi Parva')

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

# File names
file_names = ["Bibek Debroy's", "KM Ganguly's"]

# Allow user to input section number
section_number = st.number_input('Enter the section number (1 to 236):', min_value=1, step=1)

if st.button('Compare Sections'):
    response1 = requests.get(file_paths[0])
    file_content1 = response1.text
    response2 = requests.get(file_paths[1])
    file_content2 = response2.text
    
    section_content1 = get_section(file_content1, section_number)
    section_content2 = get_section(file_content2, section_number)
    
    common_words = get_common_words(section_content1, section_content2)
    
    similarity_score = jaccard_similarity(section_content1, section_content2)
    
    st.write("Jaccard Similarity Score:", similarity_score)
    st.write("Common Words:")
    st.write(common_words)
