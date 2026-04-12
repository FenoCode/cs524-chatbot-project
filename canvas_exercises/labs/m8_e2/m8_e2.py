from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pypdf import PdfReader
import re

SOURCE_LANGUAGE = 'english'
TARGET_LANGUAGE = 'spanish'
SOURCE_TO_TARGET_MODEL = "Helsinki-NLP/opus-mt-en-es"
TARGET_TO_SOURCE_MODEL = "Helsinki-NLP/opus-mt-es-en"
MAX_LENGTH = 256
MODEL_MAX_LENGTH = 512

# Load text from PDF
def load_text_from_pdf(path):
    reader = PdfReader(path)
    content = " ".join(p.extract_text() for p in reader.pages if p.extract_text())
    return " ".join(content.split('\n'))

# Pre-processing function to clean text
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text) # Remove links
    text = re.sub(r'[^a-zA-Z.,!?;:\s]', '', text) # Remove special characters and numbers (keep only letters and basic punctuation)
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    return text.strip()

def chunk_text(sentences, tokenizer, max_chunk_length=512):
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        temp = current_chunk + " " + sentence
        token_count = len(tokenizer.encode(temp, truncation=False))

        if token_count < max_chunk_length:
            current_chunk = temp
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip()) 

    return chunks

def tokenize_text(text, tokenizer, max_length=512):
    return tokenizer.encode(text, return_tensors="pt", max_length=max_length)
    
    
# Chatbot corpus text
text = load_text_from_pdf(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\books\pdf\2012-HaagSpruit.pdf")
text = preprocess_text(text)
sentences = sent_tokenize(text)


### STEP 1: English -> Spanish ###

# Split chunks and tokenize
tokenizer = AutoTokenizer.from_pretrained(SOURCE_TO_TARGET_MODEL)
ref_text_chunks = chunk_text(sentences, tokenizer=tokenizer, max_chunk_length=MAX_LENGTH)
ref_text_chunks = ref_text_chunks[2:3] # NOTE: Slicing text for demonstration purposes
print(" ".join(ref_text_chunks))
text_chunk_tokens = [tokenize_text(chunk, tokenizer=tokenizer, max_length=MAX_LENGTH) for chunk in ref_text_chunks]
# English to Spanish model
model = AutoModelForSeq2SeqLM.from_pretrained(SOURCE_TO_TARGET_MODEL)

target_language_translation = []

# Generate target lnguage translation for each chunk
for token_chunk in text_chunk_tokens:
    output_ids = model.generate(token_chunk, num_beams=4, early_stopping=True)
    translation_chunk = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    target_language_translation.append(translation_chunk)

print("Translation:")
print(" ".join(target_language_translation))

### STEP 2: Spanish -> English ###

# Split chunks and tokenize
sentences = sent_tokenize(" ".join(target_language_translation))
tokenizer = AutoTokenizer.from_pretrained(TARGET_TO_SOURCE_MODEL)
text_chunks = chunk_text(sentences, tokenizer=tokenizer, max_chunk_length=MAX_LENGTH)
text_chunk_tokens = [tokenize_text(chunk, tokenizer=tokenizer, max_length=MAX_LENGTH) for chunk in text_chunks]
# English to Spanish model
model = AutoModelForSeq2SeqLM.from_pretrained(TARGET_TO_SOURCE_MODEL)

source_language_translation = []

# Generate target lnguage translation for each chunk
for token_chunk in text_chunk_tokens:
    output_ids = model.generate(token_chunk, num_beams=4, early_stopping=True)
    translation_chunk = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    source_language_translation.append(translation_chunk)

print("Translation:")
print(" ".join(source_language_translation))

### STEP 3: Compute BLEU evaluation metrics
references = []
hypotheses = []
# Perform word tokenization for BLEU score calculation
for ref, pred in zip(ref_text_chunks, source_language_translation):
    ref_tokens = word_tokenize(ref, language=SOURCE_LANGUAGE)
    pred_tokens = word_tokenize(pred, language=SOURCE_LANGUAGE)

    references.append([ref_tokens]) # Double list reuired for BLEU
    hypotheses.append(pred_tokens)

# Calculate BLEU score for the entire corpus
bleu_score_corpus = corpus_bleu(list_of_references=references, hypotheses=hypotheses)
print("Corpus BLEU Score: ", bleu_score_corpus)