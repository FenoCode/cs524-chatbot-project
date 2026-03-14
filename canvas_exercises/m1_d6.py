import nltk
from nltk.tokenize import word_tokenize

text = open("F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\m1_d6_text.txt").read()
tokens = word_tokenize(text)
print("Token count:", len(tokens))
print("Unique token count:", len(set(tokens)))