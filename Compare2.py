# Function to print differences between lines
def print_diff(line, sources):
    sentences = []

    for source, code, word in line:
        if code == ' ':
            sentences.append((source, word))
        elif code == '-' or code == '+':
            sentences.append((source, f'<span style="color: {"blue" if code == "-" else "red"}">{word}</span>'))

    formatted_sentences = []
    for source, word in sentences:
        formatted_sentences.append(f"{source}: {word}")

    return formatted_sentences

# Function to find text differences line by line
def find_text_differences(texts, sources):
    differences = []

    differ = difflib.Differ()

    # Print the formatted differences with context
    for line_number, sentences in enumerate(zip(*texts), start=1):
        formatted_diffs = []
        for i, (sentence1, sentence2) in enumerate(combinations(sentences, 2)):
            diff = list(differ.compare(sentence1.split(), sentence2.split()))
            formatted_diff = [(sources[i], code, word) for item in diff for code, word in [(item[:1], item[2:])]]
            formatted_diffs.append(formatted_diff)

        differences.append((line_number, print_diff(formatted_diffs, sources)))

    return differences

# Streamlit UI
st.title("File Comparison App")

# URLs of the text files and their respective sources
file_paths = [
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR_VS.txt', 
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK_VS.txt',
    'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/SV_VS.txt'
]
sources = ["BORI", "Kumbakonam", "Sastri Vavilla"]

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
            differences = find_text_differences([text[line_number] for text in texts], sources)

            # Print differences for each line
            for line_num, diffs in differences:
                st.markdown(f"<h3>Line {line_num}</h3>", unsafe_allow_html=True)
                for diff in diffs:
                    st.markdown(' '.join(diff), unsafe_allow_html=True)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

