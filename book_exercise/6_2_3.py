from sklearn. model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report

# sample corpus
corpus = [
    "I love this product! It's amazing.",
    "This is the worst service I have ever experienced.",
    "I am very happy with my purchase.",
    "I am disappointed with the quality of this item.",
    "This item saved my party",
    "My event was ruined by this product"
]
labels = [1, 0, 1, 0, 1, 0] # 1 for positive, 0 for negative

# Init TF-IDF and transform text into feature
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.25, random_state=42)

# Init, train, and predict with the Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Eval the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification report")
print(report)