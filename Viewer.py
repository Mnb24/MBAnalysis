import streamlit as st
import re

def get_section(file_content, section_number):
    # Add a placeholder for the end of the document
    file_content += "\n\nSection End:"
    # Use regex to find the section
    match = re.search(f"Section {section_number}:(.*?)(?=Section \d+:)", file_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "Section not found."

# Streamlit UI
st.title('Document Viewer')

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode()

    # Allow user to input section number
    section_number = st.number_input('Enter the section number:', min_value=1, step=1)

    if st.button('View Section'):
        st.write(f"Attempting to view Section {section_number}")
        section_content = get_section(file_content, section_number)
        st.write(f"Extracted content of Section {section_number}:")
        st.write(section_content)
