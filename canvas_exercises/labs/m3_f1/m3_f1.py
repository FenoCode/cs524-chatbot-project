import numpy as np
import re
import nltk
from nltk.tokenize import word_tokenize
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding

nltk.download('punkt_tab')

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+', '<URL>', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Load and tokenize corpus
with open(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\chatbot_corpus.txt", "r", encoding="utf-8") as f:
    corpus = f.read()

corpus = clean_text(corpus)
corpus_tokens = word_tokenize(corpus)
corpus_tokens = corpus_tokens[300000:]

# Build vocabulary
vocab = sorted(set(corpus_tokens))
word_to_idx = {word: idx for idx, word in enumerate(vocab)}
idx_to_word = {idx: word for word, idx in word_to_idx.items()}

vocab_size = len(vocab)
print("Vocabulary size:", vocab_size)


# Encode tokens and form batched dataset
encoded = np.array([word_to_idx[w] for w in corpus_tokens], dtype=np.int32)
sequence_length = 200
batch_size = 64
dataset = tf.data.Dataset.from_tensor_slices(encoded)
dataset = dataset.window(sequence_length + 1, shift=1, drop_remainder=True)
dataset = dataset.flat_map(lambda w: w.batch(sequence_length + 1))

# X = first 'sequence_length' tokens (i.e. first 200 tokens)
# y = next token
dataset = dataset.map(lambda w: (w[:-1], w[-1]))

dataset = dataset.shuffle(10000)
dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)

# LSTM model definition
model = Sequential([
    Embedding(vocab_size, 256),
    LSTM(256, return_sequences=True),
    LSTM(128),
    Dense(vocab_size, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

model.fit(dataset, epochs=10)
model.summary()

# Text gen function
def generate_text(model, start_string, num_generate=25, temperature=1.0):
    start_string = clean_text(start_string)
    input_words = word_tokenize(start_string)

    # Keep last 200 tokens
    input_words = input_words[-sequence_length:]
    input_ids = [word_to_idx.get(w, 0) for w in input_words]

    input_eval = np.array(input_ids)[None, :]  # shape (1, seq_len)

    generated = input_words.copy()

    for _ in range(num_generate):
        predictions = model.predict(input_eval, verbose=0)[0]

        # Temperature sampling
        predictions = np.log(predictions + 1e-8) / temperature
        probabilities = tf.nn.softmax(predictions).numpy()
        predicted_id = np.random.choice(len(probabilities), p=probabilities)

        generated.append(idx_to_word[predicted_id])

        # Slide window
        input_eval = np.concatenate(
            [input_eval[:, 1:], [[predicted_id]]],
            axis=1
        )

    return " ".join(generated)


# Generate new text
start_string = "How can I integrate SSO into my applicaiton?"
start_string = start_string[-sequence_length:]  # Use the last 'sequence_length' words as the starting point

generated_text = generate_text(model, start_string, 50);
print("Generated text:")
print(generated_text)