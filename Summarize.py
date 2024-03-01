import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee
nltk.download('punkt')
nltk.download('stopwords')

def get_section(file_name, section_number):
    content = file_name.read().decode()
    sections = re.split(r'Section \d+', content)
    if section_number < len(sections):
        return sections[section_number]
    else:
        return "Section not found."

def truncate_text(text, word_limit):
    words = nltk.word_tokenize(text)
    truncated_text = ' '.join(words[:word_limit])
    return truncated_text

def build_similarity_matrix(sentences, stop_words):
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = vectorizer.fit_transform(sentences)
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return similarity_matrix

def pagerank(M, num_iterations=100, d=0.85):
    N = M.shape[1]
    v = np.random.rand(N, 1)
    v = v / np.linalg.norm(v, 1)
    M_hat = (d * M + (1 - d) / N)
    for i in range(num_iterations):
        v = M_hat @ v
    return v

def generate_summary(file_name, section_number, word_limit=200, top_n=5):
    section = get_section(file_name, section_number)
    if section == "Section not found.":
        return section

    if len(section.split()) > word_limit:
        section = truncate_text(section, word_limit)

    sentences = nltk.sent_tokenize(section)
    stop_words = set(stopwords.words('english'))

    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    scores = pagerank(csr_matrix(sentence_similarity_matrix))

    scores = scores.flatten()

    ranked_sentences = [sentences[i] for i in np.argsort(scores)[::-1][:top_n]]
    summary = ' '.join(ranked_sentences)

    return summary

st.title('Document Summarizer')

num_files = st.number_input('Enter the number of files:', min_value=1, step=1)
file_names = []
for i in range(num_files):
    file_name = st.file_uploader(f'Choose file {i+1}', type=['txt'])
    if file_name is not None:
        file_names.append(file_name)

section_number = st.number_input('Enter the section number:', min_value=1, step=1)

if st.button('Summarize'):
    st.write('Summaries for each file:\n')
    for file_name in file_names:
        summary = generate_summary(file_name, section_number)
        st.write(f"Summary for {file_name.name}:")
        st.write(summary)
        st.write("-" * 50)

