from pathlib import Path
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def chunk_sentences(sentences, window=3, stride=1):
    chunks = []
    for i in range(0, len(sentences) - window + 1, stride):
        chunks.append((
            " ".join(sentences[i:i+window]),
            i
        ))
    return chunks


# Retrieve corpus from '/dataset'
chunks=[]
doc_files = list(Path("F:\CS524\cs524-chatbot-project\dataset").rglob('*.txt'))
for file in doc_files:
    text = file.read_text(encoding='utf-8')
    sentences = sent_tokenize(text)

    for chunk_text, idx in chunk_sentences(sentences):
        chunks.append({
            "text": chunk_text,
            "path": file.name,
            "sentence_idx": idx
        })

texts = [c["text"] for c in chunks]

# User search query
query = "How can I contact help for this?"

# Build TF-IDF matrix
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)
doc_vectors = vectorizer.fit_transform(texts)
query_vector = vectorizer.transform([query])

# Compute similarity
scores = cosine_similarity(query_vector, doc_vectors)[0]

top_hits = sorted(
    zip(scores, chunks),
    key=lambda x: x[0],
    reverse=True
)[:5]

for score, hit in top_hits:
    print(score, hit["path"], hit["sentence_idx"], "\"", hit["text"], "\"")
    print("\n\n")