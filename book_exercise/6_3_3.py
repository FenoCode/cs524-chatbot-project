import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
from keras.layers import TextVectorization;
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# sample corpus
corpus = [
    "I love this product! It's amazing.",
    "This is the worst service I have ever experienced.",
    "I am very happy with my purchase.",
    "I am disappointed with the quality of this item.",
]
labels = np.array([1, 0, 1, 0], dtype="float32")  # convert labels

vectorizer = TextVectorization(
    max_tokens=5000,
    output_mode="int",
    output_sequence_length=10
)

vectorizer.adapt(corpus)
X = vectorizer(corpus).numpy()

# split data into training and tests sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.25, random_state=42)
# build the model
model = Sequential()
model.add(Embedding(input_dim=5000, output_dim=50, input_shape=(10,)))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))

# compile & train the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=5, verbose=1, validation_data=(X_test, y_test))
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# Predicting with the model
new_text = ["This product is the worst."]
new_text_seq = vectorizer(new_text)
prediction = model.predict(new_text_seq)
print("Prediction:", "Positive" if prediction[0][0] > 0.5 else "Negative")