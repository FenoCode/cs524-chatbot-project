import textblob

text = "I love programming in Python. It's such a versatile language!"
blob = textblob.TextBlob(text)
print(blob.sentiment)
