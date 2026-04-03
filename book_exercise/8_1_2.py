import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

nltk.download('punkt')
nltk.download('stopwords')

# sample text
text = """Natural language processing (NLP) is a subfield of artificial intelligence (AI) that focuses on the interaction between computers and humans through natural language. 
The ultimate goal of NLP is to enable computers to understand, interpret, and generate human language in a valuable way. 
NLP combines computational linguistics with machine learning, deep learning, statistical modeling, and more.
It has a wide range of applications, including language translation, sentiment analysis, chatbots, and information retrieval."""

# Preprocess the text
sentences = sent_tokenize(text)
stop_words = set(stopwords.words('english'))

def preprocess_sentence(sentence):
    words = word_tokenize(sentence.lower())
    words = [word for word in words if word.isalnum and word not in stop_words]
    return words

# Sentence scoring based on term frequency
def score_sentences(sentences):
    sentence_scores = []
    word_frequencies = FreqDist([word for sentence in sentences for word in preprocess_sentence(sentence)])
    for sentence in sentences:
        words = preprocess_sentence(sentence)
        sentence_score = sum(word_frequencies[word] for word in words)
        sentence_scores.append((sentence, sentence_score))
    return sentence_scores

# Select top-ranked sentences
def select_sentences(sentence_scores, num_sentences=2):
    sentence_scores.sort(key=lambda x: x[1], reverse=True)
    selected_sentences = [sentence[0] for sentence in sentence_scores[:num_sentences]]
    return selected_sentences

# Generate summary
sentence_scores = score_sentences(sentences)
summary_sentences = select_sentences(sentence_scores)
summary = ' '.join(summary_sentences)

print("Summary:")
print(summary)