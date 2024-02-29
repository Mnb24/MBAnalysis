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
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK_VS.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV_VS.txt'
]

compare_button = st.button("Compare Vishnu Sahasranama Files")

if compare_button:
    try:
        # Fetch content of files from GitHub
        responses = [requests.get(file_path) for file_path in file_paths]
        texts = [response.text.splitlines() for response in responses]

        # Determine the maximum number of lines among the files
        max_lines = max(len(text) for text in texts)

        for line_number in range(max_lines):
            st.markdown(f"### Line {line_number + 1}")

            # Compare line from File 1 and File 2
            if line_number < len(texts[0]) and line_number < len(texts[1]):
                differences_12 = find_text_differences([texts[0][line_number]], [texts[1][line_number]])
                if differences_12:
                    for original, modified in differences_12:
                        st.markdown(f"#### File1 - BORI")
                        st.markdown(original, unsafe_allow_html=True)
                        st.markdown(f"#### File2 - Kumbakonam")
                        st.markdown(modified, unsafe_allow_html=True)
            
            # Compare line from File 2 and File 3
            if line_number < len(texts[1]) and line_number < len(texts[2]):
                differences_23 = find_text_differences([texts[1][line_number]], [texts[2][line_number]])
                if differences_23:
                    for original, modified in differences_23:
                        st.markdown(f"#### File2 - Kumbakonam")
                        st.markdown(original, unsafe_allow_html=True)
                        st.markdown(f"#### File3 - Sastri Vavilla")
                        st.markdown(modified, unsafe_allow_html=True)

            # Compare line from File 1 and File 3
            if line_number < len(texts[0]) and line_number < len(texts[2]):
                differences_13 = find_text_differences([texts[0][line_number]], [texts[2][line_number]])
                if differences_13:
                    for original, modified in differences_13:
                        st.markdown(f"#### File1 - BORI")
                        st.markdown(original, unsafe_allow_html=True)
                        st.markdown(f"#### File3 - Sastri Vavilla")
                        st.markdown(modified, unsafe_allow_html=True)
            
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")


      
