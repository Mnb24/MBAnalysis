import streamlit as st
import spacy
import requests

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Function to extract a section from the content
def get_section(file_content, section_number):
    sections = file_content.split('\nSection ')
    for section in sections:
        lines = section.strip().split('\n')
        current_section_number = lines[0].split(' ')[0]
        if current_section_number == str(section_number):
            return '\n'.join(lines[1:])  # Exclude the section number line
    return "Section not found."

# Function to convert direct speech to indirect speech
def convert_to_indirect_speech(text):
    # Process the text using SpaCy
    doc = nlp(text)
    indirect_text = ""

    # Iterate through the sentences
    for token in doc:
        # Check if the token is a quotation mark
        if token.text == '"':
            # Check if it's a starting quotation mark
            if token.head.text == '"':
                # Replace starting quotation mark with 'said'
                indirect_text += " said"
            else:
                # Replace ending quotation mark with punctuation
                indirect_text += token.text
        else:
            # Append the token text to the indirect text
            indirect_text += token.text_with_ws

    return indirect_text

# Streamlit UI
st.title('Direct to Indirect Speech Converter - Adi Parva')

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

# Allow user to input section number
section_number = st.number_input('Enter the section number (1 to 236):', min_value=1, step=1)

# Convert to indirect speech button
if st.button('Convert to Indirect Speech'):
    for file_path in file_paths:
        response = requests.get(file_path)
        file_content = response.text
        section_content = get_section(file_content, section_number)
        indirect_text = convert_to_indirect_speech(section_content)
        st.markdown(f"## Indirect Speech for Section {section_number}:")
        st.write(indirect_text)
