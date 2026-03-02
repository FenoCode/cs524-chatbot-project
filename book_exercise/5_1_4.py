from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger
from nltk.corpus import treebank
import nltk
nltk.download('treebank')

# Load treebank corpus
train_data = treebank.tagged_sents()[:3000]
test_data = treebank.tagged_sents()[3000:]

# Train a UnigramTagger
unigram_tagger = UnigramTagger(train_data)

# Eval the tagger
accuracy = unigram_tagger.accuracy(test_data)
print("[untrained] Unigram Tagger Accuracy: ")
print("Unigram Tagger Accuracy: ", accuracy)

# Train BigramTagger backed by UnigramTagger
bigram_tagger = BigramTagger(train_data, backoff=unigram_tagger)

# Eval the tagger
accuracy = bigram_tagger.accuracy(test_data)
print("Bigram Tagger Accuracy: ", accuracy)
 
# Train a TrigramTagger backed by BigramTagger
trigram_tagger = TrigramTagger(train_data, backoff=bigram_tagger)
accuracy = trigram_tagger.accuracy(test_data)
print("Trigram Tagger Accuracy: ", accuracy)