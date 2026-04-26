import re
import numpy as np
from tensorflow import keras
from keras.layers import Input, LSTM, Dense
from keras.models import Model, load_model
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Define start and end tokens
START_TOKEN = "START"
END_TOKEN = "END"


print("Loading data files: ")
with open("human_text.txt", 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
with open("robot_text.txt", 'r', encoding='utf-8') as f:
    lines2 = f.read().split('\n')

print("Preprocessing text: ")
lines = [" ".join(re.findall(r"\w+", line)) for line in lines]
lines2 = [" ".join(re.findall(r"\w+", line)) for line in lines2]
pairs = list(zip(lines, lines2))

input_docs, target_docs = [], []
input_tokens, target_tokens = set(), set()

for input_line, target_line in pairs[:400]:
    input_docs.append(input_line)
    # Use explicit START and END tokens instead of tab and newline
    target_line = START_TOKEN + ' ' + target_line + ' ' + END_TOKEN
    target_docs.append(target_line)

    for token in re.findall(r"[\w']+|[^\s\w]", input_line):
        input_tokens.add(token)
    for token in target_line.split():
        target_tokens.add(token)

# Add START and END tokens explicitly to ensure they're in vocabulary
target_tokens.add(START_TOKEN)
target_tokens.add(END_TOKEN)

input_tokens = sorted(list(input_tokens))
target_tokens = sorted(list(target_tokens))
num_encoder_tokens = len(input_tokens)
num_decoder_tokens = len(target_tokens)

# Print values to understand
print(f"Input vocabulary size: {num_encoder_tokens}")
print(f"Target vocabulary size: {num_decoder_tokens}")
print(f"START_TOKEN in vocabulary: {START_TOKEN in target_tokens}")
print(f"END_TOKEN in vocabulary: {END_TOKEN in target_tokens}")

input_features_dict = {token: i for i, token in enumerate(input_tokens)}
target_features_dict = {token: i for i, token in enumerate(target_tokens)}
reverse_input_features_dict = {i: token for token, i in input_features_dict.items()}
reverse_target_features_dict = {i: token for token, i in target_features_dict.items()}

max_encoder_seq_length = max(len(re.findall(r"[\w']+|[^\s\w]", doc)) for doc in input_docs)
max_decoder_seq_length = max(len(doc.split()) for doc in target_docs)

print(f"Max encoder sequence length: {max_encoder_seq_length}")
print(f"Max decoder sequence length: {max_decoder_seq_length}")

encoder_input_data = np.zeros((len(input_docs), max_encoder_seq_length, num_encoder_tokens), dtype='float32')
decoder_input_data = np.zeros((len(input_docs), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
decoder_target_data = np.zeros((len(input_docs), max_decoder_seq_length, num_decoder_tokens), dtype='float32')

print("Vectorizing sequences: ")
for line, (input_doc, target_doc) in enumerate(zip(input_docs, target_docs)):
    for t, token in enumerate(re.findall(r"[\w']+|[^\s\w]", input_doc)):
        if token in input_features_dict:  
            encoder_input_data[line, t, input_features_dict[token]] = 1.
    
    target_tokens_list = target_doc.split()
    for t, token in enumerate(target_tokens_list):
        if token in target_features_dict: 
            decoder_input_data[line, t, target_features_dict[token]] = 1.
            if t > 0:  
                decoder_target_data[line, t - 1, target_features_dict[token]] = 1.

# Model setup
dimensionality = 256
batch_size = 10
epochs = 600

print("Building model: ")
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder_lstm = LSTM(dimensionality, return_state=True, activation='tanh', recurrent_activation='sigmoid', unroll=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)
encoder_states = [state_h, state_c]

decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(dimensionality, return_sequences=True, return_state=True,
                    activation='tanh', recurrent_activation='sigmoid', unroll=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

training_model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
training_model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

print("Training model: ")
training_model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
                   batch_size=batch_size, epochs=epochs, validation_split=0.2)
print("Training completed.")
training_model.save("training_model.h5")

print("Loading trained model: ")
training_model = load_model("training_model.h5")
encoder_model = Model(encoder_inputs, encoder_states)

decoder_state_input_h = Input(shape=(dimensionality,))
decoder_state_input_c = Input(shape=(dimensionality,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

def decode_response(test_input):
    states_value = encoder_model.predict(test_input)
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    
    target_seq[0, 0, target_features_dict[START_TOKEN]] = 1.

    decoded_sentence = ''
    while True:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        #sampled_index = np.argmax(output_tokens[0, -1, :])
        def sampleT(probabilities, temperature=1.0):
            predictions = np.asarray(probabilities).astype('float64')
            predictions = np.log(predictions + 1e-10) / temperature
            exp_preds = np.exp(predictions)
            predictions = exp_preds / np.sum(exp_preds)
            return np.random.choice(len(predictions), p=predictions)

        sampled_index = sampleT(output_tokens[0, -1, :], temperature=0.7)
        sampled_token = reverse_target_features_dict[sampled_index]
        
        if sampled_token == END_TOKEN:
            break
        if sampled_token != START_TOKEN:
            decoded_sentence += ' ' + sampled_token

        if len(decoded_sentence.split()) > max_decoder_seq_length:
            break

        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_index] = 1.
        states_value = [h, c]

    return decoded_sentence.strip()

class ChatBot:
    exit_commands = ("quit", "exit", "bye", "goodbye", "stop")

    def start_chat(self):
        print("ChatBot ready! Type a message or 'exit' to quit.")
        user_input = input("You: ")
        while not self.should_exit(user_input):
            response = self.generate_response(user_input)
            print("Bot:", response)
            user_input = input("You: ")
        print("Bot: Goodbye!")

    def generate_response(self, user_input):
        user_matrix = self.sentence_to_matrix(user_input)
        return decode_response(user_matrix)

    def sentence_to_matrix(self, sentence):
        tokens = re.findall(r"[\w']+|[^\s\w]", sentence)
        matrix = np.zeros((1, max_encoder_seq_length, num_encoder_tokens), dtype='float32')
        for t, token in enumerate(tokens):
            if token in input_features_dict:
                matrix[0, t, input_features_dict[token]] = 1.
        return matrix

    def should_exit(self, reply):
        return any(exit_cmd in reply.lower() for exit_cmd in self.exit_commands)

def please_chat():
    chatbot = ChatBot()
    chatbot.start_chat()

if __name__ == "__main__":
    please_chat()