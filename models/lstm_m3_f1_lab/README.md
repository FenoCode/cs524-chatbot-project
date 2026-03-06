# Initial Experimentation

First, an character-prediction LSTM was attempted with the following parameters:

| Corpus Size | Epoch Count | Vocab Size | Loss Algorithm | Model Structure |
| :---- | :---- | :---- | :---- | :---- |
| 300k | 200 | 48 | categorical\_crossentropy | LSTM (50 units) Dense Softmax |

This model structure performed horribly, as it repeated characters in a loop shortly after the first couple of predictions:  
**Input**: “What is identity and access management?”  
**Output**: “What is identity and access management? rere trere t”

Adjusting the epoch count and LSTM size helped some, but it seemed to be architecturally limited. That is when it was selected to do a next-word token model. The following parameters were attempted:

| Corpus Size | Epoch Count | Vocab Size | Loss Algorithm | Model Structure |
| :---- | :---- | :---- | :---- | :---- |
| 10k | 200 | 6.8k | categorical\_crossentropy | LSTM (100 units) Dense Softmax |

The reason the corpus size was decreased was because memory exploded with one-hot encoding for the output vector. This model overfitted and performed poorly because the corpus was so small.

It was then decided to choose Sparse Categorical Crossentropy to reduce the memory footprint 6800x\! This finding was absolutely paramount. With the combination of using dataset batching and the different loss algorithm, real results were beginning to form. Thus, the experiment was in a stage where hyperparameter tuning would be a worthy effort.

# Hyperparameter Experimentation

The following model structures were trained with these sets of parameters:

| Corpus Token Size | Vocab Size | Batch Size | Epoch Count |
| :---- | :---- | :---- | :---- |
| 300k | 5.7k | 64 | 10 |

The following model architectures and their accuracy and loss at Epoch 10 was recorded:

| \# | Architecture | Training Time | Final Accuracy | Final Loss |
| :---- | :---- | :---- | :---- | :---- |
| 1 | `model = Sequential([     Embedding(vocab_size, 256),     LSTM(256),     Dense(vocab_size, activation='softmax') ])`  | 1 hr 5 min | 0.6174 | 1.4698 |
| 2 | `model = Sequential([     Embedding(vocab_size, 1024),     LSTM(256),     Dense(vocab_size, activation='softmax') ])` | 1 hr 45 min | 0.5837 | 1.6651 |
| 3 | `model = Sequential([     Embedding(vocab_size, 256),     LSTM(256, return_sequences=True),     LSTM(128),     Dense(vocab_size, activation='softmax') ])`  | 1hr 45 min | 0.5754 | 1.7148 |

The script located in Appendix B shows the code used to train and evaluate the model.