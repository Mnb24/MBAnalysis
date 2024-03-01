import streamlit as st
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization")

def summarize_section(text, max_length=250, min_length=30, do_sample=False):
    # Truncate the input text to fit within the maximum sequence length
    if len(text) > 1000:
        text = text[:1000]  # Truncate the text if it exceeds 1000 characters

    # Adjust the max_length parameter based on the length of the input text
    max_length = min(max_length, len(text) // 2)  # Set max_length to half of the input length

    # Generate the summary
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample)[0]['summary_text']
    return summary

# Streamlit UI
st.title("Text Summarizer")

# User input for the number of files
num_files = st.number_input("Enter the number of files:", min_value=1, step=1)

# Initialize an empty list to store file names
file_names = []

# Prompt for file names and store them in the list
for i in range(num_files):
    file_name = st.text_input(f"Enter the name of file {i + 1}: ")
    file_names.append(file_name)

# Accept user input for the section number
section_number = st.number_input("Enter the section number:", min_value=0, step=1)

# Iterate over each file
for file_name in file_names:
    st.write(f"\nSummarizing {file_name}:")

    # Initialize an empty string to store the content of the specified section
    section_content = ""

    # Read the content of the specified section from the text file
    with open(file_name, 'r') as file:
        # Read the file in chunks to handle larger files
        for chunk in iter(lambda: file.read(4096), ''):
            section_content += chunk

    # Split the content into sections based on the "Section" keyword
    sections = section_content.split("Section")

    # Check if the section number is valid
    if section_number < 0 or section_number >= len(sections):
        st.write("Section not found.")
    else:
        # Extract the specified section
        section_content = sections[section_number]

        # Summarize the section
        summary = summarize_section(section_content)

        # Split the summary at each full stop and print each sentence on a new line
        st.write(f"Summary of Section {section_number}:")
        sentences = summary.split(".")
        for sentence in sentences:
            st.write(sentence.strip() + ".")
