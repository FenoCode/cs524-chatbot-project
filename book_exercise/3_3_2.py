from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize

text = "Natural language processing is fun and exciting. Language models are important in NLP. I enjoy learning about artificial intelligence. Machine learning and NLP are closely related. Deep learning is a subset of machine learning."

# Tokenize the text into sentences and then into words
sentences = sent_tokenize(text)
tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
# Train a Word2Vec model
model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, sg=1)


# vector model of word 'language'
vector = model.wv['language']
print("Vector representation of the word 'language':")
print(vector)

# most similar words to 'language'
similar_words = model.wv.most_similar('language')
print("\nWords most similar to 'language':")
print(similar_words)