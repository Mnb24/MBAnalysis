import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def perform_string_matching(files, target_word):
    st.write(f"String Matching Analysis for '{target_word}':")
    st.write("")

    occurrences = {file_name: 0 for file_name in files.keys()}  # Dictionary to store occurrences per file

    # Count occurrences in each file
    for file_name, file_path in files.items():
        response = requests.get(file_path)
        lines = response.text.split('\n')

        # Check each line for the target word
        for line in lines:
            if target_word in line:
                occurrences[file_name] += 1

    # Create DataFrame for word distribution
    df = pd.DataFrame(list(occurrences.items()), columns=['File', 'Occurrences'])

    # Plot word distribution
    st.write("Word Distribution:")
    st.bar_chart(df.set_index('File'))

    st.write("")  # Empty line for spacing

    # Display results for each file
    st.write("Results:")
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

def main():
    # Displaying heading
    st.title("String-Matching Tool (Adi Parva)")

    files = {
         'BD':'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
         'KMG':'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
         'MND':'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
    }

    # Input field for the target word
    target_word = st.text_input("Enter the word for string matching:", "")

    # Button to trigger the string matching analysis
    if st.button('Perform String Matching'):
        if target_word.strip() == "":
            st.warning("Please enter a valid word.")
        else:
            perform_string_matching(files, target_word)

if __name__ == "__main__":
    main()

