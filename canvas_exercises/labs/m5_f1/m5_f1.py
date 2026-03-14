import re
import pandas as pd
import json
from keras.layers import TextVectorization
from keras.models import load_model
from nltk import sent_tokenize
from textblob import TextBlob
DOC_ROOT_PATH = 'F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m5_f1'
MODEL_ROOT_PATH = 'F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m5_d6'
CSV_ROOT_PATH = 'F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\customer_support_tickets'
def clean_text(text):
    #text = text.lower()
    text = re.sub(r'https?://\S+', '<URL>', text)
    text = re.sub(r'\n', ' ', text)
    #text = re.sub(r'[^a-zA-Z0-9<> \n\r]+', ' ', text)
    #text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Load config and recreate the layer
with open(f"{MODEL_ROOT_PATH}/text_vectorization_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open(f"{MODEL_ROOT_PATH}/vocabulary.json", 'r') as f:
    vocab = json.load(f )

t_loaded = TextVectorization.from_config(config)
t_loaded.set_vocabulary(vocab)

#
df = pd.read_csv(f"{CSV_ROOT_PATH}/aa_dataset-tickets-multi-lang-5-2-50-version.csv")
df_subset = df[df['language'] == 'en'].iloc[:10]
text = "\n".join(df_subset['body'].tolist() + df_subset['answer'].tolist())
text_sent = sent_tokenize(clean_text(text))
print(len(text_sent))

# PRED TYPE 1: Keras model of IMDB dataset to evaluate on chatbot corpus
model = load_model(f"{MODEL_ROOT_PATH}/sentiment_model.keras")
# Transform the new texts using the loaded TextVectorization layer
new_data = t_loaded(text_sent)
# Make predictions with the loaded model
keras_predictions = model.predict(new_data)
# Print the predictions
for text, pred in zip(text_sent, keras_predictions):
    sentiment = "positive" if pred[0] > 0.5 else "negative"
    print(f"Text: {text}\nPredicted Sentiment: {sentiment}\n")


# PRED TYPE 2: TextBlob sentiment analysis on chatbot corpus sentences
blob_predictions = [TextBlob(text).sentiment.polarity for text in text_sent]
for text, blob_pred in zip(text_sent, blob_predictions):
    blob_sentiment = "positive" if blob_pred > 0 else "negative" if blob_pred < 0 else "neutral"
    print(f"Text: {text}\nTextBlob Predicted Sentiment: {blob_sentiment}\n")



# PRED TYPE 3: LinearSVC Model of IMDB model to evaluate on chatbot corpus
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from nltk import sent_tokenize
import pandas as pd
# Load dataset from kaggle: https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews/data
dataset = pd.read_csv('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m5_d6\IMDB Dataset.csv')

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

# Eval model on Dataset
X = vectorizer.transform(text_sent)
svc_predictions = clf.predict(X)
# Print out sentences with their predicted and true labels in table format
for sentence, pred in zip(text_sent, svc_predictions):
    print(f"Sentence: {sentence}")
    print(f"Predicted Sentiment: {le.inverse_transform([pred])[0]}")


# Compare first 5 predictions of each model for the first 5 sentences
print("\nComparing first 10 predictions of each model for the first 10 sentences:\n")
for i in range(10):
    print(f"Sentence: {text_sent[i]}")
    print(f"Keras Model Predicted Sentiment: {'positive' if keras_predictions[i][0] > 0.5 else 'negative'}")
    print(f"TextBlob Predicted Sentiment: {'positive' if blob_predictions[i] > 0 else 'negative' if blob_predictions[i] < 0 else 'neutral'}")
    print(f"LinearSVC Predicted Sentiment: {le.inverse_transform([svc_predictions[i]])[0]}\n")