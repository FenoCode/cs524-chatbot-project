import os
import spacy
import re
import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag_sents
from spacy import displacy

from collections import Counter

def clean_text(text):
    #text = text.lower()
    text = re.sub(r'https?://\S+', '<URL>', text)
    #text = re.sub(r'[^a-z0-9<> \n\r]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Required nltk and spaCy downloads
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")

# Load in chatbot corpus
corpus = open(r"F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\chatbot_corpus.txt", 'r').read()
corpus = clean_text(corpus)
corpus_sentences = sent_tokenize(corpus)
corpus_sentences = corpus_sentences[:10] # Uncomment to subset corpus for testing
corpus_tokenized_sentences = [word_tokenize(sent) for sent in corpus_sentences]
corpus_tokens = word_tokenize(corpus)

# POS (Part of Speech) tagging
print("==== POS Tagging Analysis on Corpus ====")
pos_tags = pos_tag_sents(corpus_tokenized_sentences)
print("First 3 sentences:")
for i, sent_tags in enumerate(pos_tags[:3]):
    print(f"Sentence [{i + 1}]:", sent_tags)

# NER (Named Entity Recognition) tagging
print("\n==== NER Analysis on Corpus ====")
print("==== STAGE 1: NER with spaCy ====")
ner_doc_list = []
for sent in corpus_sentences:
    doc = nlp(sent)
    ner_doc_list.append(doc)

print("==== STAGE 2: Perform ranking of NER occurences ====")
entity_counts = Counter()
for doc in ner_doc_list:
    for ent in doc.ents:
        entity_counts[(ent.label_, ent.text)] += 1

for entity, count in entity_counts.most_common(10):
    print(f"{entity}: {count}")

# Dependency parsing
print("\n==== Render Dependency Parsing ====")
options = {"compact": True, "bg": "#09a3d5", "color": "white", "font": "sans-serif"}
# Generate entity and dependency views as HTML (of selected 5 sentences)
html_ent = displacy.render(ner_doc_list[0:5], style="ent", page=True, options=options)
html_dep = displacy.render(ner_doc_list[0:5], style="dep", page=True, options=options)

combined_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SpaCy Visualization</title>
</head>
<body>
    <h2>Entity View</h2>
    {html_ent}
    <hr>
    <h2>Dependency View</h2>
    {html_dep}
</body>
</html>
"""

script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, "combined_displacy.html")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(combined_html)

print("Combined HTML saved as combined_displacy.html")