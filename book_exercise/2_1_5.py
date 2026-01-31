import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

text = "Natural Language Processing (NLP) is a fascinating field of study that focuses on the interaction between computers and human language. It involves the development of algorithms and models that enable machines to understand, interpret, and generate human language in a way that is meaningful and useful."

# Lowercase text, remove punctuation, and split into words
text_tokens = text.lower().translate(str.maketrans('','', string.punctuation)).split()
print("Processed text:", text_tokens)
print('Token count:', len(text_tokens))

print("\n Stop Words Removal \n")

# removes stop words
stop_words = set(stopwords.words('english'))
text_tokens = [word for word in text_tokens if word not in stop_words]
print("Processed text:", text_tokens)
print('Token count:', len(text_tokens))

print("\n Stemming Process \n")
# Stemming process of tokens
ps = PorterStemmer()
stemmed_tokens = [ps.stem(word) for word in text_tokens]
print("Stemmed tokens:", stemmed_tokens)
print('Token count:', len(stemmed_tokens))

print("\n Lemmatization Process \n")
# Lemmatization process of tokens
lm = WordNetLemmatizer()
lemmatized_tokens = [lm.lemmatize(word) for word in text_tokens]
print("Lemmatized tokens:", lemmatized_tokens)
print('Token count:', len(lemmatized_tokens))
