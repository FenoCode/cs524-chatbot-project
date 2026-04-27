
from transformers import BartForConditionalGeneration, BartTokenizer
import torch


model_name = "facebook/bart-large-cnn"
MODEL_CONTEXT_SIZE = 512 - 12 # BART's max input length is 1024 tokens

class SummarizationInferenceService:
    def __init__(self):
        model_name = "facebook/bart-large-cnn"
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    # Adaptation from source: https://www.geeksforgeeks.org/nlp/website-summarizer-using-bart/
    def splitTextIntoChunks(self, text, chunk_size=MODEL_CONTEXT_SIZE):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=False,
            add_special_tokens=False
        )["input_ids"][0]

        chunks = []
        for i in range(0, len(inputs), chunk_size):
            chunk_ids = inputs[i:i + chunk_size]
            chunk_text = self.tokenizer.decode(chunk_ids, skip_special_tokens=True)
            chunks.append(chunk_text)

        return chunks
    
    # source: https://www.geeksforgeeks.org/nlp/website-summarizer-using-bart/
    def summarize(self, text, chunk_size=MODEL_CONTEXT_SIZE, chunk_summary_size=256):
        text = "Summarize: " + text
        chunks = self.splitTextIntoChunks(text, chunk_size)

        summaries = []
        for chunk in chunks:
            size = chunk_summary_size
            if(len(chunk) < chunk_summary_size):
                size = max(10, int(len(chunk) / 2))
            inputs = self.tokenizer.encode(chunk, return_tensors="pt").to(self.device)
            summary_ids = self.model.generate(inputs, min_length=min(30, size), max_length=size, num_beams=4, length_penalty=2.0,early_stopping=True)
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)

        return " ".join(summaries)