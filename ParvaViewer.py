import streamlit as st
import requests

def get_adhyaya(file_content, adhyaya_number):
    adhyayas = file_content.split('\n')
    found_adhyaya = False
    adhyaya_content = []
    for line in adhyayas:
        if line.strip().startswith("Adhyaya"):
            current_adhyaya_number = line.strip().split(" ")[1]
            if current_adhyaya_number == str(adhyaya_number):
                found_adhyaya = True
                adhyaya_content.append(line)
            elif found_adhyaya:
                break
        elif found_adhyaya:
            adhyaya_content.append(line)
    return '\n'.join(adhyaya_content)

def get_parva(file_content, parva_number):
    parvas = file_content.split('\n')
    found_parva = False
    parva_content = []
    for line in parvas:
        if line.strip().startswith("Parva"):
            current_parva_number = line.strip().split(" ")[1]
            if current_parva_number == str(parva_number):
                found_parva = True
                parva_content.append(line)
            elif found_parva:
                break
        elif found_parva:
            if line.strip().startswith("BR-") or line.strip().startswith("KK-"):  # Check if line starts with "BR-" or "KK-"
                parva_content.append('\n' + line)  # Add newline before lines starting with "BR-" or "KK-"
            else:
                parva_content.append(line)
    return '\n'.join(parva_content)

# Streamlit UI
st.title('Mahabharata Text Viewer')

# File paths
file_paths = {
    "BORI (BR)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    "Kumbakonam (KK)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KK-Complete.txt',
    "Mahabharata Tatparya Nirnaya (MBTN)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MBTN.txt'
}

# Parva names
parva_names = ["Adi Parva", "Sabha Parva", "Vana Parva", "Virata Parva", "Udyoga Parva", "Bhishma Parva", "Drona Parva",
               "Karna Parva", "Shalya Parva", "Sauptika Parva", "Stri Parva", "Shanti Parva", "Anushasana Parva", 
               "Ashvamedhika Parva", "Ashramavasika Parva", "Mausala Parva", "Mahaprasthanika Parva", "Svargarohanika Parva"]

# Allow user to select translation
selected_translation = st.selectbox('Select Translation:', list(file_paths.keys()))

# If MBTN is selected, show dropdown for Adhyayas
if selected_translation == "Mahabharata Tatparya Nirnaya (MBTN)":
    selected_adhyaya = st.selectbox('Select Adhyaya:', list(range(1, 33)))  # Adhyayas from 1 to 32
    section_identifier = "Adhyaya"
else:
    selected_parva = st.selectbox('Select the Parva:', parva_names)
    section_identifier = "Section"

if st.button('View Content'):
    file_path = file_paths[selected_translation]
    response = requests.get(file_path)
    file_content = response.text
    if selected_translation == "Mahabharata Tatparya Nirnaya (MBTN)":
        content = get_adhyaya(file_content, selected_adhyaya)
    else:
        parva_number = parva_names.index(selected_parva) + 1  # Parva numbers start from 1
        content = get_parva(file_content, parva_number)
    st.markdown(f"## {selected_translation} - {section_identifier} {selected_adhyaya if selected_translation == 'Mahabharata Tatparya Nirnaya (MBTN)' else selected_parva}:")
    st.write(content)
