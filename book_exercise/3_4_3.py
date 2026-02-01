from transformers import BertTokenizer, BertModel
import torch

# load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

#Sample text
text = "Natural Language is fascinating."

# Tokenize text w/ BERT
inputs = tokenizer(text, return_tensors='pt')

# Generate BERT embeddings
with torch.no_grad():
    outputs = model(**inputs)

# Get embeddings for the [CLS] t oken (represending the entire input text)
cls_embeddings =  outputs.last_hidden_state[:, 0, :]

print ("BERT embeddings for text:")
print(cls_embeddings)