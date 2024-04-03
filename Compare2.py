import streamlit as st
import difflib
import requests

# Function to print colored differences between lines
def print_colored_diff(sentence1, sentence2):
    colored_sentence1 = ''
    colored_sentence2 = ''

    for char1, char2 in zip(sentence1, sentence2):
        if char1 == char2:
            colored_sentence1 += char1
            colored_sentence2 += char2
        else:
            colored_sentence1 += f'<span style="color: blue">{char1}</span>'
            colored_sentence2 += f'<span style="color: red">{char2}</span>'

    return colored_sentence1, colored_sentence2

# Function to find text differences character by character
def find_text_differences(text1, text2):
    differences = []

    differ = difflib.Differ()

    # Print the formatted differences with context
    diff = differ.compare(text1, text2)
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

        # Get the number of characters in the shortest file
        min_chars = min(len(text) for text in texts)

        # Compare characters from each pair of files
        for char_index in range(min_chars):
            differences_12 = find_text_differences(texts[0][char_index], texts[1][char_index])
            differences_23 = find_text_differences(texts[1][char_index], texts[2][char_index])
            differences_13 = find_text_differences(texts[0][char_index], texts[2][char_index])

            # Print differences for each pair of files
            if differences_12:
                sentence1, sentence2 = differences_12[0]
                st.markdown("File1 - BORI")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown("File2 - Kumbakonam")
                st.markdown(sentence2, unsafe_allow_html=True)

            if differences_23:
                sentence1, sentence2 = differences_23[0]
                st.markdown("File2 - Kumbakonam")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(sentence2, unsafe_allow_html=True)

            if differences_13:
                sentence1, sentence2 = differences_13[0]
                st.markdown("File1 - BORI")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(sentence2, unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

if compare_gita_button:
    try:
        # Fetch content of Bhagavad Gita files from GitHub
        responses = [requests.get(file_path) for file_path in bhagavad_gita_file_paths]
        texts = [response.text for response in responses]

        # Get the number of characters in the shortest file
        min_chars = min(len(text) for text in texts)

        # Compare characters from each pair of files
        for char_index in range(min_chars):
            differences_12 = find_text_differences(texts[0][char_index], texts[1][char_index])
            differences_23 = find_text_differences(texts[1][char_index], texts[2][char_index])
            differences_13 = find_text_differences(texts[0][char_index], texts[2][char_index])

            # Print differences for each pair of files
            if differences_12:
                sentence1, sentence2 = differences_12[0]
                st.markdown("File1 - BORI")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown("File2 - Kumbakonam")
                st.markdown(sentence2, unsafe_allow_html=True)

            if differences_23:
                sentence1, sentence2 = differences_23[0]
                st.markdown("File2 - Kumbakonam")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(sentence2, unsafe_allow_html=True)

            if differences_13:
                sentence1, sentence2 = differences_13[0]
                st.markdown("File1 - BORI")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown("File3 - Sastri Vavilla")
                st.markdown(sentence2, unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
