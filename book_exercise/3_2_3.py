from sklearn.feature_extraction.text import TfidfVectorizer

# Sample documents and their corresponding labels
documents = [
    "Natural language processing is fun",
    "Language models are important in NLP",
    "I enjoy learning about artificaial intelligence",
    "Machine learning  and NLP are closely related",
    "Deep learning is a subset of machine learning"
]

# Init transformer and apply to corpus
ts = TfidfVectorizer()
X = ts.fit_transform(documents)

print("Vocab:")
print(ts.get_feature_names_out())
print("TF-IDF Array:")
print(X.toarray())
