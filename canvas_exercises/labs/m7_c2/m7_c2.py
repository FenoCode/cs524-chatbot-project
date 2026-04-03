from transformers import BartForConditionalGeneration, BartTokenizer
from rouge import Rouge

ROUGE = Rouge()

# Load the BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Sample text 
text = """Weather is the day-to-day or hour-to-hour change in the atmosphere. 
Weather includes wind, lightning, storms, hurricanes, tornadoes (also known as twisters), rain, hail, snow, and lots more. 
Energy from the Sun affects the weather too. 
Climate tells us what kinds of weather usually happen in an area at different times of the year. 
Changes in weather can affect our mood and life. We wear different clothes and do different things in different weather conditions. 
We choose different foods in different seasons.
Weather stations around the world measure different parts of weather. 
Ways to measure weather are wind speed, wind direction, temperature and humidity. 
People try to use these measurements to make weather forecasts for the future. 
These people are scientists that are called meteorologists. 
They use computers to build large mathematical models to follow weather trends."""

annotated_summary = """Weather describes short-term atmospheric conditions like wind, rain, and temperature, while climate refers to long-term patterns of weather in a region. 
Meteorologists use measurements like temperature, humidity, and wind to build computer models that predict future weather and help people plan their daily lives."""

# Tokenize and encode text and generate summary
inputs = tokenizer.encode("Generate Summary: " + text, return_tensors="pt", max_length=512, truncation=True)
summary_ids = model.generate(inputs, max_length=60, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Format annotated summary:
inputs = tokenizer.encode(annotated_summary, return_tensors="pt", max_length=512, truncation=True)
annotated_ids = model.generate(inputs, max_length=60, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
annotated_summary = tokenizer.decode(annotated_ids[0], skip_special_tokens=True)

print("Summary:")
print(summary)

print(ROUGE.get_scores(summary, annotated_summary))