import numpy as np
import re
import nltk
from nltk.tokenize import word_tokenize
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding

nltk.download('punkt_tab')

# ---------------------------
# Text Cleaning
# ---------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+', '<URL>', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ---------------------------
# Load + Tokenize Corpus
# ---------------------------
with open(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\chatbot_corpus.txt", "r", encoding="utf-8") as f:
    corpus = f.read()

corpus = clean_text(corpus)
corpus_tokens = word_tokenize(corpus)
corpus_tokens = corpus_tokens[3000:]
# ---------------------------
# Build Vocabulary
# ---------------------------
vocab = sorted(set(corpus_tokens))
word_to_idx = {word: idx for idx, word in enumerate(vocab)}
idx_to_word = {idx: word for word, idx in word_to_idx.items()}

vocab_size = len(vocab)
print("Vocabulary size:", vocab_size)

# ---------------------------
# Encode Entire Corpus (only ~9MB)
# ---------------------------
encoded = np.array([word_to_idx[w] for w in corpus_tokens], dtype=np.int32)

# ---------------------------
# Create Efficient tf.data Dataset
# ---------------------------
sequence_length = 200
batch_size = 64

dataset = tf.data.Dataset.from_tensor_slices(encoded)

dataset = dataset.window(sequence_length + 1, shift=1, drop_remainder=True)
dataset = dataset.flat_map(lambda w: w.batch(sequence_length + 1))

# X = first 200 tokens
# y = next token
dataset = dataset.map(lambda w: (w[:-1], w[-1]))

for x, y in dataset.take(3):
    print("Input shape:", x.shape)
    print("Target shape:", y.shape)

    print("\nInput:")
    print([idx_to_word[i] for i in x.numpy()])

    print("\nTarget word:")
    print(idx_to_word[y.numpy()])

dataset = dataset.shuffle(10000)
dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)

print("First 3 rows of the dataset:")
for i, element in enumerate(dataset.take(3)):
    print(f"Row {i + 1}: {element[2]}")