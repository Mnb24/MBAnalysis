import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import requests
import re

def fetch_section_content(file_path, section_number):
    response = requests.get(file_path)
    content = response.text
    sections = re.split('Section \d+', content)  # Split content based on 'Section (number)'
    section_content = sections[section_number] if section_number < len(sections) else ""
    return section_content
    
def generate_word_cloud(section_content):
    if not section_content:
        st.write("No content available for the selected section.")
        return
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(section_content)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.pyplot()

def main():
    # Displaying heading
    st.title("Word Cloud Generator")

    # File paths to the text files
    file_paths = {
        'Bibek Debroy': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
        'KM Ganguly': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
        'MN Dutt': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
    }

    # Dropdown for selecting the file
    file_path = st.selectbox("Select File:", list(file_paths.keys()))

    # User input for section number
    section_number = st.number_input("Enter the section number (1 to 236):", min_value=1, max_value=236, step=1)

    # Fetch content of the selected section from the chosen file
    section_content = fetch_section_content(file_paths[file_path], section_number)

    # Generate and display word cloud
    if st.button('Generate Word Cloud'):
        generate_word_cloud(section_content)

if __name__ == "__main__":
    main()


