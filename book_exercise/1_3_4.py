import nltk, spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
nltk.download('stopwords')

# sample reviews
review = [
    "I absolutely love this product! It has changed my life for the better.",
    "This is the worst purchase I've ever made. Completely disappointed.",
    "I am extremely satisfied with my experience. Highly recommend to everyone!",
    "The quality is terrible and I will never buy this again.",
] 
labels = [1, 0, 1, 0]  # 1: positive, 0: negative

nlp = spacy.load("en_core_web_sm")

def spacy_tokenizer(text):
    doc = nlp(text)
    return [token.text for token in doc]

stop_words = list(set(stopwords.words('english')))

pipeline = Pipeline([
    ('vectorizer', CountVectorizer(tokenizer=spacy_tokenizer, stop_words=stop_words)),
    ('classifier', MultinomialNB())
])

pipeline.fit(review, labels)

test_review = ["I will never buy this product again, it was a waste of money."]
prediction = pipeline.predict(test_review)
print(f"Review: {test_review[0]}")
print(f"Predicted Sentiment: {prediction}")