# This code was minimally changed from the original script provided by the book because the "output_attentions" on generate() is not supported in the current version of transformers. Instead, we need to call the model directly with the input and decoder_input_ids to get the attentions.
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import T5Tokenizer, T5ForConditionalGeneration

# =========================
# Load model + tokenizer
# =========================
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

model.eval()

# =========================
# Input text
# =========================
# Sample text
text = """Translate English to French: Machine learning is a subset of artificial intelligence. 
It involves algorithms and statistical models to perform tasks without explicit instructions. 
Machine learning is widely used in various applications such as image recognition, natural language processing, and autonomous driving. It relies on patterns and inference instead of predefined rules."""

inputs = tokenizer(
    text,
    return_tensors="pt",
    max_length=128,
    truncation=True
)

input_ids = inputs["input_ids"]

# =========================
# Create decoder inputs
# =========================
# T5 uses shifted decoder inputs
decoder_input_ids = model._shift_right(input_ids)

# =========================
# Forward pass WITH attentions
# =========================
with torch.no_grad():
    outputs = model(
        input_ids=input_ids,
        decoder_input_ids=decoder_input_ids,
        output_attentions=True,
        return_dict=True
    )

# =========================
# Extract attentions
# =========================
encoder_attn = outputs.encoder_attentions      # tuple: (layers, batch, heads, seq, seq)
decoder_attn = outputs.decoder_attentions
cross_attn   = outputs.cross_attentions

# =========================
# Convert tokens for labels
# =========================
input_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
decoder_tokens = tokenizer.convert_ids_to_tokens(decoder_input_ids[0])

# =========================
# Visualization function
# =========================
def plot_attention(attn, tokens_x, tokens_y, title):
    """
    attn: (layers, batch, heads, seq_len, seq_len)
    """
    # Take last layer, first head
    matrix = attn[-1][0][0].detach().cpu().numpy()

    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, xticklabels=tokens_x, yticklabels=tokens_y)

    plt.title(title)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

# =========================
# Plot attentions
# =========================

# Encoder self-attention
plot_attention(
    encoder_attn,
    input_tokens,
    input_tokens,
    "Encoder Self-Attention"
)

# Decoder self-attention
plot_attention(
    decoder_attn,
    decoder_tokens,
    decoder_tokens,
    "Decoder Self-Attention"
)

# Cross attention (decoder attending to encoder)
plot_attention(
    cross_attn,
    input_tokens,
    decoder_tokens,
    "Cross Attention (Decoder → Encoder)"
)