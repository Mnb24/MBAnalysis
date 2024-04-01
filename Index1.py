import streamlit as st
import requests

# Function to fetch verses beginning with the specified Devanagari letter
def fetch_verses(letter, texts):
    verses = []

    # Iterate through each file
    for text in texts:
        for verse in text:
            # Split the verse by space
            parts = verse.split(" ", 1)
            # Check if there are at least two parts after splitting
            if len(parts) >= 2:
                marker, devanagari = parts
                # Check if the devanagari text starts with the specified letter
                if devanagari.startswith(letter):
                    verses.append(verse)
    
    return verses

# Streamlit UI
st.title("Index - Adi Parva")

# URLs of the text files
file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt'
]

# User input for Devanagari letter
devanagari_letter = st.text_input("Enter a Devanagari letter:")

# Dictionary to map file names to their index
file_names = {0: "BORI", 1: "Kumbakonam", 2: "Sastri-Vavilla" }

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
            for i, text in enumerate(texts):
                st.markdown(f"<h3 style='font-size:24px'>{file_names[i]}</h3>", unsafe_allow_html=True)
                file_verses = [verse for verse in text if len(verse.split(" ", 1)) >= 2 and verse.split(" ", 1)[1].startswith(devanagari_letter)]
                if file_verses:
                    for verse in file_verses:
                        highlighted_verse = verse.replace(devanagari_letter, f"<span style='color:red'>{devanagari_letter}</span>", 1)
                        st.write(highlighted_verse, unsafe_allow_html=True)
                else:
                    st.write(f"No verses found beginning with '{devanagari_letter}' in {file_names[i]}.")
        else:
            st.write(f"No verses found beginning with '{devanagari_letter}'.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
