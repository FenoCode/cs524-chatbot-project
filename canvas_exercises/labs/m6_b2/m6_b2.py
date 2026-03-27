from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

# text corpus
corpus = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m6_b2\m6_b2.txt', 'r').read()

# Vectorize and train model
vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(corpus.splitlines())
lsa = TruncatedSVD(n_components=8)
X_reduced = lsa.fit_transform(X)

# Print terms and their corresponding components
terms = vectorizer.get_feature_names_out()
for i, comp in enumerate(lsa.components_):
    terms_comp = zip(terms, comp)
    sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:5]
    print(f"Topic {i}:")
    for term, weight in sorted_terms:
        print(f" - {term} : {weight:.4f}")