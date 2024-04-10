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

# Function to find matches in the BR and KK files and highlight the target word by changing font color
def find_matches(target_phrases, br_text, kk_text):
    texts = {'BORI edition': br_text, 'KK edition': kk_text}
    matched_lines = {name: [] for name in texts.keys()}
    for name, text in texts.items():
        lines = text.split('\n')
        for line in lines:
            for phrase in target_phrases:
                if re.search(re.escape(phrase), line, flags=re.IGNORECASE):
                    line = re.sub(re.escape(phrase), r'<span style="color:red">\g<0></span>', line, flags=re.IGNORECASE)
                    matched_lines[name].append(line)
    return matched_lines

# Main function
def main():
    # Title and description
    st.title("Parallel Phrase Finder")
    st.write("Find matches for words/phrases entered in the second text box (referring the text in the sidebar) within the BORI and KK editions.")

    # Fetching file contents
    mbtn_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-Complete.txt")
    br_complete_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt")
    kk_complete_text = fetch_text("https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt")

    if mbtn_text is None or br_complete_text is None or kk_complete_text is None:
        st.error("Failed to fetch file contents. Please try again later.")
        return

    # Sidebar with text boxes
    st.sidebar.header("Text from Sastri Vavilla")
    selected_text = st.sidebar.text_area("SV", mbtn_text, height=400)
    
    target_phrases = st.sidebar.text_area("Enter phrases to find matches", height=200).strip().split('\n')

    # Button to find matches
    if st.sidebar.button("Find Matches"):
        matched_lines = find_matches(target_phrases, br_complete_text, kk_complete_text)
        for name, lines in matched_lines.items():
            if lines:
                st.header(f"Matches Found in {name}:")
                for line in lines:
                    st.markdown(line, unsafe_allow_html=True)
            else:
                st.header(f"No matches found in {name}.")

# Run the main function
if __name__ == "__main__":
    main()
