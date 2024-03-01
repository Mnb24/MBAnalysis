import streamlit as st
from collections import Counter
import re

def count_word_in_text(text, word):
    words = re.findall(r'\w+', text.lower())
    return words.count(word.lower())

st.title('Word Frequency Analyzer - Adi Parva')

word_to_search = st.text_input("Enter a word to search:")

uploaded_files = []
for i in range(3):
    file = st.file_uploader(f"Choose a text file {i+1}", type="txt")
    if file is not None:
        uploaded_files.append(file)

if st.button('Analyze'):
    if word_to_search and len(uploaded_files) == 3:
        for i, file in enumerate(uploaded_files, start=1):
            text = file.getvalue().decode()
            count = count_word_in_text(text, word_to_search)
            st.write(f'Frequency of "{word_to_search}" in file {i}: {count}')
    else:
        st.write("Please input a word and upload 3 files.")
