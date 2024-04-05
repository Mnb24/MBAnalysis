import streamlit as st
import requests

# Function to fetch verses beginning with the specified Devanagari letter
def fetch_verses(letter, texts):
    verses = []

    # Iterate through each file
    for text in texts:
        for verse in text:
            # Check if there is a space following the marker
            space_index = verse.find(" ")
            if space_index != -1 and space_index + 1 < len(verse):
                # Get the first character after the space
                first_char = verse[space_index + 1]
                # Check if the first character matches the user-input letter
                if first_char == letter:
                    verses.append(verse)
    
    return verses

# Streamlit UI
st.title("Index - Mahabharata Verses")

# URLs of the text files
file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MBTN.txt'
]

# User input for Devanagari letter
devanagari_letter = st.text_input("Enter a Devanagari letter:")

# Dropdown menu to select the version of Mahabharata text
selected_version = st.selectbox("Select Mahabharata Version", ["BORI", "Kumbakonam", "Sastri-Vavilla", "Mahabharata Tatparya Nirnaya"])

# Dictionary to map file names to their index
file_names = {"BORI": 0, "Kumbakonam": 1, "Sastri-Vavilla": 2, "Mahabharata Tatparya Nirnaya": 3}

if devanagari_letter:
    try:
        # Fetch content of selected file from GitHub
        response = requests.get(file_paths[file_names[selected_version]])
        text = response.text.splitlines()

        # Fetch verses beginning with the specified letter
        verses = fetch_verses(devanagari_letter, [text])

        # Display verses
        if verses:
            st.write(f"Verses beginning with '{devanagari_letter}' in {selected_version}:")
            for verse in verses:
                highlighted_verse = verse.replace(devanagari_letter, f"<span style='color:red'>{devanagari_letter}</span>", 1)
                st.write(highlighted_verse, unsafe_allow_html=True)
        else:
            st.write(f"No verses found beginning with '{devanagari_letter}' in {selected_version}.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
