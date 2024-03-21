import streamlit as st
import requests
import zipfile
import io

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
st.title('Mahabharata Parva Viewer')

# File paths
file_paths = {
    "BORI (BR)": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt',
    "Kumbakonam (KK)": 'https://github.com/Mnb24/MBAnalysis/blob/main/KK-%20Complete.zip?raw=true'  # Direct link to the ZIP file
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
    if file_path.endswith(".zip"):
        response = requests.get(file_path)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            file_list = z.namelist()
            for filename in file_list:
                if filename.endswith(".txt"):
                    with z.open(filename) as f:
                        file_content = f.read().decode('utf-8')
                        break  # Stop after reading the first TXT file
    else:
        response = requests.get(file_path)
        file_content = response.text
    
    parva_number = parva_names.index(selected_parva) + 1  # Parva numbers start from 1
    parva_content = get_parva(file_content, parva_number)
    st.markdown(f"## {selected_translation} - {selected_parva}:")
    st.write(parva_content)
