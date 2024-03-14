import streamlit as st
import requests
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def count_words_in_text(text):
    words_text = re.findall(r'\b\w+\b', text.lower())  # Only alphabetic words
    return Counter(words_text)

st.title('Heatmap Generator')

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

# Section number input
section_number = st.number_input("Enter section number:", min_value=1, max_value=236, value=1, step=1)

if st.button('Generate Heatmap'):
    # Split text into sections based on the section headings
    sections = text.split('Section')

    # Extract text of the selected section
    section_text = sections[int(section_number) - 1].strip() if 1 <= int(section_number) <= len(sections) else ''

    # Count words in the section text
    word_counts = count_words_in_text(section_text)
    
    # Create DataFrame from word counts
    df = pd.DataFrame.from_dict(word_counts, orient='index', columns=['Frequency'])
    df.reset_index(inplace=True)
    df.columns = ['Word', 'Frequency']
    
    # Create heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.pivot("Word", "Frequency", "Frequency"), cmap="YlGnBu", cbar_kws={'label': 'Frequency'})
    plt.title(f'Word Frequency Heatmap for Section {section_number}')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.tight_layout()
    
    st.pyplot(plt)

