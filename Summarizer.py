import streamlit as st
import requests
from transformers import BartTokenizer, BartForConditionalGeneration

# Load BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

def summarize_text(text):
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=150, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

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
        summary = summarize_text(section_content)
        st.write(summary)


