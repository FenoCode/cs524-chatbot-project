from transformers import T5ForConditionalGeneration, T5Tokenizer
from pypdf import PdfReader

# Load the T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Sample text 
text = """Natural language processed (NLP)) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data. The ultimate goal of NLP is to enable computers to understand, interpret, and generate human language in a valuable way. NLP combines computational linguistics with machine learning, deep learning, statistical modeling, and more. It has a wide range of applications, including language translation, sentiment analysis, chatbots, and information retrieval."""
reader = PdfReader(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\books\pdf\IAM Management - concept, challenges,solutions.pdf")
content = " ".join(p.extract_text() for p in reader.pages)
text = "" .join(content.split('\n'))
# Tokenize and encode text
inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)

# Generate the summary
summary_ids = model.generate(inputs, max_length=150, min_length=140, length_penalty=2.0, num_beams=4, early_stopping=True)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print("Summary:")
print(summary)
