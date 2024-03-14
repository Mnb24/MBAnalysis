import streamlit as st
import requests
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# Function to fetch text from URL
def fetch_text(url):
    response = requests.get(url)
    return response.text

# Function to create a heatmap
def create_heatmap(text):
    # Initialize CountVectorizer to convert text into a matrix of word counts
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([text])

    # Convert the word counts matrix into a DataFrame
    df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

    # Compute the correlation matrix
    corr_matrix = df.corr()

    # Create a heatmap using seaborn
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, cmap="YlGnBu")
    plt.title('Word Co-occurrence Heatmap')
    plt.xlabel('Words')
    plt.ylabel('Words')

# Streamlit app
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
text = fetch_text(file_urls[selected_translation])

if st.button('Generate Heatmap'):
    create_heatmap(text)
    st.pyplot()

