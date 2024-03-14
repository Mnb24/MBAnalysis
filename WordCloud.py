import streamlit as st
from wordcloud import WordCloud
from collections import Counter
import re
import requests

# Function to count words in text
def count_words_in_text(text):
    words_text = re.findall(r'\w+', text.lower())
    return Counter(words_text)

st.title('Word Cloud Generator')

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

if st.button('Generate Word Cloud'):
    # Count words in the text
    word_counts = count_words_in_text(text)
    
    try:
        # Generate word cloud
        wordcloud = WordCloud(font_path='arial.ttf', max_words=100).generate_from_frequencies(word_counts)
        
        # Display word cloud
        st.image(wordcloud.to_array())
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
