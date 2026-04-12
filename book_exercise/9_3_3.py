# NOTTE: This code was minimally changed from the original script provided by the book because the "output_attentions" on generate() is not supported in the current version of transformers. Instead, we need to call the model directly with the input and decoder_input_ids to get the attentions.

from transformers import T5ForConditionalGeneration, T5Tokenizer
# Load the T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Sample text
text = """Translate English to French: Machine learning is a subset of artificial intelligence. 
It involves algorithms and statistical models to perform tasks without explicit instructions. 
Machine learning is widely used in various applications such as image recognition, natural language processing, and autonomous driving. It relies on patterns and inference instead of predefined rules."""

# Tokenize and encode text
inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)
# Generate translation
output_ids = model.generate(inputs, max_length = 150, num_beams=4, early_stopping=True)
translation = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("Translation:")
print(translation)

# Visualize Self-Attention Scores
import matplotlib.pyplot as plt
import seaborn as sns

# Functiuon to visualize attention scores
def visualize_attention(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    # Provide a minimal decoder input (T5 uses <pad> as the start token)
    decoder_input_ids = tokenizer.encode("<pad>", return_tensors="pt")
    
    outputs = model(**inputs, decoder_input_ids=decoder_input_ids, output_attentions=True)
    attentions = outputs[-1]  # Last element contains attention scores
    
    # For simplicity, visualize the last encoder layer's first head's attention
    # attentions[0] is encoder self-attention (for T5-small, layers 0-5 are encoder)
    attention_matrix = attentions[-1][0][0].detach().numpy()  # Last encoder layer
    
    plt.figure(figsize=(10,8))
    sns.heatmap(attention_matrix, cmap="viridis")
    plt.title("Encoder Self-Attention Scores (Last Layer, First Head)")
    plt.xlabel("Input Tokens")
    plt.ylabel("Input Tokens")
    plt.show()

visualize_attention(model, tokenizer, text)