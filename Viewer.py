import streamlit as st

def get_section(file_content, section_number):
    sections = file_content.split('\n')
    found_sections = []
    for line in sections:
        if line.strip().startswith("Section"):
            current_section_number = line.strip().split(" ")[1]
            if current_section_number == str(section_number):
                found_sections.append(line)
            elif found_sections:
                break
        elif found_sections:
            found_sections.append(line)
    return '\n'.join(found_sections)

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
