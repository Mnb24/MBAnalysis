import streamlit as st
import requests
from textblob import TextBlob  # Sentiment analysis library
import re

# Function to perform text preprocessing
def preprocess_text(text):
    # Remove special characters and digits
    processed_text = re.sub(r'\W+', ' ', text)
    processed_text = re.sub(r'\d+', ' ', processed_text)
    return processed_text

# Function to perform sentiment analysis
def analyze_sentiment(text):
    # Perform sentiment analysis using TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment

    # Determine sentiment polarity
    polarity = sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Streamlit UI
st.title("Sentiment Analysis Tool")

# Define translations
translations = {
    'Bibek Debroy': 'BD',
    'KM Ganguly': 'KMG',
}

# User input for translation
selected_translation = st.selectbox("Select translation:", list(translations.keys()))

# Define the file path for the selected translation
selected_translation_path = {
    'Bibek Debroy': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
    'KM Ganguly': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt'
}[selected_translation]

# Input field for section number
section_number = st.number_input("Enter section number:", min_value=1, max_value=236, value=1, step=1)

# Button to trigger analysis
if st.button('Analyze'):
    response = requests.get(selected_translation_path)
    text = response.text
    
    # Split text into sections based on the section headings
    sections = text.split('Section')
    section_text = sections[section_number].strip() if section_number <= len(sections) else ''
    
    # Preprocess the section text
    processed_text = preprocess_text(section_text)
    
    # Perform sentiment analysis
    sentiment = analyze_sentiment(processed_text)
    
    # Display sentiment
    st.write(f"Sentiment for Section {section_number} ({selected_translation}): {sentiment}")

