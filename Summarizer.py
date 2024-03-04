import streamlit as st
import requests
from transformers import pipeline
import re

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

# Function to retrieve a section from the document
def get_section(file_content, section_number):
    # Your logic to retrieve the section based on the section number
    pass

# Streamlit UI
st.title('Document Viewer - Adi Parva')

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt']

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

        # Summarize section content
        st.markdown(f"## Summary of Section {section_number} from {file_name}:")
        summary = summarizer(section_content, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        st.write(summary)
