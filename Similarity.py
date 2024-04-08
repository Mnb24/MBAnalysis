import streamlit as st
import requests
from difflib import SequenceMatcher

# Function to fetch text from URL
def fetch_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to find similar phrases between two texts
def find_similar_phrases(text1, text2):
    matcher = SequenceMatcher(None, text1, text2)
    match = matcher.find_longest_match(0, len(text1), 0, len(text2))
    return text2[match.b: match.b + match.size]

# Main function
def main():
    # Title and description
    st.title("File Similarity Finder")
    st.write("This app allows you to find similar words/phrases/episodes between two files.")

    # Fetching file contents
    mbtn_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MBTN.txt")
    br_complete_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    if mbtn_text is None or br_complete_text is None:
        st.error("Failed to fetch file contents. Please try again later.")
        return

    # Displaying text from the first file
    st.header("Text from File 1 (MBTN.txt)")
    st.text(mbtn_text)

    # Text area for entering required text
    st.header("Enter Required Text")
    required_text = st.text_area("Enter the text you want to find similarities for", height=200)

    # Button to find similar phrases
    if st.button("Find Similar Phrases"):
        similar_phrases = find_similar_phrases(required_text, br_complete_text)
        st.write("Similar Phrases Found:")
        st.write(similar_phrases)

# Run the main function
if __name__ == "__main__":
    main()
