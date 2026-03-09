from afinn import Afinn
# Init the Afinn sentiment analyzer
afinn = Afinn()
text = "I don't understand what you mean. Please direct me to an engineer now."

# Perform sentiment analysis
sentiment_score = afinn.score(text)

# Determine sentiment based on score
if sentiment_score > 0:
    sentiment = "Positive"
elif sentiment_score < 0:
    sentiment = "Negative"
else:
    sentiment = "Neutral"

print("Sentiment analysis")
print(f"Text: {text}")
print(f"Sentiment Score: {sentiment_score}")
print(f"Sentiment: {sentiment}")