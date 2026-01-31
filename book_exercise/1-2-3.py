import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# sample reviews
review = [
    "I absolutely love this product! It has changed my life for the better.",
    "This is the worst purchase I've ever made. Completely disappointed.",
    "It's okay, not great but not terrible either.",
] 

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer() 
scored_reviews =  []
for rev in review:
    sentiment = sia.polarity_scores(rev)
    print(f"Review: {rev}")
    print(f"Sentiment Scores: {sentiment}\n")
    scored_reviews.append((rev, sentiment))

# Sort reviews by compound sentiment score
scored_reviews.sort(key=lambda x: x[1]['compound'], reverse=True)
print("Reviews sorted by sentiment score:")
for rev, score in scored_reviews:
    print(f"Review: {rev} | Compound Score: {score['compound']}")