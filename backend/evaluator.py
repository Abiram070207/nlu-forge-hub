import os, pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns, matplotlib.pyplot as plt
from backend.spacy_intent_model import load_intent_model

def evaluate_model_on_annotations(annotations_path, model_dir='models/intent_model'):
    df = pd.read_json(annotations_path)
    df = df.dropna(subset=['sentence','intent'])
    if df.empty:
        return 'No data', None
    nlp = load_intent_model(model_dir)
    if not nlp:
        return 'Model not found', None
    y_true = df['intent'].tolist()
    y_pred = []
    for t in df['sentence'].tolist():
        doc = nlp(t)
        # choose best label
        if doc.cats:
            lbl = max(doc.cats.items(), key=lambda x:x[1])[0]
        else:
            lbl = ''
        y_pred.append(lbl)
    report = classification_report(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=sorted(list(set(y_true+ y_pred))))
    out_dir = os.path.join(model_dir)
    os.makedirs(out_dir, exist_ok=True)
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    cm_path = os.path.join(out_dir, 'confusion_matrix.png')
    plt.savefig(cm_path)
    return report, cm_path
