import streamlit as st
from transformers import pipeline
import requests
import re

# Load the summarization pipeline from Hugging Face
summarizer = pipeline("summarization")

# Function to extract a section from the content
def get_section(file_content, section_number):
    sections = file_content.split('\nSection ')
    for section in sections:
        lines = section.strip().split('\n')
        current_section_number = lines[0].split(' ')[0]
        if current_section_number == str(section_number):
            return '\n'.join(lines[1:])  # Exclude the section number line
    return "Section not found."

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\W', ' ', text) # Remove special characters
    text = re.sub(r'\d', ' ', text) # Remove digits
    text = text.lower() # Lowercase the text
    return text

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

file_names = ["Bibek Debroy's", "KM Ganguly's"]

# Set Streamlit title
st.title('Document Summarizer (Hugging Face Transformer) - Adi Parva')

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

# Summarize Section button using Hugging Face Transformer
if col2.button('Summarize Section (Hugging Face Transformer)'):
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        section_text = get_section(file_content, section_number)
        
        # Preprocess text and summarize
        section_text_preprocessed = preprocess_text(section_text)
        summary = summarizer(section_text_preprocessed, max_length=150, min_length=50, do_sample=False)
        
        st.markdown(f"## Summary for Section {section_number} from {file_name}:")
        st.write(summary[0]['summary_text'])
