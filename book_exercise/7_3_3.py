import gensim
from nltk.corpus import stopwords
from gensim import corpora
from gensim.models import HdpModel
from gensim.models import CoherenceModel
from pprint import pprint

def main():
    stop_words = stopwords.words('english')

    # sample text corpus
    corpus = [
        "The cat sat on the mat.",
        "The dog sat on the log",
        "The cat chased the dog",
        "The dog chased the cat"
    ]

        # Tokenize, remove stop words, create dictionary representation of documents, and create BoW
    texts = [[word for word in document.lower().split() if word not in stop_words] for document in corpus];
    dictionary = corpora.Dictionary(texts)
    print(texts)
    corpus_bow = [dictionary.doc2bow(text) for text in texts]

    # Train LDA model and print topics 
    hdp_model = HdpModel(corpus=corpus_bow, id2word=dictionary)
    print("Topcis:")
    print(hdp_model.print_topics(num_topics=2, num_words=5))
    
    # Assign topics to new document
    new_doc = "What is the dog doing?"
    new_doc_bow = dictionary.doc2bow([word for word in new_doc.lower().split() if word not in stop_words])
    print("\nTopic Distribution for the new document:")
    pprint(hdp_model[new_doc_bow])
    
    # Perform coherency model testing for LDA model
    coherence_model_lda = CoherenceModel(model=hdp_model, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print(f"Coherence Score: {coherence_lda}")


if __name__ == "__main__":
    # HOTFIX: Had to wrap script in main function when including the CoherenceModel library due to infinite thread spawning of main module
    # https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing
	main()