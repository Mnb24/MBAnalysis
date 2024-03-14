import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import StringIO

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
def generate_word_cloud(text):
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_font_size=100).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    except Exception as e:
        print("Error generating word cloud:", e)
        print("Text causing the error:", text)


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
        # Split text into sections
        sections = text_content.split('\n\n')  # Assuming sections are separated by double line breaks

        # Check if section number is valid
        if section_number > len(sections):
            st.error("Invalid Section Number! Please enter a valid section number.")
        else:
            section_text = sections[section_number - 1]
            generate_word_cloud(section_text)

if __name__ == "__main__":
    main()
