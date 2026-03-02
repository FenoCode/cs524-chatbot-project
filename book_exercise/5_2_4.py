import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.util import minibatch, compounding

# Create blank English model
nlp = spacy.blank("en")

# Create a new NER component and add to the pipeline
ner = nlp.add_pipe("ner")
ner.add_label("GADGET")

# Sample training data
TRAIN_DATA = [
    ("Apple is releasing a new iPhone.", {"entities": [(26, 32, "GADGET")]}),
    ("The new iPad Pro is amazing", {"entities": [(8, 16, "GADGET")]})
]

# Convert training data to spaCy's format and build Example objects
# (DocBin is unnecessary for such a small dataset)
examples = []
for text, annotations in TRAIN_DATA:
    doc = nlp.make_doc(text)
    examples.append(Example.from_dict(doc, annotations))


# Train NER model
optimizer = nlp.begin_training()
for each in range(10):
    losses = {}
    batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        nlp.update(batch, drop=0.5, losses=losses)
    print("Losses", losses)

# Test the trained model
doc = nlp("I just bought a new iPad Pro.")
print("Named Entities:", doc.ents)