from transformers import BartForConditionalGeneration, BartTokenizer

# Load the BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

summary = []
# Sample text 
text = open("F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m7_d5\m7_d5.txt", 'r').read()

# Tokenize and encode text and generate summary
inputs = tokenizer.encode("summarize: " + text, max_length=1024, truncation=True, padding=True, return_overflowing_tokens=True, stride=128,return_tensors="pt")

for input_slice in inputs.split(1024, dim=1):
    summary_ids = model.generate(input_slice, min_length=40, max_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary_snippet = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    summary.append(summary_snippet)

print("Summary:")
print(' '.join(summary))
