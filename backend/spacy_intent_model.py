import spacy, os
def load_intent_model(path='models/intent_model'):
    if os.path.exists(path):
        try:
            nlp = spacy.load(path)
            return nlp
        except Exception as e:
            print('Failed to load model:',e)
            return None
    return None

def predict_textcats(nlp, text):
    doc = nlp(text)
    if not doc.cats:
        return None
    best = max(doc.cats.items(), key=lambda x:x[1])
    return best  # (label, score)
