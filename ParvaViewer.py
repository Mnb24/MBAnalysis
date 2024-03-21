import streamlit as st
import requests
from docx import Document

def get_parva(doc_content, parva_number):
    found_parva = False
    parva_content = []
    for paragraph in doc_content.paragraphs:
        if paragraph.text.startswith("Parva"):
            current_parva_number = paragraph.text.split(" ")[1]
            if current_parva_number == str(parva_number):
                found_parva = True
                parva_content.append(paragraph.text)
            elif found_parva:
                break
        elif found_parva:
            if paragraph.text.startswith("BR-") or paragraph.text.startswith("KK-"):
                parva_content.append('\n' + paragraph.text)
            else:
                parva_content.append(paragraph.text)
    return '\n'.join(parva_content)

# Streamlit UI
st.title('Mahabharata Parva Viewer')

# File paths
file_paths = {
    "BORI (BR)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    "Kumbakonam (KK)": 'https://github.com/Mnb24/MBAnalysis/raw/main/KK-word.docx'  # Direct link to the Word file
}

# Parva names
parva_names = ["Adi Parva", "Sabha Parva", "Vana Parva", "Virata Parva", "Udyoga Parva", "Bhishma Parva", "Drona Parva",
               "Karna Parva", "Shalya Parva", "Sauptika Parva", "Stri Parva", "Shanti Parva", "Anushasana Parva", 
               "Ashvamedhika Parva", "Ashramavasika Parva", "Mausala Parva", "Mahaprasthanika Parva", "Svargarohanika Parva"]

# Allow user to select translation
selected_translation = st.selectbox('Select Translation:', list(file_paths.keys()))

# Allow user to select parva
selected_parva = st.selectbox('Select the Parva:', parva_names)

if st.button('View Parva'):
    file_path = file_paths[selected_translation]
    response = requests.get(file_path)
    doc_content = Document(io.BytesIO(response.content))
    parva_number = parva_names.index(selected_parva) + 1  # Parva numbers start from 1
    parva_content = get_parva(doc_content, parva_number)
    st.markdown(f"## {selected_translation} - {selected_parva}:")
    st.write(parva_content)
