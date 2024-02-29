import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def perform_string_matching(files, target_word):
    st.write(f"String Matching Analysis for '{target_word}':")
    st.write("")

    occurrences = {file_name: 0 for file_name in files.keys()}  # Dictionary to store occurrences per file

    # Iterate over each file
    for file_name, file_path in files.items():
        response = requests.get(file_path)
        lines = response.text.split('\n')

        st.write(f"Results from file: {file_name}")

        # Check each line for the target word
        for line_number, line in enumerate(lines, start=1):
            if target_word in line:
                # Highlight the target word with a color
                highlighted_line = line.replace(target_word, f"<span style='color: red'>{target_word}</span>")
                st.write(f"Line {line_number}: {highlighted_line}", unsafe_allow_html=True)
                occurrences[file_name] += 1

    # Create DataFrame for word distribution
    df = pd.DataFrame(list(occurrences.items()), columns=['File', 'Occurrences'])

    # Plot word distribution
    st.bar_chart(df.set_index('File'))

def main():
    # Displaying heading
    st.title("String Matcher")

    files = {
        'BR': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-01-Complete.txt',
        'KK': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-01-Complete.txt',
        'SV': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV-01-Complete.txt'
    }

    # Input field for the target word
    target_word = st.text_input("Enter the Devanagari word for string matching:", "")

    # Button to trigger the string matching analysis
    if st.button('Perform String Matching'):
        if target_word.strip() == "":
            st.warning("Please enter a valid Devanagari word.")
        else:
            perform_string_matching(files, target_word)

if __name__ == "__main__":
    main()