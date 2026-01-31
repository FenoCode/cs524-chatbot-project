import nltk

text = open("F:\CS524\cs524-chatbot-project\canvas_exercises\m1_d6_text.txt").read()

stop_words = set(nltk.corpus.stopwords.words('english'))

text_tokens = nltk.word_tokenize(text)
filtered_tokens = [word for word in text_tokens if word.lower() not in stop_words]
print("Filtered tokens:", filtered_tokens)
# stemming 
ps = nltk.PorterStemmer()
stemmed_tokens = [ps.stem(word) for word in filtered_tokens]
print("Stemmed tokens:", stemmed_tokens)
# lemmatization
lm = nltk.WordNetLemmatizer()
lemmatized_tokens = [lm.lemmatize(word) for word in stemmed_tokens]
print("Lemmatized tokens:", lemmatized_tokens)