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
    diff = differ.compare(text1.split(), text2.split())
    formatted_diff = [(code, word) for item in diff for code, word in [(item[:1], item[2:])]]

    differences.append((1, print_colored_diff(formatted_diff)))

    return differences

# Streamlit UI
st.title("File Comparison App")

# Vishnu Sahasranama URLs
vishnu_sahasranama_file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR_VS.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK_VS.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV_VS.txt'
]

# Bhagavad Gita URLs
bhagavad_gita_file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-BR.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-KK.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BG-SV.txt'
]

compare_vishnu_button = st.button("Compare Vishnu Sahasranama Versions")
compare_bhagavad_button = st.button("Compare Bhagavad Gita Versions")

if compare_vishnu_button:
    try:
        for i in range(len(vishnu_sahasranama_file_paths)-1):
            response1 = requests.get(vishnu_sahasranama_file_paths[i])
            response2 = requests.get(vishnu_sahasranama_file_paths[i+1])
            
            text1 = response1.text
            text2 = response2.text
            
            differences = find_text_differences(text1, text2)
            if differences:
                sentence1, sentence2 = differences[0][1]
                st.markdown(f"File{i+1} - BORI")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown(f"File{i+2} - Kumbakonam")
                st.markdown(sentence2, unsafe_allow_html=True)
        
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

if compare_bhagavad_button:
    try:
        for i in range(len(bhagavad_gita_file_paths)-1):
            response1 = requests.get(bhagavad_gita_file_paths[i])
            response2 = requests.get(bhagavad_gita_file_paths[i+1])
            
            text1 = response1.text
            text2 = response2.text
            
            differences = find_text_differences(text1, text2)
            if differences:
                sentence1, sentence2 = differences[0][1]
                st.markdown(f"File{i+1} - BORI")
                st.markdown(sentence1, unsafe_allow_html=True)
                st.markdown(f"File{i+2} - Kumbakonam")
                st.markdown(sentence2, unsafe_allow_html=True)
        
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
