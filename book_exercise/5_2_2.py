import spacy

# Load pre-trained spacy model
nlp = spacy.load("en_core_web_sm")

# Sample text
text = "Apple is looking at buying U.K. startup for 1 billion."

# Process text w/ spacy model
doc = nlp(text)

# Print named entities with their labels
print("Named entities:") 
for ent in doc.ents:
    print(ent.text, ent.label_)
