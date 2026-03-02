import spacy
nlp = spacy.load("en_core_web_sm")

# Sample text
corpus = [
    "Firestorm Labs, a San Diego-based startup, plans to use 3D printing to build over 50 war-ready drones for military use.",
    "George Washington was the first President of the United States.",
]

for sent in corpus:
    doc = nlp(sent)
    print("Sentence NER elements:")
    for ent in doc.ents:
        print(ent.text, ent.label_)
    print()