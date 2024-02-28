import streamlit as st
import requests

def perform_string_matching(files, target_string):
    st.write(f"String Matching Analysis for '{target_string}':")
    st.write("")

    # Iterate over each file
    for file_name, file_path in files.items():
        response = requests.get(file_path)
        lines = response.text.split('\n')

        st.write(f"Results from file: {file_name}")
        
        # Check each line for the target string
        for line_number, line in enumerate(lines, start=1):
            if target_string in line:
                # Highlight the target string with a color
                highlighted_line = line.replace(target_string, f"<span style='color: red'>{target_string}</span>")
                st.write(f"Line {line_number}: {highlighted_line}", unsafe_allow_html=True)

def main():
    # Displaying heading
    st.title("String Matcher")

    # Dictionary containing file names and their corresponding URLs
    files = {
        'BR': 'https://raw.githubusercontent.com/your_username/your_repository/main/file1.txt',
        'KK': 'https://raw.githubusercontent.com/your_username/your_repository/main/file2.txt',
        'SV': 'https://raw.githubusercontent.com/your_username/your_repository/main/file3.txt'
    }

    # Input field for the target string
    target_string = st.text_input("Enter the Devanagari string for string matching:", "")

    # Button to trigger the string matching analysis
    if st.button('Perform String Matching'):
        if target_string.strip() == "":
            st.warning("Please enter a valid Devanagari string.")
        else:
            perform_string_matching(files, target_string)

if __name__ == "__main__":
    main()

