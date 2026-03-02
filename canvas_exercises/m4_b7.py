from nltk import word_tokenize, pos_tag

corpus = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a high-level programming language"
]

for i, sent in enumerate(corpus):
    tags = pos_tag(word_tokenize(sent))
    print(f"Sentence[{i}] Tags: {[tag for tag in tags]}")