import spacy
from spacy.tokens import DocBin
from spacy.training.example import Example
import pandas as pd
import os, shutil

ANNOT_PATH = "data/annotated/sample_annotations.json"
OUT_DIR = "models/intent_model"

print("Loading annotations...")
df = pd.read_json(ANNOT_PATH)

texts = df["sentence"].tolist()
labels = df["intent"].tolist()
unique_labels = sorted(list(set(labels)))

print("Labels:", unique_labels)

# Create blank model
nlp = spacy.blank("en")
textcat = nlp.add_pipe("textcat")

for label in unique_labels:
    textcat.add_label(label)

# Prepare training data
train_examples = []
for text, label in zip(texts, labels):
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, {"cats": {l: 1.0 if l == label else 0.0 for l in unique_labels}})
    train_examples.append(example)

# Train
optimizer = nlp.initialize()
print("Training model...")

for i in range(25):
    losses = {}
    nlp.update(train_examples, sgd=optimizer, losses=losses)
    print(f"Epoch {i+1} Losses:", losses)

# Save model
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
    
os.makedirs(OUT_DIR, exist_ok=True)

nlp.to_disk(OUT_DIR)

print("Model saved to:", OUT_DIR)
