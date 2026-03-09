from textblob import TextBlob

# Sample text
text = "This article helped me understand."

# Perform sentiment analysis
blob = TextBlob(text)
sentiment = blob.sentiment

print("Sentiment Analysis:")
print(f"Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}")