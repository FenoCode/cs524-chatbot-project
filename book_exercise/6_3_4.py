import numpy as np
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import evaluate

# note: this script is nothing like the book. The book's script uses depreciated libraries. Like keras 2 or something.

# sample corpus
corpus = [
    "I love this product! It's amazing.",
    "This is the worst service I have ever experienced.",
    "I am very happy with my purchase.",
    "I am disappointed with the quality of this item.",
    "This item saved my party",
    "My event was ruined by this product"
]

labels = [1,0,1,0,1,0]

# train/test split
train_texts, test_texts, train_labels, test_labels = train_test_split(
    corpus, labels, test_size=0.25, random_state=42
)

# convert to HuggingFace dataset
train_dataset = Dataset.from_dict({"text": train_texts, "label": train_labels})
test_dataset = Dataset.from_dict({"text": test_texts, "label": test_labels})

# tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(example):
    return tokenizer(example["text"], padding="max_length", truncation=True)

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

train_dataset.set_format(type="torch", columns=["input_ids","attention_mask","label"])
test_dataset.set_format(type="torch", columns=["input_ids","attention_mask","label"])

# load model
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# evaluation metric
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    return accuracy.compute(predictions=preds, references=labels)

# training config
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_dir="./logs"
)

# trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
)

# train
trainer.train()

# evaluate
trainer.evaluate()



text = "This product is excellent and I love it"

inputs = tokenizer(text, return_tensors="pt")

outputs = model(**inputs)

prediction = np.argmax(outputs.logits.detach().numpy())

print("Prediction:", "Positive" if prediction == 1 else "Negative")