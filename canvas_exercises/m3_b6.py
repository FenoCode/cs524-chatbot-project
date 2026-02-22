
import math
import string

from collections import Counter
from nltk import bigrams
from nltk import word_tokenize
from nltk import sent_tokenize

def calculate_bigram_perplexity(sentence, bigram_model, unigram_counts, unique_words):
    bigram_sentence = list(bigrams(sentence.split()))
    log_prob = 0

    for bigram in bigram_sentence:
        # Apply Add-One smoothing
        bigram_prob = (bigram_model[bigram] + 1) / (unigram_counts[bigram[0]] + unique_words)
        log_prob += math.log(bigram_prob, 2)

    return math.pow(2, -log_prob / len(bigram_sentence))

# Assuming we have a trained bigram model, unigram counts, and the count of unique words
sentence = "identity is important"

# Assuming corpus is a list of sentences
corpus = open("F:\CS524\cs524-chatbot-project\canvas_exercises\m3_b6.txt", "r").read()
translator = str.maketrans('','', string.punctuation)
corpus = corpus.translate(translator)  # Remove punctuation
corpus = list(filter(None, corpus.splitlines()))  # split into sentences and remove empty lines

# Combine sentences with one word into one sentence to ensure we have bigrams
combined_corpus = []
current_sentence = ""

for sent in corpus:
    if current_sentence:
        current_sentence += " " + sent
    else:
        current_sentence = sent
    
    # If we have at least 2 words, add to corpus
    if len(current_sentence.split()) > 1:
        combined_corpus.append(current_sentence)
        current_sentence = ""

# If there's any remaining single word, append it to the last sentence
if current_sentence and combined_corpus:
    combined_corpus[-1] += " " + current_sentence
elif current_sentence:
    combined_corpus.append(current_sentence)

corpus = combined_corpus
print(corpus)


corpus.append(sentence) # Add test sentence to compute perplexity

bigram_counts = Counter()
unigram_counts = Counter()

for sentence in corpus:
    tokens = word_tokenize(sentence)
    bigram_counts.update(list(bigrams(tokens)))
    unigram_counts.update(tokens)

# Now we can estimate the probability

for sentence in corpus:
    perplexity = calculate_bigram_perplexity(sentence, bigram_counts, unigram_counts, len(set(corpus)))
    print(f"Perplexity of the sentence {sentence,perplexity}")