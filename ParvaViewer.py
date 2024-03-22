import streamlit as st
import requests

def get_content(file_content, section_identifier, selected_section):
    sections = file_content.split('\n')
    found_section = False
    section_content = []
    for line in sections:
        if line.strip().startswith(section_identifier):
            current_section_number = line.strip().split(" ")[1]
            if current_section_number == str(selected_section):
                found_section = True
                section_content.append(line)
            elif found_section:
                break
        elif found_section:
            section_content.append(line)
    return '\n'.join(section_content)

# Streamlit UI
st.title('Mahabharata Text Viewer')

# File paths
file_paths = {
    "BORI (BR)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    "Kumbakonam (KK)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt',
    "Mahabharata Tatparya Nirnaya (MBTN)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MBTN.txt'
}

# Allow user to select translation
selected_translation = st.selectbox('Select Translation:', list(file_paths.keys()))

# If MBTN is selected, show dropdown for Adhyayas
if selected_translation == "Mahabharata Tatparya Nirnaya (MBTN)":
    selected_section = st.selectbox('Select Adhyaya:', list(range(1, 33)))  # Adhyayas from 1 to 32
    section_identifier = "Adhyaya"
else:
    selected_section = st.number_input('Enter the Parva/Section number:', min_value=1, step=1)
    section_identifier = "Section"

if st.button('View Content'):
    file_path = file_paths[selected_translation]
    response = requests.get(file_path)
    file_content = response.text
    content = get_content(file_content, section_identifier, selected_section)
    st.markdown(f"## {selected_translation} - {section_identifier} {selected_section}:")
    st.write(content)

# List of Parvas (for BR and KK translations)
if selected_translation in ["BORI (BR)", "Kumbakonam (KK)"]:
    st.sidebar.title("List of Parvas")
    parvas = ["Adi Parva", "Sabha Parva", "Vana Parva", "Virata Parva", "Udyoga Parva", "Bhishma Parva", 
              "Drona Parva", "Karna Parva", "Shalya Parva", "Sauptika Parva", "Stri Parva", "Shanti Parva", 
              "Anushasana Parva", "Ashvamedhika Parva", "Ashramavasika Parva", "Mausala Parva", 
              "Mahaprasthanika Parva", "Svargarohanika Parva"]
    selected_parva = st.sidebar.selectbox('Select the Parva:', parvas)
    st.sidebar.write(f"You selected {selected_parva}.")
