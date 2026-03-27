import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# sample text corpus
corpus = [
    "The cat sat on the mat.",
    "The dog sat on the log",
    "The cat chased the dog",
    "The dog chased the cat"
]

# Create feature and train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

lsa = TruncatedSVD(n_components=2, random_state=42)
X_reduced = lsa.fit_transform(X)

# Print terms and their corresponding components
terms = vectorizer.get_feature_names_out()
for i, comp in enumerate(lsa.components_):
    terms_comp = zip(terms, comp)
    sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:5]
    print(f"Topic {i}:")
    for term, weight in sorted_terms:
        print(f" - {term} : {weight:.4f}")

# Output:
#  Topic 0:
#   - the : 0.7179 (stop-word removal filtering would show that dog/cat are the most important in topic 1)
#   - dog : 0.3503
#   - cat : 0.3503
#   - chased : 0.3232
#   - on : 0.2192
#  Topic 1:
#   - chased : 0.4932 
#   - dog : 0.2005
#   - cat : 0.2005
#   - the : 0.0028
#   - log : -0.3114