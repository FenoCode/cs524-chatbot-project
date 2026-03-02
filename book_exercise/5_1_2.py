import nltk
from nltk import word_tokenize, pos_tag
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')

# Sample text
text = "Natural Language Processing with Python is fascinating"

text = open("F:\CS524\cs524-chatbot-project\dataset\chatbot_corpus-clean.txt", "r").read()

# Tokenize text, perform POS tagging, and output
tokens = word_tokenize(text)
pos_tags = pos_tag(tokens)
print("POS Tags:")
print(pos_tags)