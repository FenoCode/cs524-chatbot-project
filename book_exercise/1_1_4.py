import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize

text = "Hello, world! This is a test."
tokens = word_tokenize(text)
print(tokens)