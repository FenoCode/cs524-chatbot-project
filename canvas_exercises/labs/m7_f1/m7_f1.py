import nltk
import numpy as np
import networkx as nx

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity

from pypdf import PdfReader

# nltk dependencies
nltk.download('punkt_tab')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load text from PDF
def load_text_from_pdf(path):
    reader = PdfReader(path)
    content = " ".join(p.extract_text() for p in reader.pages if p.extract_text())
    return " ".join(content.split('\n'))

# Sentence preprocesing
def preprocess_sentence(sentence):
    words = word_tokenize(sentence.lower())
    words = [w for w in words if w.isalnum() and w not in stop_words]
    return ' '.join(words)

# Build hybrid similarity matrix
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

    # Create TF-IDF matrix and NMF topic model
    tf = TfidfVectorizer()
    X = tf.fit_transform(processed)
    nmf = NMF(n_components=num_topics, random_state=42)
    W = nmf.fit_transform(X)   # Sentence-topic matrix

    # Lexical similarity (word overlap importance)
    sim_tfidf = cosine_similarity(X)
    # Semantic similarity (topic alignment)
    sim_topic = cosine_similarity(W)

    # Build final similarity matrix with tunable alpha
    similarity_matrix = alpha * sim_topic + (1 - alpha) * sim_tfidf

    return similarity_matrix

# TextRank algorithm for summarization
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
    #selected = sorted(ranked[:num_sentences], key=lambda x: x[2])

    return [s for (_, s, _) in ranked[:num_sentences]]

text = load_text_from_pdf(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\books\pdf\IAM Management - concept, challenges,solutions.pdf")
ground_truth_summary = """Identity and Access Management is important in today's evolving world. It is the process of managing
who has access to what information over time. Activity of IAM involves creation of identities for user and
system. Secure user access plays a key role in the exchange of data and information. In addition, electronic data
is becoming ever more valuable for most companies. Access protection must therefore meet increasingly strict
requirements an issue that is often solved by introducing strong authentication. Identity and the Access are two
very important concept of the IAM which are needed to be managed by the company. Companies are now
relying more on the automated tool which can manage all these things. But then it creates the risk. Because tools
are not intelligent enough to take the decisions, so we can add the intelligence by using the various data mining
algorithm. This can keep the data over time and then build the models. This paper covers all the challenges
associated with the Identity and Access Management. The possible solution is given for these challenges"""

# Tokenize text into sentences and filter
sentences = sent_tokenize(text)
sentences = [s for s in sentences if len(s.split()) > 8]

# Perform extractive summarization using TextRank with hybrid similarity
extractive_summary = textrank(
    sentences,
    num_sentences=10,
    num_topics=3,
    alpha=0.7
)

extractive_summary = " ".join(extractive_summary)
print("\n=== EXTRACTIVE SUMMARY ===\n")
print(extractive_summary)

# Abstractive summarization using BART
from transformers import BartForConditionalGeneration, BartTokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
abstractive_summary = []
# Tokenize and encode text and generate summary
inputs = tokenizer.encode("summarize: " + text, return_tensors="pt")

for input_slice in inputs.split(1024, dim=1):
    summary_ids = model.generate(input_slice, min_length=40, max_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary_snippet = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    abstractive_summary.append(summary_snippet)

abstractive_summary = ' '.join(abstractive_summary)

print("\n=== ABSTRACTIVE SUMMARY ===\n")
print(abstractive_summary)

# Perfromance evaluation using ROUGE
from rouge import Rouge
ROUGE = Rouge()
# Evaluate abstractive vs extractive summaries
print("\n=== ROUGE SCORES (Abstractive vs Extractive) ===\n")
print(ROUGE.get_scores(abstractive_summary, extractive_summary))
# Evaluate extractive vs ground truth summary
print("\n=== ROUGE SCORES (Extractive vs Ground Truth) ===\n")
print(ROUGE.get_scores(extractive_summary, ground_truth_summary))
# Evaluate abstractive vs ground truth summary
print("\n=== ROUGE SCORES (Abstractive vs Ground Truth) ===\n")
print(ROUGE.get_scores(abstractive_summary, ground_truth_summary))
