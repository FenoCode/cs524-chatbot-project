import spacy

# Load pre-trained spAcy model
nlp = spacy.load('en_core_web_sm')
text = "The cat sat on the mat."

# Process w/ spaCy model and print out dependencies
doc = nlp(text)
print("Dependency Parsing:")
for token in doc:
    print(f"{token.text} ({token.dep_}): {token.head.text}")

# Visualize the dependency tree
from spacy import displacy
displacy.render(doc, style="dep", jupyter=True)