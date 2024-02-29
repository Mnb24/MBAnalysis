import streamlit as st
import requests

# Function to fetch verses beginning with the specified Devanagari letter
def fetch_verses(letter, texts):
    verses = []

    # Iterate through each file
    for text in texts:
        for verse in text:
            if verse.startswith(letter):
                verses.append(verse)
    
    return verses

# Streamlit UI
st.title("Index")

# URLs of the text files
file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-01-Complete.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-01-Complete.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-01-Complete.txt'
]


# User input for Devanagari letter
devanagari_letter = st.text_input("Enter a Devanagari letter:")

if devanagari_letter:
    try:
        # Fetch content of files from GitHub
        responses = [requests.get(file_path) for file_path in file_paths]
        texts = [response.text.splitlines() for response in responses]

        # Fetch verses beginning with the specified letter
        verses = fetch_verses(devanagari_letter, texts)

        # Display verses
        if verses:
            st.write(f"Verses beginning with '{devanagari_letter}':")
            for verse in verses:
                st.write(verse)
        else:
            st.write(f"No verses found beginning with '{devanagari_letter}'.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

