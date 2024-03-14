import streamlit as st
import requests
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# Function to count word co-occurrences in text
def count_word_cooccurrences(text, words1, words2):
    words_text = re.findall(r'\b\w+\b', text.lower())
    word_pairs = [(word1, word2) for word1 in words1 for word2 in words2]
    word_cooccurrences = Counter(pair for pair in zip(words_text, words_text[1:]) if pair in word_pairs)
    return word_cooccurrences

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

# Input word sets
word_set1 = st.text_input("Enter words in first set (comma-separated):")
word_set2 = st.text_input("Enter words in second set (comma-separated):")

if st.button('Generate Heatmap'):
    # Split words and remove empty strings
    words1 = [word.strip() for word in word_set1.split(',') if word.strip()]
    words2 = [word.strip() for word in word_set2.split(',') if word.strip()]
    
    # Count word co-occurrences
    word_cooccurrences = count_word_cooccurrences(text, words1, words2)
    
    # Create DataFrame from word co-occurrences
    df = pd.DataFrame.from_dict(word_cooccurrences, orient='index', columns=['Frequency'])
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, cmap="YlGnBu", cbar_kws={'label': 'Frequency'})
    plt.title('Word Co-occurrence Heatmap')
    plt.xlabel('Second Word')
    plt.ylabel('First Word')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    st.pyplot(plt)

