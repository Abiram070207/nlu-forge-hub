from sklearn.model_selection import train_test_split
import spacy, random, os
from spacy.training.example import Example
import matplotlib.pyplot as plt

def prepare_spacy_training(dataframe):
    texts = dataframe['sentence'].tolist()
    labels = dataframe['intent'].tolist()
    cats = []
    unique_labels = sorted(list(set(labels)))
    for l in labels:
        cat = {lab: 1.0 if lab == l else 0.0 for lab in unique_labels}
        cats.append(cat)
    return list(zip(texts, [{'cats': c} for c in cats]))

def train_and_save_spacy_textcat(annotations_json_path, model_out_dir='models/intent_model', epochs=8):
    import pandas as pd
    df = pd.read_json(annotations_json_path).dropna(subset=['sentence','intent'])
    if df.empty:
        return 'No data'

    train_data = prepare_spacy_training(df)
    random.shuffle(train_data)

    # SAFE SPLIT FIX → works even with 1 or 2 samples
    if len(train_data) < 3:
        train = train_data
        dev = []
    else:
        train, dev = train_test_split(train_data, test_size=0.2, random_state=42)

    labels = sorted(set(df['intent'].tolist()))

    nlp = spacy.blank('en')
    textcat = nlp.add_pipe('textcat', last=True)

    for lab in labels:
        textcat.add_label(lab)

    optimizer = nlp.initialize()
    losses = []

    for ep in range(epochs):
        random.shuffle(train)
        batch_loss = {}
        for text, ann in train:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, ann)
            nlp.update([example], sgd=optimizer, losses=batch_loss)
        losses.append(batch_loss.get('textcat', 0))

    os.makedirs(model_out_dir, exist_ok=True)
    nlp.to_disk(model_out_dir)

    return {'model_dir': model_out_dir, 'epochs': epochs}
