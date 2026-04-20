import json
import numpy as np
import tensorflow as tf
from keras.layers import TextVectorization
from keras.preprocessing.sequence import pad_sequences


class ChatbotInference:
    def __init__(self, artifacts: str):
        # Load models
        self.encoder_model = tf.keras.models.load_model(f"{artifacts}\encoder_model.keras")
        self.decoder_model = tf.keras.models.load_model(f"{artifacts}\decoder_model.keras")

        # Load metadata
        with open(f"{artifacts}\metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # Rebuild vectorizers
        self.input_vectorizer = TextVectorization(output_mode="int")
        self.target_vectorizer = TextVectorization(output_mode="int")

        self.input_vectorizer.set_vocabulary(metadata["input_vocab"])
        self.target_vectorizer.set_vocabulary(metadata["target_vocab"])

        # Load sequence lengths
        self.max_len_input = metadata["max_len_input"]
        self.max_len_target = metadata["max_len_target"]

        # Cache vocab + token indices (important for performance)
        self.target_vocab = self.target_vectorizer.get_vocabulary()

        self.start_token = "starttoken"
        self.end_token = "endtoken"

        self.start_index = self.target_vocab.index(self.start_token)
        self.end_index = self.target_vocab.index(self.end_token)

        print("Chatbot model loaded!")

    def generate_response(self, question: str) -> str:
        text = f"{self.start_token} {question} {self.end_token}"

        seq = self.input_vectorizer([text])
        seq = pad_sequences(seq, maxlen=self.max_len_input, padding="post")

        return self._decode_sequence(seq)

    def _decode_sequence(self, input_seq):
        states_value = self.encoder_model.predict(input_seq, verbose=0)

        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = self.start_index

        decoded_tokens = []

        while True:
            output_tokens, h, c = self.decoder_model.predict(
                [target_seq] + states_value,
                verbose=0
            )

            sampled_token_index = int(np.argmax(output_tokens[0, -1, :]))
            sampled_word = self.target_vocab[sampled_token_index]

            # Stop condition
            if sampled_word == self.end_token or len(decoded_tokens) > self.max_len_target:
                break

            decoded_tokens.append(sampled_word)

            # Update next step
            target_seq[0, 0] = sampled_token_index
            states_value = [h, c]

        return " ".join(decoded_tokens)