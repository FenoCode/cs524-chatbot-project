from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Retrieve corpus from '/dataset'
doc_files = list(Path("F:\CS524\cs524-chatbot-project\dataset").rglob('*.txt'))
doc_content_list = [file.read_text(encoding='utf-8') for file in doc_files]

# User search query
query = "Why should I use OIDC in my application"

# Build TF-IDF matrix
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)
doc_vectors = vectorizer.fit_transform(doc_content_list)
query_vector = vectorizer.transform([query])

# Compute similarity
similarities = cosine_similarity(query_vector, doc_vectors)[0]

# Retrieve best match
best_index = similarities.argmax()
best_score = similarities[best_index]

print("==== Best match ====")
print("Location: ", doc_files[best_index])
print("==== Document Snippet ====")
print(doc_content_list[best_index][0:400])
print("Similarity score:", best_score)