import streamlit as st
import requests
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Function to count word co-occurrences in text
def count_word_cooccurrences(text):
    words_text = re.findall(r'\b\w+\b', text.lower())
    word_pairs = [(words_text[i], words_text[i+1]) for i in range(len(words_text)-1)]
    word_cooccurrences = Counter(word_pairs)
    return word_cooccurrences

st.title('Top 10 Word Pairs Co-occurrence Heatmap')

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
    # Count word co-occurrences
    word_cooccurrences = count_word_cooccurrences(text)
    
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

