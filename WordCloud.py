import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# File paths
file_paths = {
    'Bibek Debroy': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt', 
    'KM Ganguly': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt', 
    'MN Dutt': 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
}

# Function to fetch text content
def fetch_text_content(file_url):
    response = requests.get(file_url)
    return response.text

# Function to generate word cloud
def generate_word_cloud(all_text):
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(all_text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

# Streamlit app
def main():
    st.title("Section-wise Word Cloud Generator")

    # Select text from dropdown
    selected_text = st.selectbox("Select Text", list(file_paths.keys()))

    # Fetch text content
    text_content = fetch_text_content(file_paths[selected_text])

    # Display section number input field
    section_number = st.number_input("Enter Section Number", min_value=1, max_value=236, value=1, step=1)

    # Display word cloud for the selected section
    if st.button("Generate Word Cloud"):
        # Split text into sections based on the section headings
        sections = text_content.split('Section')

        # Check if section number is valid
        if section_number > len(sections):
            st.error("Invalid Section Number! Please enter a valid section number.")
        else:
            section_text = sections[section_number].strip()  # Extract the text of the selected section
            
            # Generate word cloud
            generate_word_cloud(section_text)

if __name__ == "__main__":
    main()

