import requests
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords

# Function to count words in text
def count_words_in_text(text):
    words_text = re.findall(r'\b[A-Za-z]+\b', text.lower())  # Omit numbers and punctuation marks
    return Counter(words_text)

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
    word_pairs = [(words_text[i], words_text[i+1]) for i in range(len(words_text)-1)]
    word_cooccurrences = Counter(word_pairs)
    
    # Filter out stopwords from word co-occurrences
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
 to include it in this code: import streamlit as st
import requests
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from nltk import pos_tag, word_tokenize
from wordcloud import STOPWORDS

def count_words_in_text(text):
    words_text = re.findall(r'\b[A-Za-z]+\b', text)  # Omit numbers and punctuation marks
    return Counter(words_text)

def count_pos(text):
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    pos_counts = Counter(tag for word, tag in pos_tags)
    return pos_counts

st.title('Plots for Adi Parva Sections')

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
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Word', y='Frequency', data=df)
    plt.title('Top 10 Words in Section {}\n\n\n\n'.format(section_number), fontsize=20, fontweight='bold')  
    plt.xticks(rotation=45, fontsize=12)  # Increase font size
    plt.yticks(fontsize=12)  # Increase font size
    plt.xlabel('Word', fontsize=14)  # Increase font size
    plt.ylabel('Frequency', fontsize=14)  # Increase font size
    
    # Add frequency as text on bars within the plot's rectangle
    for bar, frequency in zip(ax.patches, df['Frequency']):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), frequency,
                 ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    st.pyplot(plt)
      
    
    # Create a pie chart for the distribution of the top 10 words
    plt.figure(figsize=(8, 8))
    plt.pie(df['Frequency'], labels=df['Word'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Distribution of Top 10 Words\n\n\n\n', fontsize=16, fontweight='bold')
    plt.rcParams['font.size'] = 10  # Adjust font size of pie chart labels and percentages
    
    st.pyplot(plt)

    # Count POS in the section text
    pos_counts = count_pos(section_text)
    
    # Filter out punctuation POS tags
    filtered_pos_counts = {pos: count for pos, count in pos_counts.items() if pos.isalpha()}
    
    # Create a DataFrame for filtered POS counts
    pos_df = pd.DataFrame(filtered_pos_counts.items(), columns=['POS', 'Count'])
    
    # Create a bar plot for POS counts
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='POS', y='Count', data=pos_df)
    plt.title('Part-of-Speech Frequencies\n\n\n', fontsize=20, fontweight='bold')  # Increase font size and make it bold
    plt.xticks(rotation=45, fontsize=12)  # Increase font size
    plt.yticks(fontsize=12)  # Increase font size
    plt.xlabel('Part of Speech', fontsize=14)  # Increase font size
    plt.ylabel('Count', fontsize=14)  # Increase font size

    # Add frequency as text on bars within the plot's rectangle
    for bar, count in zip(ax.patches, pos_df['Count']):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), count,
                 ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    st.pyplot(plt) 
