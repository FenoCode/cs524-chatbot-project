from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sample documents and their corresponding labels
documents = [
    "Natural language processing is fun",
    "Language models are important in NLP",
    "I enjoy learning about artificaial intelligence",
    "Machine learning  and NLP are closely related",
    "Deep learning is a subset of machine learning"
]

labels = [1, 1, 0, 1, 0] # 1 for NLP-related, 0 for AI-related

# Init vectorizer and transform text data
ve = CountVectorizer()
X = ve.fit_transform(documents)
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.20, random_state=42)

# Init classifier and train it
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Run test predictions
y_pred = classifier.predict(X_test)

# Calc accuracy and return
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy)