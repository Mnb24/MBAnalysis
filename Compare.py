import streamlit as st
import difflib

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

def find_text_differences(file1_path, file2_path):
    differences = []  # Variable to store differences

    with open(file1_path, 'r', encoding='utf-8') as file1:
        text1 = file1.readlines()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        text2 = file2.readlines()

    differ = difflib.Differ()

    # Print the formatted differences with context
    for line_number, (sentence1, sentence2) in enumerate(zip(text1, text2), start=1):
        diff = list(differ.compare(sentence1.split(), sentence2.split()))
        formatted_diff = [(code, word) for item in diff for code, word in [(item[:1], item[2:])]]

        differences.append((line_number, print_colored_diff(formatted_diff)))

    return differences

# Streamlit UI
st.title("File Comparison App")

file1 = st.file_uploader("Upload File 1", type=["txt"])
file2 = st.file_uploader("Upload File 2", type=["txt"])

compare_button = st.button("Compare Files")

if compare_button:
    if file1 and file2:
        differences = find_text_differences(file1.name, file2.name)

        if differences:
            for line_number, (original, modified) in differences:
                st.markdown(f"### Line {line_number} - {file1.name}")
                st.markdown(f"#### Original")
                st.markdown(original, unsafe_allow_html=True)
                st.markdown(f"### Line {line_number} - {file2.name}")
                st.markdown(f"#### Modified")
                st.markdown(modified, unsafe_allow_html=True)
        else:
            st.write("No differences found.")
    else:
        st.write("Please upload both files before comparing.")


