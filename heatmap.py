import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

# Function to count words in text
def count_words_in_text(text):
    words_text = re.findall(r'\w+', text.lower())
    return Counter(words_text)

st.title('Section Heatmap Generator')

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

# Extract text for the specified section
sections = text.split('Section')
section_text = sections[section_number].strip() if section_number <= len(sections) else ''

if st.button('Generate Heatmap'):
    # Count words in the text
    word_counts = count_words_in_text(section_text)

    # Convert word counts to DataFrame for heatmap
    df = pd.DataFrame.from_dict(word_counts, orient='index', columns=['Frequency'])
    df.reset_index(inplace=True)
    df.columns = ['Word', 'Frequency']
    df['Word'] = df['Word'].str.capitalize()  # Capitalize words for better readability

    # Create heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.pivot("Word", "Frequency", "Frequency"), cmap="YlGnBu", cbar_kws={'label': 'Frequency'})
    plt.title(f'Word Frequency Heatmap for Section {section_number}')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    st.pyplot(plt)
