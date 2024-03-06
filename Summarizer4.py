import streamlit as st
import torch
from transformers import BartForConditionalGeneration, BartTokenizer
import requests
from nltk.tokenize import sent_tokenize
import re

# Load the pre-trained BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

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

# Function to generate summary using Pointer Generator Network
def generate_summary(input_text, max_length=150):
    inputs = tokenizer([input_text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=max_length, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

file_names = ["Bibek Debroy's", "KM Ganguly's"]

st.title('Document Summarizer (Pointer Generator Network) - Adi Parva')

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

# Summarize Section button using Pointer Generator Network
if col2.button('Summarize Section (Pointer Generator Network)'):
    for i, (file_path, file_name) in enumerate(zip(file_paths, file_names)):
        response = requests.get(file_path)
        file_content = response.text
        section_text = get_section(file_content, section_number)
        summary = generate_summary(section_text)
        st.markdown(f"## Summary for Section {section_number} from {file_name}:")
        st.write(summary)
