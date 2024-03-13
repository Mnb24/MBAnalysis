import requests
import streamlit as st
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import string

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove punctuation and lowercase all tokens
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table).lower() for w in tokens]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in stripped if word.isalpha() and word not in stop_words]
    return words

def get_common_words(text1, text2):
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)
    common_words = set(words1) & set(words2)
    return list(common_words)

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
    
    st.write("Common Words:")
    st.write(common_words)

