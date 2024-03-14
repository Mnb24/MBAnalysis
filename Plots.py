import streamlit as st
import requests
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import STOPWORDS

def count_words_in_text(text):
    words_text = re.findall(r'\w+', text)
    return Counter(words_text)

st.title('Word Frequency Analyzer - Adi Parva')

section_number = st.number_input("Enter section number:", min_value=1, max_value=236, value=1, step=1)

# Define the file paths and translations
translations = {
    'Bibek Debroy': 'BD',
    'KM Ganguly': 'KMG',
    'MN Dutt': 'MND'
}

selected_translation = st.selectbox("Select translation:", list(translations.keys()))

# Define the file path for the selected translation
selected_translation_path = {
    'Bibek Debroy': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
    'KM Ganguly': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
    'MN Dutt': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
}[selected_translation]

if st.button('Analyze'):
    response = requests.get(selected_translation_path)
    text = response.text
    
    # Split text into sections based on the section headings
    sections = text.split('Section')
    section_text = sections[section_number].strip() if section_number <= len(sections) else ''
    
    # Count words in the section text
    word_counts = count_words_in_text(section_text)
    
    # Remove stopwords from word counts
    word_counts = {word: count for word, count in word_counts.items() if word.lower() not in STOPWORDS}
    
    # Sort words by frequency
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Get top 10 words
    top_words = sorted_word_counts[:10]
    
    # Create a DataFrame for the top words
    df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
    
    # Create a histogram for word frequencies
    st.subheader("Histogram of Word Frequencies")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Frequency'], bins=20, kde=True)
    plt.xlabel('Frequency')
    plt.ylabel('Count')
    plt.grid(True)
    st.pyplot(plt)

    # Create a pie chart for word frequencies
    st.subheader("Pie Chart of Word Frequencies")
    plt.figure(figsize=(8, 8))
    plt.pie(df['Frequency'], labels=df['Word'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    st.pyplot(plt)

    # Create a line plot for word frequencies
    st.subheader("Line Plot of Word Frequencies")
    plt.figure(figsize=(10, 6))
    plt.plot(df['Word'], df['Frequency'], marker='o', linestyle='-')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)
