import nltk
from nltk import word_tokenize, pos_tag
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')

# Sample text
text = "Janet will back the bill. Does Will?"

# Tokenize text, perform POS tagging, and output
tokens = word_tokenize(text)
pos_tags = pos_tag(tokens)
print("POS Tags:")
print(pos_tags)