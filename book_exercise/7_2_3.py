from gensim import corpora
from gensim.models import LdaModel
from gensim.models import CoherenceModel
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

def main():
    stop_words = stopwords.words('english')
    
    corpus = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m6_c5\m6_c5.txt', 'r').read()

    # sample text corpus
    corpus = sent_tokenize(corpus)

    # Tokenize, remove stop words, create dictionary representation of documents, and create BoW
    texts = [[word for word in document.lower().split() if word not in stop_words] for document in corpus];
    dictionary = corpora.Dictionary(texts)
    corpus_bow = [dictionary.doc2bow(text) for text in texts]

    # Train LDA model and print topics 
    lda_model = LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=5, random_state=42, passes=10)

    # Print topics
    print("Topics:")
    pprint(lda_model.print_topics(num_words=10))

    # Assign topics to new document
    new_doc = "What is the dog doing?"
    new_doc_bow = dictionary.doc2bow([word for word in new_doc.lower().split() if word not in stop_words])
    print("\nTopic Distribution for the new document:")
    pprint(lda_model.get_document_topics(new_doc_bow))

    # Perform coherency model testing for LDA model
    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print(f"Coherence Score: {coherence_lda}")

if __name__ == "__main__":
    # HOTFIX: Had to wrap script in main function when including the CoherenceModel library due to infinite thread spawning of main module
    # https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing
	main()