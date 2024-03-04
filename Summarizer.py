import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re

def get_section(file_name, section_number):
    with open(file_name, 'r') as file:
        content = file.read()
        sections = re.split(r'Section \d+', content)
        if section_number < len(sections):
            return sections[section_number]
        else:
            return "Section not found."

def truncate_text(text, word_limit):
    words = word_tokenize(text)
    truncated_text = ' '.join(words[:word_limit])
    return truncated_text

def generate_summary(file_name, section_number, word_limit=200, top_n=5):
    section = get_section(file_name, section_number)
    if section == "Section not found.":
        return section

    # Truncate the section if it exceeds the word limit
    if len(section.split()) > word_limit:
        section = truncate_text(section, word_limit)

    # Tokenize sentences
    sentences = sent_tokenize(section)
    stop_words = set(stopwords.words('english'))

    # Generate similarity matrix across sentences
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    # Rank sentences using PageRank algorithm
    scores = pagerank(sentence_similarity_matrix)

    # Flatten the scores array
    scores = scores.flatten()

    # Sort the rank and pick top sentences
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[::-1][:top_n]]
    summary = ' '.join(ranked_sentences)

    return summary

num_files = st.number_input("Enter the number of files:", min_value=1, step=1)
file_names = []
for i in range(num_files):
    file_name = st.text_input(f"Enter the name of file {i+1}: ")
    file_names.append(file_name)

section_number = st.number_input("Enter the section number: ", min_value=1, step=1)

st.write("\nUsing TextRank Summarization:")
for file_name in file_names:
    st.write(f"Summary for {file_name}:")
    summary = generate_summary(file_name, section_number)
    st.write(summary)
    st.write("-" * 50)
