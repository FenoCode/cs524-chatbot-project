from collections import defaultdict
import nltk
from nltk.util import ngrams


def train_bigram_model(tokenized_corpus):
    model = defaultdict(lambda: defaultdict(lambda:0))

    # Count bigrams
    for sentence in tokenized_corpus:
        for w1, w2 in ngrams(sentence, 2):
            model[w1][w2] += 1
    
    # Calculate probabilities
    for w1 in model:
        total_count = float(sum(model[w1].values()))
        for w2 in model[w1]:
            model[w1][w2] /= total_count
    
    return model

def get_bigram_probability(bigram_model, w1, w2):
    return bigram_model[w1][w2]


corpus = [
    "Natural Language Processing is a fascinating field of study.",
    "Machine learning and NLP are closely related.",
    "Language models are essential for NLP tasks."
]

tokenized_corpus = [nltk.tokenize.word_tokenize(sentence) for sentence in corpus]

bigram_model = train_bigram_model(tokenized_corpus)
print("Bigram probability (NLP | for):")
print(get_bigram_probability(bigram_model, "for", "NLP"))


    