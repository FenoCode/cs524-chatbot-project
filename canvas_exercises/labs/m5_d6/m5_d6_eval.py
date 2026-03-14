import json
from keras.layers import TextVectorization
from keras.models import load_model
from nltk import sent_tokenize

# Load config and recreate the layer
with open("text_vectorization_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open('vocabulary.json', 'r') as f:
    vocab = json.load(f )

t_loaded = TextVectorization.from_config(config)
t_loaded.set_vocabulary(vocab)

# Now the layer can transform raw strings
text = open('F:\CS524\cs524-chatbot-project-refresh\cs524-chatbot-project\canvas_exercises\labs\m5_d6\m5_d6.txt').read()
text_sent = sent_tokenize(text)

model = load_model('sentiment_model.keras')
# Transform the new texts using the loaded TextVectorization layer
new_data = t_loaded(text_sent)
# Make predictions with the loaded model
predictions = model.predict(new_data)
# Print the predictions
for text, pred in zip(text_sent, predictions):
    sentiment = "positive" if pred[0] > 0.5 else "negative"
    print(f"Text: {text}\nPredicted Sentiment: {sentiment}\n")