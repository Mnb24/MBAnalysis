import streamlit as st
import requests
import re

# Function to fetch text from URL(s)
def fetch_text(urls):
    texts = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            texts.append(response.text)
        else:
            texts.append(None)
    return texts

# Function to find matches in the BR and KK files and highlight the target word by changing font color
def find_matches(target_phrases, texts):
    matched_lines = []
    for text in texts:
        lines = text.split('\n')
        for line in lines:
            for phrase in target_phrases:
                if re.search(re.escape(phrase), line, flags=re.IGNORECASE):
                    line = re.sub(re.escape(phrase), r'<span style="color:red">\g<0></span>', line, flags=re.IGNORECASE)
                    matched_lines.append(line)
    return matched_lines

# Main function
def main():
    # Title and description
    st.title("Parallel Phrase Finder")
    st.write("Find matches for words/phrases entered in the second text box (referring the text in the sidebar) within the BORI and KK editions.")

    # Fetching file contents
    texts = fetch_text([
        "https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt",
        "https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt"
    ])

    if None in texts:
        st.error("Failed to fetch file contents. Please try again later.")
        return

    # Sidebar with text boxes
    st.sidebar.header("Text from Sastri Vavilla")
    selected_text = st.sidebar.text_area("SV", height=400)
    
    target_phrases = st.sidebar.text_area("Enter phrases to find matches", height=200).strip().split('\n')

    # Button to find matches
    if st.sidebar.button("Find Matches"):
        matched_lines = find_matches(target_phrases, texts)
        if matched_lines:
            st.header("Matches Found in BORI and KK editions:")
            for line in matched_lines:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.header("No matches found.")

# Run the main function
if __name__ == "__main__":
    main()
