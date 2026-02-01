import sklearn.feature_extraction.text as fe

documents = [
    "I love programming in Python",
    "Python is a great programming language",
]

# Create a CountVectorizer instance
vectorizer = fe.CountVectorizer()
# Fit and transform the documents
X = vectorizer.fit_transform(documents)

vocab = vectorizer.get_feature_names_out()
print(vocab)
print(X.toarray())