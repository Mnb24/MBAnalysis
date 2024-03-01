import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Function to preprocess and tokenize text
def preprocess_text(text):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    preprocessed_sentences = [sentence.lower() for sentence in sentences if sentence.strip() != ""]
    return preprocessed_sentences

# Function to get section content
def get_section(file_content, section_number):
    sections = file_content.split('Section ')
    for section in sections:
        if section.startswith(str(section_number) + '.'):
            return section
    return "Section not found."

# Function to generate summary
def generate_summary(text):
    sentences = preprocess_text(text)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    similarity_matrix = cosine_similarity(X, X)
    scores = similarity_matrix.sum(axis=1)
    summary_sentences = [sentences[i] for i in scores.argsort()[-5:]]
    summary = ' '.join(summary_sentences)
    return summary

# Streamlit UI
st.title('Document Summarizer')

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    # Allow user to input section number
    section_number = st.number_input('Enter the section number:', min_value=1, step=1)

    section_content = get_section(text, section_number)
    if section_content != "Section not found.":
        st.write(f"**Section {section_number} Content:**")
        st.write(section_content)

        if st.button("Summarize Section"):
            summary = generate_summary(section_content)
            st.write("**Summary:**")
            st.write(summary)
    else:
        st.write("Section not found.")
