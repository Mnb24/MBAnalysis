import streamlit as st

def get_section(file_content, section_number):
    sections = file_content.split('\n\n')
    for section in sections:
        if section.strip().startswith(f"Section {section_number}"):
            return section[len(f"Section {section_number}"):].strip()
    return "Section not found."

# Streamlit UI
st.title('Document Viewer')

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    # Allow user to input section number
    section_number = st.number_input('Enter the section number:', min_value=1, step=1)

    if st.button('View Section'):
        section_content = get_section(text, section_number)
        if section_content != "Section not found.":
            st.write(f"**Section {section_number} Content:**")
            st.write(section_content)
        else:
            st.write("Section not found.")
