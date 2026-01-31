import nltk
import re

text = open("F:\CS524\cs524-chatbot-project\canvas_exercises\m1_f4_text.txt").read()
text_tokens = nltk.word_tokenize(text)
text_labels = nltk.pos_tag(text_tokens)

words_ly = [word for word in text_tokens if re.search(r'ly$', word)]
print("Words with ly:", len(words_ly))
# Extract adverbs
adverbs = [word for word, pos in text_labels if pos == 'RB' or pos == 'RBR' or pos == 'RBS']
# Filter adverbs ending with 'ly'
adverbs_ly = [word for word in adverbs if re.search(r'ly$', word)]
print("Adverbs with ly:", adverbs_ly)
print("Adverb count:", len(adverbs_ly))
print("Unique adverb count:", len(set(adverbs_ly)))