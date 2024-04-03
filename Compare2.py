import streamlit as st
import difflib
import requests

# Function to print colored differences between sentences
def print_colored_diff(sentence1, sentence2):
    colored_sentence1 = ''
    colored_sentence2 = ''

    differ = difflib.Differ()
    diff = list(differ.compare(sentence1.split(), sentence2.split()))

    for item in diff:
        code = item[:1]
        word = item[2:]
        if code == ' ':
            colored_sentence1 += word + ' '
            colored_sentence2 += word + ' '
        elif code == '+':
            colored_sentence1 += f'<span style="color: blue">{word}</span> '
        elif code == '-':
            colored_sentence2 += f'<span style="color: red">{word}</span> '

    return colored_sentence1, colored_sentence2

# Function to find text differences sentence by sentence
def find_text_differences(text1, text2):
    differences = []

    differ = difflib.Differ()

    # Print the formatted differences with context
    diff = list(differ.compare(text1.splitlines(keepends=True), text2.splitlines(keepends=True)))
    formatted_diff = [(code, word) for item in diff for code, word in [(item[:1], item[2:])]]

    differences.append(print_colored_diff(text1, text2))

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
        texts = [response.text for response in responses]

        # Compare sentences from each pair of files
        sentences_12 = difflib.ndiff(texts[0].splitlines(keepends=True), texts[1].splitlines(keepends=True))
        sentences_23 = difflib.ndiff(texts[1].splitlines(keepends=True), texts[2].splitlines(keepends=True))
        sentences_13 = difflib.ndiff(texts[0].splitlines(keepends=True), texts[2].splitlines(keepends=True))

        # Print differences for each pair of files
        for diff_12, diff_23, diff_13 in zip(sentences_12, sentences_23, sentences_13):
            if diff_12.startswith('-') or diff_12.startswith('+'):
                sentence1, sentence2 = diff_12[2:], diff_23[2:] if diff_23.startswith((' ', '+')) else diff_13[2:]
                st.markdown(f"File1 - BORI: {sentence1}", unsafe_allow_html=True)
                st.markdown(f"File2 - Kumbakonam: {sentence2}", unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

if compare_gita_button:
    try:
        # Fetch content of Bhagavad Gita files from GitHub
        responses = [requests.get(file_path) for file_path in bhagavad_gita_file_paths]
        texts = [response.text for response in responses]

        # Compare sentences from each pair of files
        sentences_12 = difflib.ndiff(texts[0].splitlines(keepends=True), texts[1].splitlines(keepends=True))
        sentences_23 = difflib.ndiff(texts[1].splitlines(keepends=True), texts[2].splitlines(keepends=True))
        sentences_13 = difflib.ndiff(texts[0].splitlines(keepends=True), texts[2].splitlines(keepends=True))

        # Print differences for each pair of files
        for diff_12, diff_23, diff_13 in zip(sentences_12, sentences_23, sentences_13):
            if diff_12.startswith('-') or diff_12.startswith('+'):
                sentence1, sentence2 = diff_12[2:], diff_23[2:] if diff_23.startswith((' ', '+')) else diff_13[2:]
                st.markdown(f"File1 - BORI: {sentence1}", unsafe_allow_html=True)
                st.markdown(f"File2 - Kumbakonam: {sentence2}", unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
