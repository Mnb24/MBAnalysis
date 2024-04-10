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
def find_matches(target_phrases, br_text):
    lines = br_text.split('\n')
    matched_lines = []
    for line in lines:
        for phrase in target_phrases:
            if re.search(re.escape(phrase), line, flags=re.IGNORECASE):
                line = re.sub(re.escape(phrase), r'<span style="color:red">\g<0></span>', line, flags=re.IGNORECASE)
                matched_lines.append(line)
    return matched_lines

# Function to find partial matches (individual words) in the BR file
def find_partial_matches(target_phrases, br_text):
    words = re.findall(r'\b\w+\b', br_text.lower())  # Extract individual words from the text
    matched_words = set()
    for phrase in target_phrases:
        for word in words:
            if re.search(re.escape(word), phrase.lower()):
                matched_words.add(word)
    return matched_words

# Main function
def main():
    # Title and description
    st.title("Parallel Phrase Finder")
    st.write("Find matches for words/phrases entered in the second text box (referring the text in the sidebar) within the BORI edition.")

    # Fetching file contents
    mbtn_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt")
    br_complete_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")

    if mbtn_text is None or br_complete_text is None:
        st.error("Failed to fetch file contents. Please try again later.")
        return

    # Sidebar with text boxes
    st.sidebar.header("Text from Sastri Vavilla")
    selected_text = st.sidebar.text_area("SV", mbtn_text, height=400)
    
    target_phrases = st.sidebar.text_area("Enter phrases to find matches", height=200).strip().split('\n')

    # Button to find matches
    if st.sidebar.button("Find Matches"):
        # Exact Matches
        exact_matches = find_matches(target_phrases, br_complete_text)
        if exact_matches:
            st.header("Exact Matches Found in BORI edition:")
            for line in exact_matches:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.header("No exact matches found.")

        # Partial Matches
        partial_matches = find_partial_matches(target_phrases, br_complete_text)
        if partial_matches:
            st.header("Partial Matches Found in BORI edition:")
            st.write(", ".join(partial_matches))
        else:
            st.header("No partial matches found.")

# Run the main function
if __name__ == "__main__":
    main()
