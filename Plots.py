import streamlit as st
import requests
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Function to count words in text
def count_words_in_text(text):
    words_text = re.findall(r'\b[A-Za-z]+\b', text.lower())  # Omit numbers and punctuation marks
    return Counter(words_text)

# Function to count word co-occurrences
def count_word_cooccurrences(text):
    words_text = word_tokenize(text.lower())
    word_pairs = [(words_text[i], words_text[i+1]) for i in range(len(words_text)-1)]
    return Counter(word_pairs)

st.title('Word Co-occurrence Heatmap')

# File URLs
file_urls = {
    'Bibek Debroy': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt',
    'KM Ganguly': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt',
    'MN Dutt': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
}

# Translation selection
selected_translation = st.selectbox("Select translation:", list(file_urls.keys()))

# Get text from selected translation URL
response = requests.get(file_urls[selected_translation])
text = response.text

if st.button('Generate Heatmap'):
    # Count words in the text
    word_counts = count_words_in_text(text)
    
    # Remove stopwords from word counts
    stop_words = set(stopwords.words('english'))
    word_counts = {word: count for word, count in word_counts.items() if word.lower() not in stop_words}
    
    # Count word co-occurrences
    word_cooccurrences = count_word_cooccurrences(text)
    
    # Remove stopwords from word co-occurrences
    word_cooccurrences = {pair: count for pair, count in word_cooccurrences.items() if pair[0] not in stop_words and pair[1] not in stop_words}
    
    # Convert to DataFrame and select top 10 word pairs
    df = pd.DataFrame.from_dict(word_cooccurrences, orient='index', columns=['Frequency'])
    df = df.sort_values(by='Frequency', ascending=False).head(10)
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, cmap="YlGnBu", annot=True, fmt="d", cbar_kws={'label': 'Frequency'})
    plt.title('Top 10 Word Pairs Co-occurrence Heatmap')
    plt.xlabel('Second Word')
    plt.ylabel('First Word')
    
    st.pyplot(plt)
