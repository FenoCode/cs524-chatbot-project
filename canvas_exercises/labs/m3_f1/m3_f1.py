import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.utils import to_categorical

# text corpus
text = "hello world"

# Create character level vocab
chars = sorted (set(text))
char_to_idx = {char: idx for idx, char in enumerate(chars)}
idx_to_char = {idx: char for char, idx in char_to_idx.items()}

# Create input-output pairs for training
sequence_length = 3
X = []
y = []
for i in range(len(text) - sequence_length):
    X.append([char_to_idx[char] for char in text[i:i + sequence_length]])
    y.append([char_to_idx[text[i + sequence_length]]])

X = np.array(X)
y = to_categorical(y, num_classes=len(chars))

# Reshape input to be compatible with RNN input
X = X.reshape((X.shape[0], X.shape[1], 1))

# Define the RNN model
model = Sequential()
model.add(LSTM(50, input_shape=(sequence_length, 1)))
model.add(Dense(len(chars), activation='softmax'))

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy')

# Train model
model.fit(X, y, epochs=200 , verbose=1)

# Func to generate text using the trained model
def generate_text(model, start_string, num_generate):
    input_eval = [char_to_idx[s] for s in start_string]
    input_eval = np.array(input_eval).reshape((1, len(input_eval), 1))

    text_generated = []

    for i in range(num_generate):
        predictions = model.predict(input_eval)
        predicted_id = np.argmax(predictions[-1])

        input_eval = np.append(input_eval[:, 1:], [[[predicted_id]]], axis=1)
        text_generated.append(idx_to_char[predicted_id])
    

    return start_string + ''.join(text_generated)

# Generate new text
start_string = "hel"
generated_text = generate_text(model, start_string, 5);
print("Generated text:")
print(generated_text)