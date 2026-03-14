from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Read content
text = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\m2_b5_text.txt').read()
text_tokens = word_tokenize(text.lower())

stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in text_tokens if word not in stop_words]

vc = CountVectorizer()
# Rejoins tokens to form a single string for CountVectorizer
X = vc.fit_transform([' '.join(filtered_tokens)])
features = vc.get_feature_names_out()
vector = X.toarray()[0]

word_count_list = sorted(zip(features, vector), key=lambda item: item[1], reverse=True)
for word, count in word_count_list:
    print(f"{word}: {count}")
