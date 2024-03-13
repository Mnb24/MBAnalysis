import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests

def fetch_section_content(translation_url, section_number):
    response = requests.get(translation_url)
    content = response.text
    sections = content.split("\n\n")  # Assuming sections are separated by double line breaks
    section_content = ""
    for section in sections:
        if f"Section {section_number}" in section:
            section_content = section
            break
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

    # Translation options
    translations = {
        "Bibek Debroy": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/BD1.txt',
        "KM Ganguly": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/KMG1.txt',
        "MN Dutt": 'https://raw.githubusercontent.com/Mnb24/MBAnalysis/main/MND1.txt'
    }

    # User input for section number
    section_number = st.number_input("Enter the section number (1 to 236):", min_value=1, max_value=236, step=1)

    # Dropdown for selecting the translation
    translation = st.selectbox("Select Translation:", list(translations.keys()))

    # Fetch content of the selected section from the chosen translation
    section_content = fetch_section_content(translations[translation], section_number)

    # Generate and display word cloud
    if st.button('Generate Word Cloud'):
        generate_word_cloud(section_content)

if __name__ == "__main__":
    main()
