from transformers import BartForConditionalGeneration, BartTokenizer
import torch

# Load model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

summary = []

# Load text
file_path = r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m7_d5\m7_d5.txt"
text = open(file_path, 'r', encoding='utf-8').read()

# -----------------------------
# STEP 1: PROPER TOKEN CHUNKING
# -----------------------------
def chunk_text(text, tokenizer, max_tokens=900, stride=100):
    tokens = tokenizer.encode(text, return_tensors="pt")[0]
    
    chunks = []
    start = 0
    
    while start < len(tokens):
        end = start + max_tokens
        chunk = tokens[start:end]
        chunks.append(chunk)
        start += (max_tokens - stride)
    
    return chunks


chunks = chunk_text(text, tokenizer)

# -----------------------------
# STEP 2: SUMMARIZE EACH CHUNK
# -----------------------------
for i, chunk in enumerate(chunks):
    print(f"Summarizing chunk {i+1}/{len(chunks)}")

    input_ids = chunk.unsqueeze(0)  # add batch dimension

    summary_ids = model.generate(
        input_ids,
        min_length=40,
        max_length=120,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    summary_snippet = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    summary.append(summary_snippet)

# -----------------------------
# STEP 3: MERGE CHUNK SUMMARIES
# -----------------------------
combined_summary = " ".join(summary)

print("\n--- INTERMEDIATE SUMMARY ---")
print(combined_summary)

# -----------------------------
# STEP 4 (OPTIONAL BUT RECOMMENDED): FINAL SUMMARY PASS
# -----------------------------
final_inputs = tokenizer.encode(
    combined_summary,
    return_tensors="pt",
    max_length=1024,
    truncation=True
)

final_summary_ids = model.generate(
    final_inputs,
    min_length=60,
    max_length=180,
    length_penalty=2.0,
    num_beams=4,
    early_stopping=True
)

final_summary = tokenizer.decode(final_summary_ids[0], skip_special_tokens=True)

print("\n================ FINAL SUMMARY ================")
print(final_summary)