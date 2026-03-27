import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from pprint import pprint
from gensim import corpora
from gensim.models import HdpModel

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')    
nltk.download('omw-1.4') 
nltk.download('averaged_perceptron_tagger_eng') 


stop_words = stopwords.words('english')
le = WordNetLemmatizer()

# Tokenize, remove stop words, lemmatize, create dictionary representation of documents, create BoW
corpus = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m6_d4\m6_c4.txt', 'r').read()
corpus_sent = sent_tokenize(corpus)
corpus_sent = [[word for word in word_tokenize(sent) if word.lower() not in stop_words] for sent in corpus_sent]
corpus_sent = [[word for word in sent if not all(char in string.punctuation for char in word)] for sent in corpus_sent]

corpus_sent = [[le.lemmatize(word) for word in sent]for sent in corpus_sent]
corpus_dict = corpora.Dictionary(corpus_sent)
corpus_bow = [corpus_dict.doc2bow(sent) for sent in corpus_sent]
hdp_model = HdpModel(corpus=corpus_bow, id2word=corpus_dict, random_state=42)

print("Topics:")
print(hdp_model.print_topics(num_topics=3, num_words=5))