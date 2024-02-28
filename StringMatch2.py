import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to perform string matching
def perform_string_matching(files, target_word):
    st.write(f"String Matching Analysis for '{target_word}':")
    st.write("")

    # Dataframe to store occurrences of the target word in each file
    df = pd.DataFrame(columns=['File', 'Occurrences'])

    # Iterate over each file
    for file_name, file_path in files.items():
        response = requests.get(file_path)
        lines = response.text.split('\n')

        st.write(f"Results from file: {file_name}")
        st.write("")

        # Count occurrences and store lines
        occurrences = 0
        lines_with_occurrences = []
        for line_number, line in enumerate(lines, start=1):
            if target_word in line:
                # Highlight the target word with a color
                highlighted_line = line.replace(target_word, f"<span style='color: red'>{target_word}</span>")
                st.write(f"Line {line_number}: {highlighted_line}", unsafe_allow_html=True)
                occurrences += 1
                lines_with_occurrences.append(line)

        # Update the dataframe with occurrences
        df = df.append({'File': file_name, 'Occurrences': occurrences}, ignore_index=True)
        st.write("")

        # Print total occurrences in the file
        st.write(f"Total occurrences in {file_name}: {occurrences}")
        st.write("")

    # Display bar plot of word distribution across files
    st.write("Word Distribution Across Files:")
    plt.figure(figsize=(8, 6))
    plt.bar(df['File'], df['Occurrences'], color='skyblue')
    plt.xlabel('Files')
    plt.ylabel('Occurrences')
    plt.title('Word Distribution')
    st.pyplot()

def main():
    # Displaying heading
    st.title("Devanagari String Matcher")
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
