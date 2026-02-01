# Lab: 3 (Batched Version)
# Purpose: Extract token-level BERT embeddings using batched inference
# NOTE: This produces the same embeddings as the original script. It uses batching for efficiency.

import sys, getopt
import os, csv
from collections import OrderedDict

import torch
import numpy as np

from transformers import BertModel, BertTokenizer

# --------------------------------------------------
# Model + Tokenizer (unchanged)
# --------------------------------------------------
model = BertModel.from_pretrained(
    "bert-base-uncased",
    output_hidden_states=True
)
model.eval()

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# --------------------------------------------------
# Batched text preparation (REPLACES bert_text_preparation)
# --------------------------------------------------
def prepare_batch(sentences, tokenizer):
    """
    Prepares a batch of sentences for BERT.
    Equivalent to individual [CLS] ... [SEP] processing.
    """
    marked = ["[CLS] " + s + " [SEP]" for s in sentences]

    encoding = tokenizer(
        marked,
        padding=True,
        truncation=True,
        return_tensors="pt",
        add_special_tokens=False   # IMPORTANT: we already added CLS/SEP
    )

    return (
        encoding["input_ids"],
        encoding["token_type_ids"],
        encoding["attention_mask"],
        encoding["input_ids"]
    )

# --------------------------------------------------
# Batched embedding extraction (REPLACES get_bert_embeddings)
# --------------------------------------------------
def get_batch_embeddings(input_ids, token_type_ids, attention_mask, model):
    """
    Returns token embeddings summed over the last 4 layers.
    Output shape: [batch_size, seq_len, 768]
    """
    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
            attention_mask=attention_mask,
            output_hidden_states=True
        )

    # Last 4 layers
    hidden_states = outputs.hidden_states[-4:]

    # Stack -> sum over layers
    token_embeddings = torch.stack(hidden_states, dim=0).sum(dim=0)

    return token_embeddings

# --------------------------------------------------
# Main
# --------------------------------------------------
def main(argv):

    try:
        opts, args = getopt.getopt(argv, "h:", ["ifile="])
    except getopt.GetoptError:
        print("lab3_batched.py <inputfile>")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("usage: lab3_batched.py [FILE NAME]")
        sys.exit(1)

    for opt, arg in opts:
        if opt == "-h":
            print("lab3_batched.py <inputfile>")
            sys.exit()

    inputfile = sys.argv[1]

    corpus = [line.strip() for line in open(inputfile, "r", encoding='utf-8', errors='replace') if line.strip()]

    print("\nBERT Embeddings (Batched)\n")

    batch_size = 8   # Safe default; increase if memory allows

    context_tokens = []
    context_embeddings = []

    for i in range(0, len(corpus), batch_size):
        batch_sentences = corpus[i:i+batch_size]

        input_ids, token_type_ids, attention_mask, ids = prepare_batch(
            batch_sentences, tokenizer
        )

        batch_embeddings = get_batch_embeddings(
            input_ids, token_type_ids, attention_mask, model
        )

        # --------------------------------------------------
        # Recover per-token embeddings EXACTLY like original
        # --------------------------------------------------
        for batch_idx, sentence in enumerate(batch_sentences):

            tokenized_text = tokenizer.tokenize(
                "[CLS] " + sentence + " [SEP]"
            )

            tokens = OrderedDict()

            for token in tokenized_text[1:-1]:

                if token in tokens:
                    tokens[token] += 1
                else:
                    tokens[token] = 1

                token_indices = [
                    i for i, t in enumerate(tokenized_text) if t == token
                ]
                current_index = token_indices[tokens[token] - 1]

                token_vec = batch_embeddings[batch_idx, current_index]

                context_tokens.append(token)
                context_embeddings.append(token_vec)

    # --------------------------------------------------
    # Write outputs (unchanged behavior)
    # --------------------------------------------------
    with open("metadata_small.tsv", "w+", encoding='utf-8', errors='replace') as f:
        for token in context_tokens:
            f.write(token + "\n")

    with open("embeddings_small.tsv", "w+", encoding='utf-8', errors='replace') as f:
        writer = csv.writer(f, delimiter="\t")
        for emb in context_embeddings:
            writer.writerow(emb.numpy())

# --------------------------------------------------
if __name__ == "__main__":
    main(sys.argv[1:])
