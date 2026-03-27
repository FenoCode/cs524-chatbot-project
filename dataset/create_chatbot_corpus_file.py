import os
import re
import pypandoc
from pypdf import PdfReader
import csv
from pathlib import Path
from nltk.tokenize import sent_tokenize

ROOT_DATASET_PATH = "F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset"
def unpack_text(text):
    return text.encode('utf-8').decode('unicode_escape')

# Returns a list of strings containg formatted metadata of the tickets
def create_ticket_corpus(input_csv):
    chatbot_corpus = []
    with open(input_csv, newline='', encoding='utf-8', mode='r') as f:
        reader = csv.DictReader(f)

        index = 0
        for row in reader:
            if row["language"].strip().lower() != "en":
                continue # Skip non-english tickets
            
            ticket_type = row["type"].strip()
            category = row["tag_1"].strip() + " - " + row["tag_2"].strip()
            subject = row["subject"].strip()
            body = unpack_text(row["body"].strip())
            answer = unpack_text(row["answer"].strip())

            content = f"{body}\n{answer}"
            chatbot_corpus.append(content)
        
    
    return chatbot_corpus
# Retrieve corpus from '/dataset'

# Coalescing of .txt files
txt_doc_files = list(Path(ROOT_DATASET_PATH).rglob('*.txt'))
txt_doc_files = [f for f in txt_doc_files if os.path.basename(f) != "chatbot_corpus.txt"]
doc_content_list = [file.read_text(encoding='utf-8', errors='replace') for file in txt_doc_files]

# Conversion and coalescing of .md files
md_doc_files = list(Path(ROOT_DATASET_PATH).rglob('*.md'))
md_doc_files = [f for f in md_doc_files if os.path.basename(f) != "dataset.md"]
md_content_list = [file.read_text(encoding='utf-8', errors='replace') for file in md_doc_files]
md_content_list = [pypandoc.convert_text(file.read_text(encoding='utf-8', errors='replace'), 'plain', format='markdown') for file in md_doc_files]

# Conversion and coalescing of .csv files
ticket_corpus = create_ticket_corpus(f"{ROOT_DATASET_PATH}\customer_support_tickets\\aa_dataset-tickets-multi-lang-5-2-50-version.csv")

# Conversion and coalescing of .pdf files
pdf_doc_files = list(Path(ROOT_DATASET_PATH).rglob('*.pdf'))
pdf_doc_content = []
for pdf_file in pdf_doc_files:
    try:
        reader = PdfReader(str(pdf_file))
        content = "\n".join(p.extract_text() for p in reader.pages)
        
        # custom logic for specific file terms
        if (pdf_file.name == "practical-identity-management-with-midpoint.pdf"):
            content = re.sub('midpoint', 'IGA', content, flags=re.IGNORECASE)

        pdf_doc_content.append(content)
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")

# Combine all content into a single list
doc_content_list.extend(md_content_list)
#doc_content_list.extend(ticket_corpus)
doc_content_list.extend(pdf_doc_content)

# Tokenize into sentences and filter out short sentences
filtered_sentences = []
for content in doc_content_list:
    sentences = sent_tokenize(content)
    for sentence in sentences:
        if len(sentence.split()) >= 7:  # Filter out sentences with less than 7 words
            filtered_sentences.append(sentence)

# Write corpus to file
with open(f"{ROOT_DATASET_PATH}\chatbot_corpus.txt", "w", encoding='utf-8', errors='replace') as f:
    for content in filtered_sentences:
        # Clean content allowing only valid UTF-8 characters
        content = ''.join(char for char in content if char.isprintable() or char.isspace())
        # Allow only alphanumeric characters, basic punctuation, and separation characters
        content = ''.join(char for char in content if char.isalnum() or char in " .,;:!?'-\n/\\[]()")
        f.write(content)