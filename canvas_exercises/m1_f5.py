import nltk

text = open("F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\m1_f5_text.txt").read()
sentence_tokens = nltk.sent_tokenize(text)
sentence_breakdown = []
for sentence in sentence_tokens:
    sentence_breakdown.append(nltk.word_tokenize(sentence))

# subword tokenization
subword_tokens = []
for sentence in sentence_breakdown:
    for word in sentence:
        subword_tokens= nltk.word_tokenize(word)
        if (len(subword_tokens) > 1):
            print("Subword tokens:", subword_tokens)
