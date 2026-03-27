import re
import nltk
from pprint import pprint
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF, TruncatedSVD
from gensim.models import HdpModel, LdaModel
from gensim import corpora

NUM_TOPICS = 10
NUM_WORDS = 10
NUM_PASSES = 40
RANDOM_STATE = 42

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')    
nltk.download('omw-1.4') 
nltk.download('averaged_perceptron_tagger_eng') 


stop_words = stopwords.words('english')
le = WordNetLemmatizer()

# clean corpus text
def clean_corpus(corpus):
    # Implement text cleaning steps such as lowercasing, removing punctuation, etc.
    cleaned_corpus = []
    for doc in corpus:
        cleaned_doc = doc.lower()  # Convert to lowercase
        cleaned_doc = ''.join(char for char in cleaned_doc if char.isalnum() or char.isspace())  # Remove punctuation
        cleaned_doc =  re.sub(r'https?://\S+', '', cleaned_doc) # remove links
        cleaned_corpus.append(cleaned_doc)
    return cleaned_corpus

def generate_lsa_topics(corpus, num_topics=2):
    print("==== Generating LSA Topics ====")
    # Create feature and train model
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    lsa = TruncatedSVD(n_components=num_topics, random_state=RANDOM_STATE)
    X_reduced = lsa.fit_transform(X)

    # Print terms and their corresponding components
    terms = vectorizer.get_feature_names_out()
    print("==== Finished Generation of LSA Topics ====")
    return terms, lsa.components_


def generate_lda_topics(corpus, num_topics=2, num_words=10, num_passes=10):
    dictionary = corpora.Dictionary(corpus)
    corpus_bow = [dictionary.doc2bow(text) for text in corpus]

    # Train LDA model and print topics 
    lda_model = LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=num_topics, passes=num_passes, random_state=RANDOM_STATE)

    return lda_model.print_topics(num_topics=num_topics, num_words=num_words)

def generate_hdp_topics(corpus, num_topics=2, num_words=10):
    dictionary = corpora.Dictionary(corpus)
    corpus_bow = [dictionary.doc2bow(text) for text in corpus]

    # Train LDA model and print topics 
    hdp_model = HdpModel(corpus=corpus_bow, id2word=dictionary, random_state=RANDOM_STATE)

    return hdp_model.print_topics(num_topics=num_topics, num_words=num_words)

def generate_nmf_topics(corpus, num_topics=2, num_words=10):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    nmf = NMF(n_components=num_topics, random_state=RANDOM_STATE)
    W = nmf.fit_transform(X)
    H = nmf.components_

    terms = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(H):
        top_terms_idx = topic.argsort()[:-num_words - 1:-1]
        top_terms = [terms[i] for i in top_terms_idx]
        topics.append((topic_idx, top_terms))
    
    return topics

# Retrieve corpus
corpus = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\dataset\chatbot_corpus.txt', 'r', encoding='utf-8').read()
# Parse sentences, normalize text, lemmatize, and remove stop words
corpus_sent = sent_tokenize(corpus)
corpus_sent = clean_corpus(corpus_sent)
corpus_sent = [[le.lemmatize(word.lower()) for word in word_tokenize(sent)] for sent in corpus_sent]
corpus_sent = [[word for word in sent if word not in stop_words] for sent in corpus_sent]
corpus_sent = [ ' '.join(word for word in sent) for sent in corpus_sent] # List[List[str]] -> List[str]

# LSA Model topics and output
print("LSA Topics:")
lsa_terms, lsa_components = generate_lsa_topics(corpus_sent, num_topics=NUM_TOPICS)
for i, comp in enumerate(lsa_components):
    terms_comp = zip(lsa_terms, comp)
    sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:NUM_WORDS]
    print(f"Topic {i}:")
    for term, weight in sorted_terms:
        print(f" - {term} : {weight:.4f}")

# LDA Model topics and ouptut
corpus_sent = [sent.split(' ') for sent in corpus_sent] #  List[str] -> List[List[str]]
lda_topics = generate_lda_topics(corpus_sent, num_topics=NUM_TOPICS, num_passes=NUM_PASSES)
print("LDA Topics:")
pprint(lda_topics)

# HDP Model topics and output
hdp_topics = generate_hdp_topics(corpus_sent, num_topics=NUM_TOPICS)
print("HDP Topics:")
pprint(hdp_topics)

# NMF Model topics and output
corpus_sent = [ ' '.join(word for word in sent) for sent in corpus_sent] # List[List[str]] -> List[str]
nmf_topics = generate_nmf_topics(corpus_sent, num_topics=NUM_TOPICS)
print("NMF Topics:")
pprint(nmf_topics)


# SECTION: Topic normalization and comparison across models

def extract_terms_from_lda_string(topic_str):
    # Extract words from "0.013*word + ..." format
    return [term.split('*')[1].replace('"', '').strip()
            for term in topic_str.split('+')]

def normalize_lsa(terms, components, num_words):
    norm_topics = []
    for comp in components:
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:num_words]
        norm_topics.append([term for term, _ in sorted_terms])
    return norm_topics

def normalize_lda(lda_topics):
    return [extract_terms_from_lda_string(topic[1]) for topic in lda_topics]

def normalize_hdp(hdp_topics):
    return [extract_terms_from_lda_string(topic[1]) for topic in hdp_topics]

def normalize_nmf(nmf_topics):
    return [topic[1] for topic in nmf_topics]

def jaccard_similarity(topic1, topic2):
    set1, set2 = set(topic1), set(topic2)
    return len(set1 & set2) / len(set1 | set2)

def compare_models(model_topics_dict):
    model_names = list(model_topics_dict.keys())

    print("\n" + "="*60)
    print("MODEL TOPIC OVERLAP MATRIX (Jaccard Similarity)")
    print("="*60)

    for m1 in model_names:
        for m2 in model_names:
            if m1 == m2:
                continue

            scores = []
            for t1 in model_topics_dict[m1]:
                best = max([jaccard_similarity(t1, t2) for t2 in model_topics_dict[m2]])
                scores.append(best)

            avg_score = sum(scores) / len(scores)
            print(f"{m1} vs {m2}: {avg_score:.3f}")

    print("="*60)

def print_aligned_topics(model_topics_dict, num_topics=2):
    print("\n" + "="*60)
    print("TOPIC ALIGNMENT VIEW (Top Matches Across Models)")
    print("="*60)

    base_model = list(model_topics_dict.keys())[0]

    for i, base_topic in enumerate(model_topics_dict[base_model][:num_topics]):
        print(f"\n- {base_model} Topic {i}: {base_topic}")

        for model_name, topics in model_topics_dict.items():
            if model_name == base_model:
                continue

            best_match = max(topics, key=lambda t: jaccard_similarity(base_topic, t))
            score = jaccard_similarity(base_topic, best_match)

            print(f"   -> {model_name} (score={score:.2f}): {best_match}")


lsa_norm = normalize_lsa(lsa_terms, lsa_components, NUM_WORDS)
lda_norm = normalize_lda(lda_topics)
hdp_norm = normalize_hdp(hdp_topics)
nmf_norm = normalize_nmf(nmf_topics)

model_topics = {
    "LSA": lsa_norm,
    "LDA": lda_norm,
    "HDP": hdp_norm,
    "NMF": nmf_norm
}

# Run comparison and output results
compare_models(model_topics)
print_aligned_topics(model_topics, num_topics=NUM_TOPICS)