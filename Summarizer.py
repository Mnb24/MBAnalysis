import re
import streamlit as st
from transformers import pipeline

summarizer = pipeline("summarization")

def summarize_section(text, max_length=250, min_length=30, do_sample=False):
    if len(text.split()) > 1024:
        return "Words exceed input limit."

    # Generate the summary
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample)[0]['summary_text']
    return summary

num_files = st.number_input("Enter the number of files:", min_value=1, step=1)
file_names = []
for i in range(num_files):
    file_name = st.text_input(f"Enter the name of file {i+1}: ")
    file_names.append(file_name)

section_number = st.number_input("Enter the section number: ", min_value=1, step=1)

st.write("\nSummaries for each file:\n")
for file_name in file_names:
    # Read the content of the file
    with open(file_name, 'r') as file:
        content = file.read()

    # Use regular expressions to find sections based on the section number
    pattern = rf"Section\s+{section_number}\b([\s\S]+?)(?=(Section\s+\d+|$))"
    match = re.search(pattern, content)

    if match:
        section_content = match.group(1).strip()

        # Summarize the section
        summary = summarize_section(section_content)

        # Check if the summary is an error message
        if summary == "Words exceed input limit.":
            st.write("Error: Words exceed input limit.")
        else:
            # Split the summary at each full stop and print each sentence on a new line
            st.write(f"Summary of Section {section_number} in {file_name}:")
            sentences = summary.split(".")
            for sentence in sentences:
                st.write(sentence.strip() + ".")
            st.write("-" * 50)
    else:
        st.write(f"Section {section_number} not found in {file_name}.")
