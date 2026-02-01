from pathlib import Path

# Retrieve corpus from '/dataset'
doc_files = list(Path("F:\CS524\cs524-chatbot-project\dataset").rglob('*.txt'))
doc_content_list = [file.read_text(encoding='utf-8', errors='replace') for file in doc_files]

# Write corpus to file
with open("chatbot_corpus.txt", "w", encoding='utf-8', errors='replace') as f:
    for content in doc_content_list:
        # Clean content allowing only valid UTF-8 characters
        content = ''.join(char for char in content if char.isprintable() or char.isspace())
        # Allow only alphanumeric characters and basic punctuation
        content = ''.join(char for char in content if char.isalnum() or char in " .,;:!?'-\n")
        f.write(content)