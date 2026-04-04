import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding
from keras.preprocessing.sequence import pad_sequences
from keras.layers import TextVectorization;

# sample data
input_texts = [
    "Hello.",
    "How are you?",
    "What is your name?",
    "Good morning.",
    "Good night."
]
input_texts = [f"<starttoken> {text} <endtoken>" for text in input_texts]
target_texts = [
    "Bonjour.",
    "Comment ça va?",
    "Quel est votre nom?",
    "Bonjour.",
    "Bonne nuit."
]
target_texts = [f"<starttoken> {text} <endtoken>" for text in target_texts]


max_len_input = max(len(seq.split()) for seq in input_texts)
max_len_target = max(len(seq.split()) for seq in target_texts)

# Tokenize data and pad sequences
input_vectorizer = TextVectorization(
    max_tokens=1000,
    output_mode="int",
    output_sequence_length=max_len_input,
)
target_vectorizer = TextVectorization(
    max_tokens=1000,
    output_mode="int",
    output_sequence_length=max_len_target,
)
input_vectorizer.adapt(input_texts)
input_vocab_size = len(input_vectorizer.get_vocabulary())
encoder_input_data = input_vectorizer(input_texts).numpy()
target_vectorizer.adapt(target_texts)
target_vocab_size = len(target_vectorizer.get_vocabulary())
target_sequences = target_vectorizer(target_texts).numpy()

#split into target sequences into input and output for decoder
target_input_sequences = target_sequences[:, :-1]
target_output_sequences = target_sequences[:, 1:]

# Build the Seq2Seq model
latend_dim = 256

# Encoder
encoder_inputs = Input(shape=(max_len_input,))
encoder_embedding = Embedding(input_vocab_size, latend_dim, mask_zero=True)(encoder_inputs)
encocder_lstm = LSTM(latend_dim, return_state=True)
encoder_outputs, state_h, state_c = encocder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = Input(shape=(None,))
decoder_embedding = Embedding(target_vocab_size, latend_dim, mask_zero=True)(decoder_inputs)
decoder_lstm = LSTM(latend_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = Dense(target_vocab_size, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Define and compile model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
# Train the model
model.fit([encoder_input_data, target_input_sequences], target_output_sequences, epochs=100, batch_size=64, validation_split=0.2)

# inference models for translation
encoder_model = Model(encoder_inputs, encoder_states)

# decoder inference
decoder_state_input_h = Input(shape=(latend_dim,))
decoder_state_input_c = Input(shape=(latend_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(
    decoder_embedding, initial_state=decoder_states_inputs
)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states
)
# Function to decode sequence
def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)

    # generate empty target sequence of length 1
    target_seq = np.zeros((1, 1))
    # populate first token of target sequence with the start token.
    target_seq[0, 0] = target_vectorizer.get_vocabulary().index('starttoken')

    # Sampling loop for a batch of sequences
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value
        )

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = target_vectorizer.get_vocabulary()[sampled_token_index]
        decoded_sentence += ' ' + sampled_word

        # Exit condition: either hit max length or find stop token.
        if (sampled_word == 'endtoken' or
           len(decoded_sentence.split()) > max_len_target):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index

        # Update states
        states_value = [h, c]
    
    return decoded_sentence.strip()

# Test the model
for seq_index in range(5):
    input_seq = encoder_input_data[seq_index: seq_index + 1]
    decoded_sentence = decode_sequence(input_seq)
    print(f'Input: {input_texts[seq_index]}')
    print(f'Output: {decoded_sentence}')