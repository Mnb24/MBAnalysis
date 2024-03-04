import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

nltk.download('punkt')
nltk.download('stopwords')

def get_section(file_name, section_number):
    with open(file_name, 'r') as file:
        content = file.read()
        sections = re.split(r'Section \d+', content)
        if section_number <= len(sections) and section_number > 0:
            return sections[section_number + 1] 
        else:
            return "Section not found."


def truncate_text(text, word_limit):
    words = word_tokenize(text)
    truncated_text = ' '.join(words[:word_limit])
    return truncated_text

def build_similarity_matrix(sentences, stop_words):
    # Remove stopwords and punctuations from sentences
    clean_sentences = [sentence.lower() for sentence in sentences if sentence not in stop_words]
    
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 != idx2:  # Exclude comparing the sentence with itself
                similarity_matrix[idx1][idx2] = sentence_similarity(clean_sentences[idx1], clean_sentences[idx2])
    return similarity_matrix

def sentence_similarity(sent1, sent2):
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words1 = [word.lower() for word in word_tokenize(sent1) if word.lower() not in stop_words]
    words2 = [word.lower() for word in word_tokenize(sent2) if word.lower() not in stop_words]
    
    # Create a set of all unique words
    all_words = list(set(words1 + words2))
    
    # Create vectors
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    
    # Populate vectors with word counts
    for word in words1:
        vector1[all_words.index(word)] += 1
        
    for word in words2:
        vector2[all_words.index(word)] += 1
    
    # Calculate cosine similarity
    return cosine_similarity([vector1], [vector2])[0,0]

def pagerank(similarity_matrix, damping=0.85, epsilon=1.0e-8, max_iterations=100):
    n = similarity_matrix.shape[0]  # Number of sentences
    p = np.ones(n) / n  # Initialize page rank
    
    for _ in range(max_iterations):
        new_p = np.ones(n) * (1 - damping) / n + damping * similarity_matrix.T.dot(p)
        if abs(np.sum(new_p - p)) < epsilon:
            return new_p
        p = new_p
    return p

def generate_summary(file_name, section_number, word_limit=200, top_n=5):
    section = get_section(file_name, section_number)
    if section == "Section not found.":
        return section

    # Truncate the section if it exceeds the word limit
    if len(word_tokenize(section)) > word_limit:
        section = truncate_text(section, word_limit)

    # Tokenize sentences
    sentences = sent_tokenize(section)
    stop_words = set(stopwords.words('english'))

    # Generate similarity matrix across sentences
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    # Rank sentences using PageRank algorithm
    scores = pagerank(sentence_similarity_matrix)

    # Flatten the scores array
    scores = scores.flatten()

    # Sort the rank and pick top sentences
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[::-1][:top_n]]
    summary = ' '.join(ranked_sentences)

    return summary

if __name__ == "__main__":
    num_files = int(input("Enter the number of files: "))

    file_names = []
    for i in range(num_files):
        file_names.append(input(f"Enter the name of file {i + 1}: "))

    section_number = int(input("Enter the section number: "))

    print("\nUsing TextRank Summarization:")
    for file_name in file_names:
        print(f"Summary for {file_name}:")
        summary = generate_summary(file_name, section_number)
        print(summary)
        print("-" * 50)

