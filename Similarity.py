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

# Function to find matches in the BR file and highlight the target word by changing font color
def find_matches(target_words, br_text):
    lines = br_text.split('\n')
    matched_lines = []
    for line in lines:
        if all(re.search(r'\b' + word + r'\b', line, flags=re.IGNORECASE) for word in target_words):
            for word in target_words:
                line = re.sub(r'\b(' + word + r')\b', r'<span style="color:red">\1</span>', line, flags=re.IGNORECASE)
            matched_lines.append(line)
    return matched_lines

# Main function
def main():
    # Title and description
    st.title("File Similarity Finder")
    st.write("This app allows you to find matches for words/phrases entered in the second text box (referring the text in the sidebar) within the BORI edition.")

    # Fetching file contents
    mbtn_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt")
    br_complete_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    if mbtn_text is None or br_complete_text is None:
        st.error("Failed to fetch file contents. Please try again later.")
        return

    # Sidebar with text boxes
    st.sidebar.header("Text from Sastri Vavilla")

    target_words = st.sidebar.text_area("Enter words to find matches", height=200).split()

    # Button to find matches
    if st.sidebar.button("Find Matches"):
        matched_lines = find_matches(target_words, br_complete_text)
        if matched_lines:
            st.header("Matches Found in BORI edition:")
            for line in matched_lines:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.header("No matches found.")

# Run the main function
if __name__ == "__main__":
    main()
