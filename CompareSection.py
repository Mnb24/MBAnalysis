import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st

nltk.download('punkt')
nltk.download('stopwords')

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

def compare_sections(section_content1, section_content2):
    # Tokenize the content of each section
    tokens1 = word_tokenize(section_content1)
    tokens2 = word_tokenize(section_content2)

    # Filter out stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens1 = [word.lower() for word in tokens1 if word.lower() not in stop_words]
    filtered_tokens2 = [word.lower() for word in tokens2 if word.lower() not in stop_words]

    # Calculate Jaccard similarity score
    jaccard_similarity = len(set(filtered_tokens1).intersection(filtered_tokens2)) / len(set(filtered_tokens1).union(filtered_tokens2))

    # Find common words between the two sections
    common_words = list(set(filtered_tokens1).intersection(filtered_tokens2))

    return jaccard_similarity, common_words

# Streamlit UI
st.title('Compare Sections - Adi Parva')

# File paths
file_paths = ['https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
              'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt']

# File names
file_names = ["Bibek Debroy's", "KM Ganguly's", "MN Dutt's"]

# Allow user to input section number
section_number = st.number_input('Enter the section number (1 to 236):', min_value=1, step=1)

if st.button('Compare Section'):
    # Fetch section content for each file
    section_contents = []
    for file_path, file_name in zip(file_paths, file_names):
        response = requests.get(file_path)
        file_content = response.text
        section_content = get_section(file_content, section_number)
        section_contents.append((file_name, section_content))

    # Compare sections and display results
    for i in range(len(section_contents)):
        for j in range(i+1, len(section_contents)):
            st.markdown(f"## Comparing Section {section_number} from {section_contents[i][0]} with {section_contents[j][0]}:")
            similarity_score, common_words = compare_sections(section_contents[i][1], section_contents[j][1])
            st.write(f"Jaccard Similarity Score: {similarity_score}")
            st.write("Common significant words between the specified sections:", common_words)
