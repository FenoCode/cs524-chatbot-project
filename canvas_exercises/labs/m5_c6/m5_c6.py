from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from nltk import sent_tokenize
import pandas as pd
# Load dataset from kaggle: https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews/data
dataset = pd.read_csv('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m5_c6\IMDB Dataset.csv')

# Encode reviews, encode labels, and split data
print("Dataset loaded successfully. Performing encoding and splitting...")
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(dataset['review'])
le = LabelEncoder()
y = le.fit_transform(dataset['sentiment'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)

# Create linearSVC and train cit
print("Training LinearSVC model...")
clf = LinearSVC(C=1.0, random_state=0)
clf.fit(X_train, y_train)

# Eval model on Dataset
print("Evaluating model on IMDB dataset...")
predictions = clf.predict(X_test)
accuracy = clf.score(X_test, y_test)
print(f"Accuracy (imdb dataset): {accuracy * 100}%\n")

# Perform inference on m5_c6.txt sentences
text = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m5_c6\m5_c6.txt', 'r').read()
text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
text_sent = sent_tokenize(text)

data = {
    'sentence' : text_sent,
    'sentiment': [ "negative", "negative", "negative", "positive", "positive", "negative", "negative", "positive", "negative", "positive", "positive", "positive", "positive", "negative", "negative", "positive" ]
}
df = pd.DataFrame(data)
X = vectorizer.transform(df['sentence'])
y_truth = le.transform(df['sentiment'])

# Eval model on Dataset
predictions = clf.predict(X)
accuracy = clf.score(X, y_truth)
# Print out sentences with their predicted and true labels in table format
for sentence, pred, true in zip(df['sentence'], predictions, y_truth):
    print(f"Sentence: {sentence}")
    print(f"Predicted Sentiment: {le.inverse_transform([pred])[0]}")
    print(f"True Sentiment: {le.inverse_transform([true])[0]}\n")
print(f"Accuracy (dr.seuss text): {accuracy * 100}%")
