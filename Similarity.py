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

# Function to find exact matches and partial matches in the BR file
def find_matches(target_phrases, br_text):
    exact_matched_lines = []
    partial_matched_lines = []
    lines = br_text.split('\n')
    for line in lines:
        exact_matched = False
        partial_matched = False
        for phrase in target_phrases:
            if re.search(re.escape(phrase), line, flags=re.IGNORECASE):
                line_highlighted = re.sub(re.escape(phrase), r'<span style="color:red">\g<0></span>', line, flags=re.IGNORECASE)
                if re.match(re.escape(phrase), line, flags=re.IGNORECASE):
                    exact_matched = True
                else:
                    partial_matched = True
                line = line_highlighted
        if exact_matched:
            exact_matched_lines.append(line)
        elif partial_matched:
            partial_matched_lines.append(line)
    return exact_matched_lines, partial_matched_lines

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
        exact_matched_lines, partial_matched_lines = find_matches(target_phrases, br_complete_text)
        if exact_matched_lines:
            st.header("Exact Matches Found in BORI edition:")
            for line in exact_matched_lines:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.header("No exact matches found.")
        
        if partial_matched_lines:
            st.header("Partial Matches Found in BORI edition:")
            for line in partial_matched_lines:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.header("No partial matches found.")

# Run the main function
if __name__ == "__main__":
    main()
