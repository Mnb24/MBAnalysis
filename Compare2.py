import streamlit as st
import difflib
import requests

# Function to print colored differences between lines
def print_colored_diff(line):
    sentence1 = []
    sentence2 = []

    for code, word in line:
        if code == ' ':
            sentence1.append(word)
            sentence2.append(word)
        elif code == '-':
            sentence1.append(f'<span style="color: blue">{word}</span>')
        elif code == '+':
            sentence2.append(f'<span style="color: red">{word}</span>')

    sentence1 = ' '.join(sentence1)
    sentence2 = ' '.join(sentence2)

    return sentence1, sentence2

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
vishnu_sahasranama_file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR_VS.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK_VS.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV_VS.txt'
]

bhagavad_gita_file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-BR.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-KK.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-SV.txt'
]

compare_vishnu_button = st.button("Compare Vishnu Sahasranama Versions")
compare_bhagavad_button = st.button("Compare Bhagavad Gita Versions")

if compare_vishnu_button:
    try:
        # Fetch content of files from GitHub
        responses = [requests.get(file_path) for file_path in vishnu_sahasranama_file_paths]
        texts = [response.text.splitlines() for response in responses]

        # Get the number of lines in the shortest file
        min_lines = min(len(text) for text in texts)

        # Compare lines from each pair of files
        for line_number in range(min_lines):
            differences_12 = find_text_differences([texts[0][line_number]], [texts[1][line_number]])
            differences_23 = find_text_differences([texts[1][line_number]], [texts[2][line_number]])
            differences_13 = find_text_differences([texts[0][line_number]], [texts[2][line_number]])

            # Print differences for each pair of files
            if differences_12:
                sentence1, sentence2 = differences_12[0][1]
                st.markdown("File1 - BORI")
                st.markdown(f"{sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown("File2 - Kumbakonam")
                st.markdown(f"{sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_23:
                sentence1, sentence2 = differences_23[0][1]
                st.markdown("File2 - Kumbakonam")
                st.markdown(f"{sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(f"{sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_13:
                sentence1, sentence2 = differences_13[0][1]
                st.markdown("File1 - BORI")
                st.markdown(f"{sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(f"{sentence2} (line {line_number + 1})", unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

if compare_bhagavad_button:
    try:
        # Fetch content of files from GitHub
        responses = [requests.get(file_path) for file_path in bhagavad_gita_file_paths]
        texts = [response.text.splitlines() for response in responses]

        # Get the number of lines in the shortest file
        min_lines = min(len(text) for text in texts)

        # Compare lines from each pair of files
        for line_number in range(min_lines):
            differences_12 = find_text_differences([texts[0][line_number]], [texts[1][line_number]])
            differences_23 = find_text_differences([texts[1][line_number]], [texts[2][line_number]])
            differences_13 = find_text_differences([texts[0][line_number]], [texts[2][line_number]])

            # Print differences for each pair of files
            if differences_12:
                sentence1, sentence2 = differences_12[0][1]
                st.markdown("File1 - BORI")
                st.markdown(f"{sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown("File2 - Kumbakonam")
                st.markdown(f"{sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_23:
                sentence1, sentence2 = differences_23[0][1]
                st.markdown("File2 - Kumbakonam")
                st.markdown(f"{sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(f"{sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_13:
                sentence1, sentence2 = differences_13[0][1]
                st.markdown("File1 - BORI")
                st.markdown(f"{sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(f"{sentence2} (line {line_number + 1})", unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
