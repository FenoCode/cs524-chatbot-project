

#Lab: 3
#Author: Barnett, J., Phd
#Date: 07 Feb 2024
#Purpose: Use BERT to extract features, namely word and sentence embedding vectors, from text data 

import nltk													#	(required) Natural Language Toolkit
from nltk.tokenize import word_tokenize, sent_tokenize 		#	(required) Natural Language Toolkit
from nltk.stem import WordNetLemmatizer						#	(require) NLT

import sys, getopt											#	(optional) 
															#	used to read command line arguments

import torch													# Lab 3 specific requirements
import pandas as pd												# Lab 3 specific requirements
import numpy as np												# Lab 3 specific requirements

from transformers import BertModel, BertTokenizer				# Lab 3 specific requirements

import os														# Lab 3 specific requirements
import csv

model = BertModel.from_pretrained('bert-base-uncased',
           output_hidden_states = True,)


# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
logging.basicConfig(level=logging.INFO)


# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')	# Lab 3 specific requirements

def bert_text_preparation(text, tokenizer):
	"""
	Preprocesses text input in a way that BERT can interpret.
	"""
	marked_text = "[CLS] " + text + " [SEP]"
	tokenized_text = tokenizer.tokenize(marked_text)
	indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
	segments_ids = [1]*len(indexed_tokens)

# convert inputs to tensors
	tokens_tensor = torch.tensor([indexed_tokens])
	segments_tensor = torch.tensor([segments_ids])
	return tokenized_text, tokens_tensor, segments_tensor

def get_bert_embeddings(tokens_tensor, segments_tensor, model):
	"""
	Obtains BERT embeddings for tokens.
	"""
	# gradient calculation id disabled
	with torch.no_grad():
		# obtain hidden states
		outputs = model(tokens_tensor, segments_tensor)
		hidden_states = outputs[2]

	# concatenate the tensors for all layers
	# use "stack" to create new dimension in tensor
	token_embeddings = torch.stack(hidden_states, dim=0)

	# remove dimension 1, the "batches"
	token_embeddings = torch.squeeze(token_embeddings, dim=1)

	# swap dimensions 0 and 1 so we can loop over tokens
	token_embeddings = token_embeddings.permute(1,0,2)

	# intialized list to store embeddings
	token_vecs_sum = []

	# "token_embeddings" is a [Y x 12 x 768] tensor
	# where Y is the number of tokens in the sentence

	# loop over tokens in sentence
	for token in token_embeddings:

	# "token" is a [12 x 768] tensor

	# sum the vectors from the last four layers
		sum_vec = torch.sum(token[-4:], dim=0)
		token_vecs_sum.append(sum_vec)
	return token_vecs_sum


def main(argv):
	# BLOCK 1 (OPTIONAL)
	# This block of code implements a simplistic argument checker
	# If the user has too many or too few arguments, the program will terminate
	try:
		opts, args = getopt.getopt(argv,"h:",["ifile="])
	except getopt.GetoptError:
		print ('lab3.py <inputfile>')
		sys.exit(1)	#General Error or Abnormal Termination

	if len(sys.argv) != 2:
		print('usage: lab3.py [-h] [FILE NAME]\n')
		print('\noptional arguments:')
		print('  -h            show this help message and exit')
		sys.exit(1)	#General Error or Abnormal Termination

	# This block of code displays the result of the '-h' (HELP) flag
	for opt, arg in opts:
		if opt == '-h':
			print ('lab3.py <inputfile>')
			sys.exit()

	# BLOCK 2 (CORE SOLUTION)
	# We now read the file provided by the user into a corpus
	inputfile = sys.argv[1]

	# Read in the data and strip newlines from the end
	corpus = [line.strip() for line in open(inputfile, 'r', encoding='utf-8', errors='replace')]
	# using list comprehension to
	# perform removal
	corpus = [i for i in corpus if i]

	print("\nBERT Embeddings\n")
	from collections import OrderedDict
	context_embeddings = []
	context_tokens = []

	for sentence in corpus:
		tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(sentence, tokenizer)
		list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model)

		# make ordered dictionary to keep track of the position of each   word
		tokens = OrderedDict()
		# loop over tokens in sensitive sentence
		for token in tokenized_text[1:-1]:
			# keep track of position of word and whether it occurs multiple times
			if token in tokens:
				tokens[token] += 1
			else:
				tokens[token] = 1
			# compute the position of the current token
			token_indices = [i for i, t in enumerate(tokenized_text) if t == token]
			current_index = token_indices[tokens[token]-1]

			# get the corresponding embedding
			token_vec = list_token_embeddings[current_index]

			# save values
			context_tokens.append(token)
			context_embeddings.append(token_vec)

		# We can use the TensorBoard by TensorFlow to visualize our multi-dimensional word embeddings. 
		# In order to do this, we first have to save the BERT embeddings that we generated above as .tsv files.
		filepath = os.path.join('')

		name = 'metadata_small.tsv'
		with open(os.path.join(filepath, name), 'w+', encoding='utf-8') as file_metadata:

			for i, token in enumerate(context_tokens):
				file_metadata.write(token + '\n')

		name = 'embeddings_small.tsv'
		with open(os.path.join(filepath, name), 'w+', encoding='utf-8') as tsvfile:
			writer = csv.writer(tsvfile, delimiter='\t')

			for embedding in context_embeddings:
				writer.writerow(embedding.numpy())

if __name__ == "__main__":
	main(sys.argv[1:])
