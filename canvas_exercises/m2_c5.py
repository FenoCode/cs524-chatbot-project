from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Read content
text = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\m2_c5_text.txt').read()
text_tokens = word_tokenize(text.lower())

stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in text_tokens if word not in stop_words]

vectorizer = TfidfVectorizer(ngram_range=(2,2))
X = vectorizer.fit_transform([' '.join(filtered_tokens)])
features = vectorizer.get_feature_names_out()
vector = X.toarray()[0]

word_tfidf_list = sorted(zip(features, vector), key=lambda item: item[1], reverse=True)
for word, tfidf in word_tfidf_list:
    print(f"{word}: {tfidf}")