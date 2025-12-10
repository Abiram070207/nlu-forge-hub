import json, pandas as pd
def load_annotations(path):
    df = pd.read_json(path)
    # ensure columns sentence and intent exist
    if 'sentence' not in df.columns or 'intent' not in df.columns:
        raise ValueError('annotations.json must contain sentence and intent fields')
    return df[['sentence','intent']].dropna()
