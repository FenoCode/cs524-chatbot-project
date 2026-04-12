import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding, Concatenate, TimeDistributed, Attention
from keras.preprocessing.sequence import pad_sequences
from keras.layers import TextVectorization;

# sample data
input_texts = [
    "i am happy",
    "i am sad",
    "i am tired",
    "you are happy",
    "you are sad",
    "you are tired",
    "he is happy",
    "he is sad",
    "he is tired",
    "she is happy",
    "she is sad",
    "she is tired",
    "we are happy",
    "we are sad",
    "we are tired",
    "they are happy",
    "they are sad",
    "they are tired"
]
input_texts = [f"<starttoken> {text} <endtoken>" for text in input_texts]

target_texts = [
    "je suis heureux",
    "je suis triste",
    "je suis fatigue",
    "tu es heureux",
    "tu es triste",
    "tu es fatigue",
    "il est heureux",
    "il est triste",
    "il est fatigue",
    "elle est heureuse",
    "elle est triste",
    "elle est fatiguee",
    "nous sommes heureux",
    "nous sommes tristes",
    "nous sommes fatigues",
    "ils sont heureux",
    "ils sont tristes",
    "ils sont fatigues"
]

target_texts = [f"<starttoken> {text} <endtoken>" for text in target_texts]


#max_len_input = max(len(seq.split()) for seq in input_texts)
#max_len_target = max(len(seq.split()) for seq in target_texts)

# Tokenize data and pad sequences
input_vectorizer = TextVectorization(
    max_tokens=1000,
    output_mode="int",
)
target_vectorizer = TextVectorization(
    max_tokens=1000,
    output_mode="int",
)
input_vectorizer.adapt(input_texts)
input_vocab_size = len(input_vectorizer.get_vocabulary())
encoder_input_data = input_vectorizer(input_texts).numpy()
max_len_input = max(len(seq) for seq in encoder_input_data)
encoder_input_data = pad_sequences(encoder_input_data, maxlen=max_len_input, padding='post')

target_vectorizer.adapt(target_texts)
target_vocab_size = len(target_vectorizer.get_vocabulary())
target_sequences = target_vectorizer(target_texts).numpy()
max_len_target = max(len(seq) for seq in target_sequences)
target_sequences = pad_sequences(target_sequences, maxlen=max_len_target, padding='post')

#split into target sequences into input and output for decoder
target_input_sequences = target_sequences[:, :-1]
target_output_sequences = target_sequences[:, 1:]

# Build the Seq2Seq model with Attention
latend_dim = 256

# Encoder
encoder_inputs = Input(shape=(max_len_input,))
encoder_embedding = Embedding(input_vocab_size, latend_dim, mask_zero=True)(encoder_inputs)
encocder_lstm = LSTM(latend_dim, return_sequences=True, return_state=True)
encoder_outputs, state_h, state_c = encocder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = Input(shape=(None,))
decoder_embedding_layer = Embedding(target_vocab_size, latend_dim)
decoder_embedding = decoder_embedding_layer(decoder_inputs)
decoder_lstm = LSTM(latend_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)

# Attention mechanism
attention = Attention()([decoder_outputs, encoder_outputs])
decoder_combined_context = Concatenate(axis=-1)([decoder_outputs, attention])

# Dense layer to generate predictions
decoder_dense = TimeDistributed(Dense(target_vocab_size, activation='softmax'))
decoder_outputs = decoder_dense(decoder_combined_context)

# Define and compile model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
# Train the model
model.fit([encoder_input_data, target_input_sequences], target_output_sequences, epochs=100, batch_size=64, validation_split=0.2)

# inference models for translation
encoder_model = Model(encoder_inputs, [encoder_outputs] + encoder_states)

# decoder inference
decoder_state_input_h = Input(shape=(latend_dim,))
decoder_state_input_c = Input(shape=(latend_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_hidden_states_input = Input(shape=(max_len_input, latend_dim))

decoder_outputs, state_h, state_c = decoder_lstm(
    decoder_embedding,
    initial_state=decoder_states_inputs
)

attention_output = Attention()([decoder_outputs, decoder_hidden_states_input])
decoder_combined = Concatenate(axis=-1)([decoder_outputs, attention_output])

decoder_outputs = decoder_dense(decoder_combined)

decoder_model = Model(
    [decoder_inputs, decoder_hidden_states_input, decoder_state_input_h, decoder_state_input_c],
    [decoder_outputs, state_h, state_c]
)

# Function to decode sequence
def decode_sequence(input_seq):
    encoder_out, h, c = encoder_model.predict(input_seq)

    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = target_vectorizer.get_vocabulary().index('starttoken')

    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq, encoder_out, h, c]
        )

        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = target_vectorizer.get_vocabulary()[sampled_token_index]

        decoded_sentence += ' ' + sampled_word

        if (sampled_word == 'endtoken' or
            len(decoded_sentence.split()) > max_len_target):
            stop_condition = True

        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index

    return decoded_sentence.strip()

# Test the model
for seq_index in range(5):
    input_seq = encoder_input_data[seq_index: seq_index + 1]
    decoded_sentence = decode_sequence(input_seq)
    print(f'Input: {input_texts[seq_index]}')
    print(f'Output: {decoded_sentence}')