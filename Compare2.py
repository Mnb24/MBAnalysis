# Function to print colored differences between lines
def print_colored_diff(line, source):
    sentence = []

    for code, word in line:
        if code == ' ':
            sentence.append(word)
        elif code == '-' or code == '+':
            sentence.append(f'<span style="color: {"blue" if code == "-" else "red"}">{word}</span>')

    sentence = ' '.join(sentence)

    return f"{source}: {sentence}"

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
            differences_12 = find_text_differences([texts[0][line_number]], [texts[1][line_number]])
            differences_23 = find_text_differences([texts[1][line_number]], [texts[2][line_number]])
            differences_13 = find_text_differences([texts[0][line_number]], [texts[2][line_number]])

            # Print differences for each pair of files
            if differences_12:
                original, _ = differences_12[0][1]
                st.markdown(original, unsafe_allow_html=True)

            if differences_23:
                _, modified = differences_23[0][1]
                st.markdown(modified, unsafe_allow_html=True)

            if differences_13:
                original, _ = differences_13[0][1]
                st.markdown(original, unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
