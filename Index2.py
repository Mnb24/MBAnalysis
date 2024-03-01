import streamlit as st
import requests

# Function to fetch verses beginning with the specified Devanagari letter
def fetch_verses(letter, texts):
    verses = []

    # Iterate through each file
    for text in texts:
        file_verses = [verse for verse in text if verse.startswith(letter)]
        verses.append(file_verses)
    
    return verses

# Streamlit UI
st.title("Index - Adi Parva")

# URLs of the text files
file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-01-Complete.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-01-Complete.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-01-Complete.txt'
]

# User input for Devanagari letter
devanagari_letter = st.text_input("Enter a Devanagari letter:")

# Dictionary to map file names to their index
file_names = {0: "BORI", 1: "Kumbakonam", 2: "Sastri-Vavilla"}

if devanagari_letter:
    try:
        # Fetch content of files from GitHub
        responses = [requests.get(file_path) for file_path in file_paths]
        texts = [response.text.splitlines() for response in responses]

        # Fetch verses beginning with the specified letter
        verses = fetch_verses(devanagari_letter, texts)

        # Display verses
        if any(verses):
            st.write(f"Verses beginning with '{devanagari_letter}':")
            max_len = max([len(file_verses) for file_verses in verses])
            for i in range(max_len):
                for j, file_verses in enumerate(verses):
                    if i < len(file_verses):
                        highlighted_verse = file_verses[i].replace(devanagari_letter, f"<span style='color:red'>{devanagari_letter}</span>", 1)
                        st.markdown(f"<h3 style='font-size:24px'>{file_names[j]}</h3>", unsafe_allow_html=True)
                        st.write(highlighted_verse, unsafe_allow_html=True)
        else:
            st.write(f"No verses found beginning with '{devanagari_letter}'.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

