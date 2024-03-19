import streamlit as st
import requests

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
            if line.strip().startswith("BR"):
                parva_content.append('\n' + line)  # Add newline before each line starting with "BR"
            else:
                parva_content.append(line)
    return ''.join(parva_content)


# Streamlit UI
st.title('Mahabharata Parva Viewer')

# File path
file_path = 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BR-Complete.txt'

# Parva names
parva_names = ["Adi Parva", "Sabha Parva", "Vana Parva", "Virata Parva", "Udyoga Parva", "Bhishma Parva", "Drona Parva",
               "Karna Parva", "Shalya Parva", "Sauptika Parva", "Stri Parva", "Shanti Parva", "Anushasana Parva", 
               "Ashvamedhika Parva", "Ashramavasika Parva", "Mausala Parva", "Mahaprasthanika Parva", "Svargarohanika Parva"]

# Allow user to select parva
selected_parva = st.selectbox('Select the Parva:', parva_names)

if st.button('View Parva'):
    response = requests.get(file_path)
    file_content = response.text
    parva_number = parva_names.index(selected_parva) + 1  # Parva numbers start from 1
    parva_content = get_parva(file_content, parva_number)
    st.markdown(f"## {selected_parva}:")
    st.write(parva_content)
