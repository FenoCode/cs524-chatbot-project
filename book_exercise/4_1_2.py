from nltk import ngrams
from collections import Counter
import nltk

# Sample text
text = "Natural Language Processing is a fascinating field of study."

# tokenize text into words
tokens = nltk.word_tokenize(text)

# func to generate n-grams
def generate_ngrams(tokens, n):
    n_grams = ngrams(tokens,n)
    return [' '.join(grams) for grams in n_grams]

# Generate unigrams, bigrams, and trigrams
unigrams = generate_ngrams(tokens,1)
bigrams = generate_ngrams(tokens,2)
trigrams = generate_ngrams(tokens,3)
print("\nunigrams:")
print(unigrams)
print("\nbigrams:")
print(bigrams)
print("\ntrigrams:")
print(trigrams)