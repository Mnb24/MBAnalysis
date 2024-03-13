import streamlit as st
import requests
import re
from collections import Counter

# Function to preprocess text
def preprocess_text(text):
    # Remove quotation marks
    text = re.sub(r'["“”]', '', text)
    return text

# Function to get section content from file content
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

# Function to calculate Jaccard similarity
def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union if union != 0 else 0

# Streamlit UI
st.title('Compare Sections - Adi Parva')

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

# File names
file_names = ["Bibek Debroy's", "KM Ganguly's"]

# Allow user to input section number
section_number = st.number_input('Enter the section number (1 to 236):', min_value=1, step=1)

if st.button('View Section'):
    section_texts = []
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        section_content = get_section(file_content, section_number)
        section_texts.append(preprocess_text(section_content))
        st.markdown(f"## Section {section_number} from {file_name}:")
        st.write(section_content)

    if len(section_texts) == 2:
        # Tokenize the text
        words1 = set(section_texts[0].split())
        words2 = set(section_texts[1].split())

        # Calculate Jaccard similarity
        similarity_score = jaccard_similarity(words1, words2)

        # Get common words excluding stopwords and quotation marks
        common_words = list(words1.intersection(words2))

        # Display similarity score and common words
        st.write(f"Similarity Score: {similarity_score}")
        st.write("Common Words:")
        for word in common_words:
            st.write(word)
    else:
        st.write("Please select exactly 2 files.")

