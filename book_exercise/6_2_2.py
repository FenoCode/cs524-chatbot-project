from sklearn.feature_extraction.text import TfidfVectorizer

# sample corpus
corpus = [
    "I love this product! It's amazing.",
    "This is the worst service I have ever experienced.",
    "I am very happy with my purchase.",
    "I am disappointed with the quality of this item."
]

# Init TF-IDF and transform text into feature
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

print("TF-IDF Feature Matrix:")
print(X.toarray())