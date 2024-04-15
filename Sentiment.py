import streamlit as st
import requests
from textblob import TextBlob
import re

def preprocess_text(text):
    text = re.sub(r'[\'\"\”\“\’\‘]', '', text)
    return text

def get_section_content(translation_path, section_number):
    response = requests.get(translation_path)
    text = response.text
    sections = text.split('Section')
    section_text = sections[section_number].strip() if section_number <= len(sections) else ''
    return section_text

def identify_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

def generate_evidence(section_content, selected_sentiment):
    sentences = section_content.split('.')  # Split into sentences
    evidence = []
    for sentence in sentences:
        if selected_sentiment.lower() == 'positive':
            if TextBlob(sentence).sentiment.polarity > 0:
                evidence.append(sentence)
        elif selected_sentiment.lower() == 'negative':
            if TextBlob(sentence).sentiment.polarity < 0:
                evidence.append(sentence)
        else:
            if TextBlob(sentence).sentiment.polarity == 0:
                evidence.append(sentence)
    return evidence

st.title('Sentiment Instance Generator - Adi Parva')

translations = {
    'Bibek Debroy': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt',
    'KM Ganguly': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt'
}

selected_translation = st.selectbox("Select translation:", list(translations.keys()))

section_number = st.number_input("Enter section number:", min_value=1, max_value=236, value=1, step=1)

selected_sentiment = st.selectbox("Select sentiment:", ['Positive', 'Negative', 'Neutral'])

if st.button('Generate Instances'):
    section_content = get_section_content(translations[selected_translation], section_number)
    section_content = preprocess_text(section_content)
    evidence = generate_evidence(section_content, selected_sentiment)
    st.write("Evidence for", selected_sentiment, "sentiment in Section", section_number, "of", selected_translation, "translation:")
    for sentence in evidence:
        st.write("-", sentence.strip())

