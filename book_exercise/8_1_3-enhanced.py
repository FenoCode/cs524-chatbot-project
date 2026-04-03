import nltk
import numpy as np
import networkx as nx

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity

from pypdf import PdfReader

# ----------------------------
# Setup
# ----------------------------
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# ----------------------------
# Load Text (PDF or fallback)
# ----------------------------
def load_text_from_pdf(path):
    reader = PdfReader(path)
    content = " ".join(p.extract_text() for p in reader.pages if p.extract_text())
    return " ".join(content.split('\n'))

# Example usage:
# text = load_text_from_pdf("your_file.pdf")

text = """Natural language processing (NLP) is a subfield of artificial intelligence (AI) that focuses on the interaction between computers and humans through natural language. 
The ultimate goal of NLP is to enable computers to understand, interpret, and generate human language in a valuable way. 
NLP combines computational linguistics with machine learning, deep learning, statistical modeling, and more.
It has a wide range of applications, including language translation, sentiment analysis, chatbots, and information retrieval."""

reader = PdfReader(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\books\pdf\IAM Management - concept, challenges,solutions.pdf")
content = " ".join(p.extract_text() for p in reader.pages)
text = "" .join(content.split('\n'))

# ----------------------------
# Preprocessing
# ----------------------------
def preprocess_sentence(sentence):
    words = word_tokenize(sentence.lower())
    words = [w for w in words if w.isalnum() and w not in stop_words]
    return ' '.join(words)

# ----------------------------
# Build Hybrid Similarity Matrix
# ----------------------------
def build_similarity_matrix(sentences, num_topics=5, alpha=0.7):
    """
    alpha controls the tradeoff between:
    
    - TF-IDF similarity (surface-level lexical overlap)
    - NMF topic similarity (latent semantic similarity)
    
    alpha = 1.0 → purely topic-based (semantic)
    alpha = 0.0 → purely TF-IDF (lexical)
    
    Recommended:
    - 0.6-0.8 → more semantic summaries
    - 0.4-0.6 → more extractive / literal summaries
    """

    # Preprocess
    processed = [preprocess_sentence(s) for s in sentences]

    # ----------------------------
    # TF-IDF Representation
    # ----------------------------
    tf = TfidfVectorizer()
    X = tf.fit_transform(processed)

    # ----------------------------
    # NMF Topic Modeling
    # ----------------------------
    nmf = NMF(n_components=num_topics, random_state=42)
    W = nmf.fit_transform(X)   # Sentence-topic matrix

    # ----------------------------
    # Similarity Computation
    # ----------------------------

    # Lexical similarity (word overlap importance)
    sim_tfidf = cosine_similarity(X)

    # Semantic similarity (topic alignment)
    sim_topic = cosine_similarity(W)

    # ----------------------------
    # Hybrid Similarity
    # ----------------------------
    similarity_matrix = alpha * sim_topic + (1 - alpha) * sim_tfidf

    return similarity_matrix

# ----------------------------
# TextRank Algorithm
# ----------------------------
def textrank(sentences, num_sentences=5, num_topics=5, alpha=0.7):
    similarity_matrix = build_similarity_matrix(
        sentences,
        num_topics=num_topics,
        alpha=alpha
    )

    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    ranked = sorted(
        ((scores[i], s, i) for i, s in enumerate(sentences)),
        reverse=True
    )

    # Preserve original order for readability
    selected = sorted(ranked[:num_sentences], key=lambda x: x[2])

    return [s for (_, s, _) in selected]

# ----------------------------
# Run Summarizer
# ----------------------------
sentences = sent_tokenize(text)

# Optional: filter very short sentences (noise reduction)
sentences = [s for s in sentences if len(s.split()) > 8]

summary_sentences = textrank(
    sentences,
    num_sentences=3,
    num_topics=5,
    alpha=0.7  # Key tuning parameter
)

summary = " ".join(summary_sentences)

print("\n=== SUMMARY ===\n")
print(summary)