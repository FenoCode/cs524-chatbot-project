from nltk import pos_tag
from nltk.corpus import treebank
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import nltk
nltk.download('treebank')

# Load treebank corpus
test_data = treebank.tagged_sents()[3000:]
test_sentences = [[word for word, tag in sent] for sent in test_data]
gold_standard = [[tag for word, tag in sent] for sent in test_data]

# Tag the test sentences using a pre-trained tagger
tagger = nltk.PerceptronTagger()
predicted_tags = [tagger.tag(sent) for sent in test_sentences]
predicted_tags = [[tag for word, tag in sent] for sent in predicted_tags]

# Flatten lists into compute metrics
gold_standard_flat = [tag for sent in gold_standard for tag in sent]
predicted_tags_flat = [tag for sent in predicted_tags for tag in sent]

# Compute evaluation metrics
accuracy = accuracy_score(gold_standard_flat, predicted_tags_flat)
precision = precision_score(gold_standard_flat, predicted_tags_flat, average='weighted')
recall = recall_score(gold_standard_flat, predicted_tags_flat, average='weighted')
f1 = f1_score(gold_standard_flat, predicted_tags_flat, average='weighted')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
