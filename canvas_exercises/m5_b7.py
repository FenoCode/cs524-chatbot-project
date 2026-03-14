from textblob import TextBlob
from nltk import sent_tokenize

text = open("F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\m5_b7.txt", "r").read()
text_sent = sent_tokenize(text)

for i, sent in enumerate(text_sent):
    blob = TextBlob(sent)
    print(f"Sentence[{i}]: Text = '{sent}' {blob.sentiment}]")

text = "All that cold wet day."
blob = TextBlob(text)
print(f"Text = '{text}' {blob.sentiment}]")
