import streamlit as st
import requests

def perform_string_matching(files, target_string):
    st.write(f"String Matching Analysis for '{target_string}':")
    st.write("")

    # Open files and read lines
    file_data = {}
    for file_name, file_path in files.items():
        response = requests.get(file_path)
        lines = response.text.split('\n')
        file_data[file_name] = lines

    # Initialize index for each file
    line_indices = {file_name: 0 for file_name in files}

    # Process lines in groups of three occurrences
    occurrences_count = 0
    while True:
        group_found = False
        for file_name, lines in file_data.items():
            line_index = line_indices[file_name]
            if line_index < len(lines):
                line = lines[line_index]
                line_indices[file_name] += 1
                if target_string in line:
                    # Highlight the target string with a color
                    highlighted_line = line.replace(target_string, f"<span style='color: red'>{target_string}</span>")
                    st.write(f"From {file_name} - {highlighted_line}", unsafe_allow_html=True)
                    group_found = True
                    occurrences_count += 1
        
        # Add *** after each group of three occurrences
        if occurrences_count % 3 == 0:
            st.write("***")
        
        # Exit the loop if no occurrences are found
        if not group_found:
            break

def main():
    # Displaying heading
    st.title("String Matcher")

    # Dictionary containing file names and their corresponding URLs
    files = {
        'BR': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-01-Complete.txt',
        'KK': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-01-Complete.txt',
        'SV': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-01-Complete.txt'
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
