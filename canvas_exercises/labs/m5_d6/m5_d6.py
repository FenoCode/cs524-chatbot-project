import json

from keras.layers import TextVectorization
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, Dropout, Embedding
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder



# ***** additional imports needed for this lab *****
import sys, getopt   #   used to read command line arguments
from nltk.tokenize import RegexpTokenizer

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split
import numpy as np # linear algebra
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
# **************************************************


def main(argv):
	# BLOCK 1 (OPTIONAL)
	# This block of code implements a simplistic argument checker
	# If the user has too many or too few arguments, the program will terminate
	try:
		opts, args = getopt.getopt(argv,"h:",["ifile="])
	except getopt.GetoptError:
		print ('lab12.py <inputfile>')
		sys.exit(1) #General Error or Abnormal Termination

	if len(sys.argv) != 2:
		print('usage: m5_d6.py [-h] [FILE NAME]\n')
		print('\noptional arguments:')
		print('  -h            show this help message and exit')
		sys.exit(1) #General Error or Abnormal Termination

	# This block of code displays the result of the '-h' (HELP) flag
	for opt, arg in opts:
		if opt == '-h':
			print ('lab12.py <inputfile>')
			sys.exit()

	# BLOCK 2 (CORE SOLUTION)
	# We now read the file provided by the user into a corpus
	inputfile = sys.argv[1]


	tokenizer = RegexpTokenizer(r'\w+')

	# Read in the data and strip newlines from the end
	corpus = [line.strip() for line in open(inputfile, 'r')]
	corpus[:] = [tokenizer.tokenize(x) for x in corpus if x != '']
	corpus[:] = [ " ".join(x)for x in corpus]


	# Load data

	data=pd.read_csv('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m5_d6\IMDB Dataset.csv')

	X=data['review']
	y=data['sentiment']

	le = LabelEncoder()
	y = le.fit_transform(data['sentiment'])

	# Split into training and testing data


	# Assume X is your list of texts and y is the corresponding sentiments
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


	# Prepare tokenizer
	t = TextVectorization(
		max_tokens=20000,         # limits vocab size like Tokenizer(num_words=20000)
		output_mode='int',        # gives integer sequences like texts_to_sequences
		output_sequence_length=100 # pads/truncates like pad_sequences
	)
	t.adapt(X)

	# Convert text into sequences of integers
	data = t(X_train)
	test_data = t(X_test)

	# Define the model
	model = Sequential()
	model.add(Embedding(20000, 100, input_length=100))
	model.add(Dropout(0.2))
	model.add(Conv1D(64, 5, activation='relu'))
	model.add(MaxPooling1D(pool_size=4))
	model.add(LSTM(100))
	model.add(Dense(1, activation='sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	# Train the model
	model.fit(data, np.array(y_train), validation_split=0.4, epochs=3)
	
	# Save model and tokenizer
	model.save('sentiment_model.keras')
	with open("text_vectorization_config.json", "w", encoding="utf-8") as f:
		json.dump(t.get_config(), f)

	with open('vocabulary.json', 'w') as f:
		json.dump(t.get_vocabulary(), f)
	
	# Evaluate on test set
	loss, accuracy = model.evaluate(test_data, np.array(y_test))
	print('Test Accuracy: %f' % (accuracy*100))

if __name__ == "__main__":
	main(sys.argv[1:])
