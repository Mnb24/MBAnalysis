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
            line_highlighted = line
            for word in target_words:
                line_highlighted = re.sub(r'\b(' + word + r')\b', r'<span style="color:red">\1</span>', line_highlighted, flags=re.IGNORECASE)
            matched_lines.append(line_highlighted)
    return matched_lines

# Main function
def main():
    # Title and description
    st.title("File Similarity Finder")
    st.write("This app allows you to find matches for words entered in the second text box within the content of the BR file.")

    # Fetching file contents
    mbtn_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MBTN.txt")
    br_complete_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    if mbtn_text is None or br_complete_text is None:
        st.error("Failed to fetch file contents. Please try again later.")
        return

    # Sidebar with text boxes
    st.sidebar.header("Text from File 1 (MBTN.txt)")
    st.sidebar.text_area("Selected Text", mbtn_text, height=400)

    target_words = st.sidebar.text_area("Enter words to find matches (separated by spaces)", height=200).split()

    # Button to find matches
    if st.sidebar.button("Find Matches"):
        if len(target_words) < 2:
            st.warning("Please enter at least two words to find matches.")
            return
        matched_lines = find_matches(target_words, br_complete_text)
        if matched_lines:
            st.header("Matches Found in BR File:")
            for line in matched_lines:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.header("No matches found.")

# Run the main function
if __name__ == "__main__":
    main()

