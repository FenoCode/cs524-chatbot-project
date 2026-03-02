import spacy

# Load and process doc
nlp = spacy.load("en_core_web_sm")
text = "The cat sat on the mat."
doc = nlp(text)

print("Tokens and their dependency tags:")
for token in doc:
    print(token.text, token.dep_, token.head.text)

# Visualize the dependency tree
from spacy import displacy
displacy.render(doc, style="dep", jupyter=True)