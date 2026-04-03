import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import networkx as nx
from pypdf import PdfReader
from pathlib import Path


nltk.download('punkt')
nltk.download('stopwords')
tf = TfidfVectorizer()
stop_words = set(stopwords.words('english'))

# sample text
text = """Natural language processing (NLP) is a subfield of artificial intelligence (AI) that focuses on the interaction between computers and humans through natural language. 
The ultimate goal of NLP is to enable computers to understand, interpret, and generate human language in a valuable way. 
NLP combines computational linguistics with machine learning, deep learning, statistical modeling, and more.
It has a wide range of applications, including language translation, sentiment analysis, chatbots, and information retrieval."""

reader = PdfReader(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\books\pdf\IAM Management - concept, challenges,solutions.pdf")
content = " ".join(p.extract_text() for p in reader.pages)
text = "" .join(content.split('\n'))

def preprocess_sentence(sentence):
    words = word_tokenize(sentence.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

# Preprocess the text and initialize TfidfVectorizer
sentences = sent_tokenize(text)
sentences = [sent for sent in sentences if len(sent.split()) > 20]


# Build sentence similarity matrix
def build_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    sentences = [preprocess_sentence(sent) for sent in sentences]
    tf.fit(sentences)

    for i, sentence1 in enumerate(sentences):
        for j, sentence2 in enumerate(sentences):
            if i != j:
                similarity_matrix[i][j] = 1 - cosine_similarity(tf.transform([sentence1]), tf.transform([sentence2]))[0][0]
    return similarity_matrix

# Apply TextRank algo
def textrank(sentences, num_sentences=2):
    similarity_matrix = build_similarity_matrix(sentences)
    similarity_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(similarity_graph)

    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
    selected_sentences = [sentence for score, sentence in ranked_sentences[:num_sentences]]

    return selected_sentences

# Generate Summary
summary_sentences = textrank(sentences, 4)
summary = ' '.join(summary_sentences)

print("Summary:")
print(summary)