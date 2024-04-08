import streamlit as st
import requests
import re

# Function to fetch text from URL
def fetch_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to find matches for words in the second text box in the BR file
def find_matches(text, br_text):
    matches = []
    for line in br_text.split("\n"):
        if re.search(r'\b(?:{})\b'.format("|".join(re.escape(word) for word in text.split())), line):
            # Highlight the target words
            for word in text.split():
                line = re.sub(r'\b({})\b'.format(re.escape(word)), r'<span style="background-color: #FFFF00">\1</span>', line, flags=re.IGNORECASE)
            matches.append(line)
    return matches

# Main function
def main():
    # Title and description
    st.title("File Similarity Finder")
    st.write("This app allows you to find matches for words/phrases in the second file (BR-Complete.txt).")

    # Fetching file contents
    br_complete_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    if br_complete_text is None:
        st.error("Failed to fetch file contents. Please try again later.")
        return

    # Sidebar with text input and file display
    st.sidebar.header("Text from File 1 (MBTN.txt)")
    selected_text = st.sidebar.text_area("Selected Text")

    # Text area for entering required text
    st.sidebar.header("Enter Words to Find Matches")
    required_words = st.sidebar.text_input("Enter words to find matches", "")

    # Button to find matches
    if st.sidebar.button("Find Matches"):
        if required_words.strip() == "":
            st.error("Please enter words to find matches.")
        else:
            matches = find_matches(required_words, br_complete_text)
            if matches:
                st.header("Matches Found in BR-Complete.txt:")
                for match in matches:
                    st.markdown(match, unsafe_allow_html=True)
            else:
                st.write("No matches found.")

# Run the main function
if __name__ == "__main__":
    main()
