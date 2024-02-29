import streamlit as st
import difflib
import requests

# Function to print colored differences between lines
def print_colored_diff(line):
    original_sentence = []
    modified_sentence = []

    for code, word in line:
        if code == ' ':
            original_sentence.append(word)
            modified_sentence.append(word)
        elif code == '-':
            original_sentence.append(f'<span style="color: blue">{word}</span>')
        elif code == '+':
            modified_sentence.append(f'<span style="color: red">{word}</span>')

    original_sentence = ' '.join(original_sentence)
    modified_sentence = ' '.join(modified_sentence)

    return f"Original: {original_sentence}", f"Modified: {modified_sentence}"

# Function to find text differences line by line
def find_text_differences(text1, text2):
    differences = []

    differ = difflib.Differ()

    # Print the formatted differences with context
    for line_number, (sentence1, sentence2) in enumerate(zip(text1, text2), start=1):
        diff = list(differ.compare(sentence1.split(), sentence2.split()))
        formatted_diff = [(code, word) for item in diff for code, word in [(item[:1], item[2:])]]

        differences.append((line_number, print_colored_diff(formatted_diff)))

    return differences

# Streamlit UI
st.title("File Comparison App")

# URLs of the text files
file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR_VS.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK_VS.txt'
]

compare_button = st.button("Compare Vishnu Sahasranama Files")

if compare_button:
    try:
        # Fetch content of File 1 from GitHub
        response1 = requests.get(file_paths[0])
        text1 = response1.text.splitlines()

        # Fetch content of File 2 from GitHub
        response2 = requests.get(file_paths[1])
        text2 = response2.text.splitlines()

        differences = find_text_differences(text1, text2)

        if differences:
            for line_number, (original, modified) in differences:
            st.markdown(f"### File1 - BORI" if 'BORI' in original else f"### File2 - Kumbakonam")
            st.markdown(f"#### {'Line ' + str(line_number) if 'BORI' in original else 'Line ' + str(line_number)}")
            st.markdown(original, unsafe_allow_html=True)
            st.markdown(f"### File2 - Kumbakonam" if 'Kumbakonam' in modified else f"### File1 - BORI")
            st.markdown(f"#### {'Line ' + str(line_number) if 'Kumbakonam' in modified else 'Line ' + str(line_number)}")
            st.markdown(modified, unsafe_allow_html=True)

        else:
            st.write("No differences found.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
