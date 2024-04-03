import streamlit as st
import difflib
import requests

# Function to print colored differences between sentences
def print_colored_diff(sentence1, sentence2):
    colored_sentence1 = ''
    colored_sentence2 = ''

    differ = difflib.Differ()
    diff = list(differ.compare(sentence1, sentence2))

    for item in diff:
        code = item[:1]
        word = item[2:]
        if code == ' ':
            colored_sentence1 += word
            colored_sentence2 += word
        elif code == '+':
            colored_sentence1 += f'<span style="color: blue">{word}</span>'
        elif code == '-':
            colored_sentence2 += f'<span style="color: red">{word}</span>'

    return colored_sentence1, colored_sentence2

# Function to find text differences line by line
def find_text_differences(text1, text2):
    differences = []

    differ = difflib.Differ()

    # Print the formatted differences with context
    for line_number, (sentence1, sentence2) in enumerate(zip(text1, text2), start=1):
        diff = list(differ.compare(sentence1.split(), sentence2.split()))
        formatted_diff = [(code, word) for item in diff for code, word in [(item[:1], item[2:])]]

        differences.append((line_number, print_colored_diff(sentence1, sentence2)))

    return differences

# Streamlit UI
st.title("File Comparison App")

# URLs of the text files
file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR_VS.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK_VS.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV_VS.txt'
]

# URLs of the Bhagavad Gita files
bhagavad_gita_file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-BR.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-KK.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-SV.txt'
]

compare_button = st.button("Compare Vishnu Sahasranama Files")
compare_gita_button = st.button("Compare Bhagavad Gita Versions")

if compare_button:
    try:
        # Fetch content of files from GitHub
        responses = [requests.get(file_path) for file_path in file_paths]
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
                st.markdown(f"File1 - BORI: {sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown(f"File2 - Kumbakonam: {sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_23:
                sentence1, sentence2 = differences_23[0][1]
                st.markdown(f"File2 - Kumbakonam: {sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown(f"File3 - Sastri Vavilla: {sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_13:
                sentence1, sentence2 = differences_13[0][1]
                st.markdown(f"File1 - BORI: {sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown(f"File3 - Sastri Vavilla: {sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            st.markdown("*****")

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

if compare_gita_button:
    try:
        # Fetch content of Bhagavad Gita files from GitHub
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
                st.markdown(f"File1 - BORI: {sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown(f"File2 - Kumbakonam: {sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_23:
                sentence1, sentence2 = differences_23[0][1]
                st.markdown(f"File2 - Kumbakonam: {sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown(f"File3 - Sastri Vavilla: {sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            if differences_13:
                sentence1, sentence2 = differences_13[0][1]
                st.markdown(f"File1 - BORI: {sentence1} (line {line_number + 1})", unsafe_allow_html=True)
                st.markdown(f"File3 - Sastri Vavilla: {sentence2} (line {line_number + 1})", unsafe_allow_html=True)

            st.markdown("*****")

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

