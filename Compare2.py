import streamlit as st
import difflib
import requests

# Function to print colored differences between lines
def print_colored_diff(line):
    First_sentence = []
    Second_sentence = []

    for code, word in line:
        if code == ' ':
            First_sentence.append(word)
            Second_sentence.append(word)
        elif code == '-':
            First_sentence.append(f'<span style="color: blue">{word}</span>')
        elif code == '+':
            Second_sentence.append(f'<span style="color: red">{word}</span>')

    First_sentence = ' '.join(First_sentence)
    Second_sentence = ' '.join(Second_sentence)

    return f"First: {First_sentence}", f"Second: {Second_sentence}"

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

        # Get the number of lines in the shortest file
        min_lines = min(len(text) for text in texts)

        # Compare lines from each pair of files
        for line_number in range(min_lines):
            differences_12 = find_text_differences([texts[0][line_number]], [textsFirst[line_number]])
            differences_23 = find_text_differences([textsFirst[line_number]], [textsSecond[line_number]])
            differences_13 = find_text_differences([texts[0][line_number]], [textsSecond[line_number]])

            # Print differences for each pair of files
            if differences_12:
                First, Second = differences_12[0]First
                st.markdown(f"<h3>Line {line_number + 1}</h3>", unsafe_allow_html=True)
                st.markdown("<h4>File1 - BORI</h4>", unsafe_allow_html=True)
                st.markdown(First, unsafe_allow_html=True)
                st.markdown("<h4>File2 - Kumbakonam</h4>", unsafe_allow_html=True)
                st.markdown(Second, unsafe_allow_html=True)

            if differences_23:
                First, Second = differences_23[0]First
                st.markdown(f"<h3>Line {line_number + 1}</h3>", unsafe_allow_html=True)
                st.markdown("<h4>File2 - Kumbakonam</h4>", unsafe_allow_html=True)
                st.markdown(First, unsafe_allow_html=True)
                st.markdown("<h4>File3 - Sastri Vavilla</h4>", unsafe_allow_html=True)
                st.markdown(Second, unsafe_allow_html=True)

            if differences_13:
                First, Second = differences_13[0]First
                st.markdown(f"<h3>Line {line_number + 1}</h3>", unsafe_allow_html=True)
                st.markdown("<h4>File1 - BORI</h4>", unsafe_allow_html=True)
                st.markdown(First, unsafe_allow_html=True)
                st.markdown("<h4>File3 - Sastri Vavilla</h4>", unsafe_allow_html=True)
                st.markdown(Second, unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
