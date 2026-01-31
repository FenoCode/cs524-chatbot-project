from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

text = """
M1.B1 Introduction to Natural Language Processing (NLP)
 INTRODUCTION TO NATURAL LANGUAGE PROCESSING (NLP)
NLP is a subfield of AI focused on teaching computers to understand, interpret, and produce human language (Hagiwara, 2021).

NLP aims to close the gap between human communication and machine processing, allowing computers to comprehend and respond to natural language in a meaningful and contextually appropriate manner.

By analyzing and interpreting text or speech, NLP algorithms and techniques enable computers to extract information, understand emotions, generate responses, and even translate languages. From virtual assistants and chatbots to search engines and data analytics, NLP plays a vital role in enhancing human–computer interaction and transforming various industries.

To understand NLP, it is important to differentiate it from other related fields. You might be familiar with artificial intelligence (AI) and machine learning (ML). You may also have heard of deep learning (DL), which is currently gaining attention in the media. This diagram demonstrates the overlap between these fields.
"""
parser = PlaintextParser.from_string(text, Tokenizer("english"))
summarizer = LsaSummarizer()

summary = summarizer(parser.document, 2)
for sentence in summary:
    print(sentence)