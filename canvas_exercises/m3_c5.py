from nltk import pos_tag
from nltk import word_tokenize, sent_tokenize
text = open("F:\CS524\cs524-chatbot-project\canvas_exercises\m3_c5.txt", "r").read()
sentences = sent_tokenize(text)

for sentence in sentences:
    tokens = word_tokenize(sentence)
    tagged_tokens = pos_tag(tokens)
    print(tagged_tokens)