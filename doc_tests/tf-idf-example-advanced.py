import nltk
import re
from pathlib import Path
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')    
nltk.download('omw-1.4') 
nltk.download('averaged_perceptron_tagger_eng') 

stop_words = stopwords.words('english')
le = WordNetLemmatizer()

def clean_corpus(corpus):
    # Implement text cleaning steps such as lowercasing, removing punctuation, etc.
    cleaned_corpus = []
    for doc in corpus:
        cleaned_doc = doc.lower()  # Convert to lowercase
        cleaned_doc = ''.join(char for char in cleaned_doc if char.isalnum() or char.isspace())  # Remove punctuation
        cleaned_doc =  re.sub(r'https?://\S+', '', cleaned_doc) # remove links
        cleaned_corpus.append(cleaned_doc)
    return cleaned_corpus

def chunk_sentences(sentences, window=3, stride=1):
    chunks = []
    for i in range(0, len(sentences) - window + 1, stride):
        chunks.append((
            " ".join(sentences[i:i+window]),
            i
        ))
    return chunks

# Retrieve corpus
corpus = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\chatbot_corpus.txt', 'r', encoding='utf-8').readlines()
corpus = [line.strip() for line in corpus if line.strip()] # Remove empty lines and strip whitespace
corpus = " ".join(corpus) # List[str] -> str

# Parse sentences, normalize text, lemmatize, and remove stop words
corpus_sent = sent_tokenize(corpus)
corpus_sent_parsed = clean_corpus(corpus_sent)
corpus_sent_parsed = [[le.lemmatize(word.lower()) for word in word_tokenize(sent)] for sent in corpus_sent_parsed]
corpus_sent_parsed = [[word for word in sent if word not in stop_words] for sent in corpus_sent_parsed]
corpus_sent_parsed = [ ' '.join(word for word in sent) for sent in corpus_sent_parsed] # List[List[str]] -> List[str]

# User search query
query = "How do I authenticate when I use SSO"
query = clean_corpus([query])[0]
query = [le.lemmatize(word.lower()) for word in word_tokenize(query)]
query = [word for word in query if word not in stop_words]
query = ' '.join(word for word in query) # List[str] -> str

# Build TF-IDF matrix
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)
doc_vectors = vectorizer.fit_transform(corpus_sent_parsed)
query_vector = vectorizer.transform([query])

# Compute similarity
scores = cosine_similarity(query_vector, doc_vectors)[0]

top_hits = sorted(
    zip(scores, corpus_sent),
    key=lambda x: x[0],
    reverse=True
)[:3]

for score, hit in top_hits:
    print(score, hit)
    print()