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
                start_index = space_index + 1
                # Check if the verse starts with "BR", "MT", "KK", or "SV"
                if verse[start_index:start_index + 2] in ["BR", "MT", "KK", "SV"]:
                    # Skip the prefix and consider the next word
                    next_space_index = verse.find(" ", start_index + 2)
                    if next_space_index != -1 and next_space_index + 1 < len(verse):
                        first_char = verse[next_space_index + 1]
                        if first_char == letter:
                            verses.append(verse)
                else:
                    # Check if the first character matches the user-input letter
                    first_char = verse[start_index]
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

# Dropdown menu for selecting the version
selected_version = st.selectbox("Select Mahabharata Version", ["BORI", "Kumbakonam", "Sastri-Vavilla", "MBTN"])

# Index to get the selected version's file path
selected_index = ["BORI", "Kumbakonam", "Sastri-Vavilla", "MBTN"].index(selected_version)

if devanagari_letter:
    try:
        # Fetch content of the selected file from GitHub
        response = requests.get(file_paths[selected_index])
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
            st.write(f"No verses found beginning with '{devanagari_letter}'.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
