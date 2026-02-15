import os
from pathlib import Path
import pypandoc

# Retrieve corpus from '/dataset'

# Coalescing of .txt files
txt_doc_files = list(Path("F:\CS524\cs524-chatbot-project\dataset").rglob('*.txt'))
txt_doc_files = [f for f in txt_doc_files if os.path.basename(f) != "chatbot_corpus.txt"]
doc_content_list = [file.read_text(encoding='utf-8', errors='replace') for file in txt_doc_files]

# Conversion and coalescing of .md files
md_doc_files = list(Path("F:\CS524\cs524-chatbot-project\dataset").rglob('*.md'))
md_doc_files = [f for f in md_doc_files if os.path.basename(f) != "dataset.md"]
md_content_list = [file.read_text(encoding='utf-8', errors='replace') for file in md_doc_files]

# Conversion and coalescing of .csv files
csv_doc_files = list(Path("F:\CS524\cs524-chatbot-project\dataset").rglob('*.csv'))
print(csv_doc_files)


# Converts markdown formatted docs to plain text
md_content_list = [pypandoc.convert_text(file.read_text(encoding='utf-8', errors='replace'), 'plain', format='markdown') for file in md_doc_files]

# Write corpus to file
with open("F:\CS524\cs524-chatbot-project\dataset\chatbot_corpus.txt", "w", encoding='utf-8', errors='replace') as f:
    for content in doc_content_list:
        # Clean content allowing only valid UTF-8 characters
        content = ''.join(char for char in content if char.isprintable() or char.isspace())
        # Allow only alphanumeric characters and basic punctuation
        content = ''.join(char for char in content if char.isalnum() or char in " .,;:!?'-\n")
        f.write(content)