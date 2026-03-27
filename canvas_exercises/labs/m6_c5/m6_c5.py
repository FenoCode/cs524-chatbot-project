import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.models import LdaModel
from gensim import corpora
from nltk.stem import WordNetLemmatizer
from pprint import pprint
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')    
nltk.download('omw-1.4') 
nltk.download('averaged_perceptron_tagger_eng') 


stop_words = stopwords.words('english')
le = WordNetLemmatizer()

# Tokenize, remove stop words, lemmatize, create dictionary representation of documents, create BoW
corpus = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m6_c5\m6_c5.txt', 'r').read()
corpus_sent = sent_tokenize(corpus)
corpus_sent = [[word for word in word_tokenize(sent) if word.lower() not in stop_words] for sent in corpus_sent]
corpus_sent = [[word for word in sent if not all(char in string.punctuation for char in word)] for sent in corpus_sent]

corpus_sent = [[le.lemmatize(word) for word in sent]for sent in corpus_sent]
corpus_dict = corpora.Dictionary(corpus_sent)
corpus_bow = [corpus_dict.doc2bow(sent) for sent in corpus_sent]
lda_model = LdaModel(corpus=corpus_bow, id2word=corpus_dict, num_topics=2, passes=50, random_state=42)

# Print topics
print("Topics:")
pprint(lda_model.print_topics(num_words=10))