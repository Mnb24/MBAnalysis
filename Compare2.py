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
def find_text_differences(text1, text2, text3):
    differences = []

    differ = difflib.Differ()

    # Print the formatted differences with context
    for line_number, (sentence1, sentence2, sentence3) in enumerate(zip(text1, text2, text3), start=1):
        diff1 = list(differ.compare(sentence1.split(), sentence2.split()))
        diff2 = list(differ.compare(sentence1.split(), sentence3.split()))

        formatted_diff1 = [(code, word) for item in diff1 for code, word in [(item[:1], item[2:])]]
        formatted_diff2 = [(code, word) for item in diff2 for code, word in [(item[:1], item[2:])]]

        differences.append((line_number, print_colored_diff(formatted_diff1), print_colored_diff(formatted_diff2)))

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

        # Compare 1st and 2nd files
        differences_12 = find_text_differences(texts[0], texts[1])

        if differences_12:
            for line_number, (original, modified) in differences_12:
                st.markdown(f"### File1 - BORI")
                st.markdown(f"#### Line {line_number}")
                st.markdown(original, unsafe_allow_html=True)
                st.markdown(f"### File2 - Kumbakonam")
                st.markdown(f"#### Line {line_number}")
                st.markdown(modified, unsafe_allow_html=True)
        else:
            st.write("No differences found between File1 and File2.")

        # Compare 2nd and 3rd files
        differences_23 = find_text_differences(texts[1], texts[2])

        if differences_23:
            for line_number, (original, modified) in differences_23:
                st.markdown(f"### File2 - Kumbakonam")
                st.markdown(f"#### Line {line_number}")
                st.markdown(original, unsafe_allow_html=True)
                st.markdown(f"### File3 - Sastri Vavilla")
                st.markdown(f"#### Line {line_number}")
                st.markdown(modified, unsafe_allow_html=True)
        else:
            st.write("No differences found between File2 and File3.")

        # Compare 1st and 3rd files
        differences_13 = find_text_differences(texts[0], texts[2])

        if differences_13:
            for line_number, (original, modified) in differences_13:
                st.markdown(f"### File1 - BORI")
                st.markdown(f"#### Line {line_number}")
                st.markdown(original, unsafe_allow_html=True)
                st.markdown(f"### File3 - Sastri Vavilla")
                st.markdown(f"#### Line {line_number}")
                st.markdown(modified, unsafe_allow_html=True)
        else:
            st.write("No differences found between File1 and File3.")
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

      
