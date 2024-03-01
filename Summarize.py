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
    st.write("**Original Text:**")
    st.write(text)

    if st.button("Summarize"):
        summary = generate_summary(text)
        st.write("**Summary:**")
        st.write(summary)

