import streamlit as st
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def count_words_in_text(text, words):
    words_text = re.findall(r'\w+', text.lower())
    return [words_text.count(word.lower()) for word in words]

st.title('Word Frequency Analyzer')

words_to_search = st.text_input("Enter words to search (comma separated):")

uploaded_files = []
for i in range(3):
    file = st.file_uploader(f"Choose a text file {i+1}", type="txt")
    if file is not None:
        uploaded_files.append(file)

if st.button('Analyze'):
    if words_to_search and len(uploaded_files) == 3:
        words_to_search = [word.strip() for word in words_to_search.split(',')]
        data = []
        for i, file in enumerate(uploaded_files, start=1):
            text = file.getvalue().decode()
            counts = count_words_in_text(text, words_to_search)
            for word, count in zip(words_to_search, counts):
                data.append([f'File {i}', word, count])

        # Create a DataFrame
        df = pd.DataFrame(data, columns=['File', 'Word', 'Frequency'])

        # Create a bar plot
        sns.barplot(x='File', y='Frequency', hue='Word', data=df)
        plt.title('Frequency of each word in each file')
        st.pyplot(plt)
    else:
        st.write("Please input words (comma separated) and upload 3 files.")
