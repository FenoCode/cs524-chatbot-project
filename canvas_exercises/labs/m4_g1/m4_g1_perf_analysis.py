import spacy
import nltk
from nltk import word_tokenize, sent_tokenize, pos_tag
from spacy import displacy

text = "How do users authenticate to my application?"

nlp = spacy.load("en_core_web_sm")
pos_tags = pos_tag(word_tokenize(text))
ner_doc = nlp(text)
print("POS Tags:", pos_tags)
print("Named Entities:")
for ent in ner_doc.ents:
    print(f"  {ent.text} ({ent.label_})")
    
# Render dependency parsing
options = {"compact": True, "bg": "#09a3d5", "color": "white", "font": "sans-serif"}
html = displacy.render(ner_doc, style="dep", page=True, options=options)
with open("dependency_parsing.html", "w", encoding="utf-8") as f:
    f.write(html)
