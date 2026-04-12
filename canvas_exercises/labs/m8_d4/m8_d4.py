from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en")

# Sample text
text = """Translate Spanish to English: El rapido zorro marron salta sobre el perro perezoso."""

# Tokenize and encode text
inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)
# Generate translation
output_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)
translation = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("Translation:")
print(translation)