NLU_Forge - Full Project (Modular)
---------------------------------
This project contains a modular Streamlit frontend and backend modules using spaCy for both NER and Intent Classification (TextCategorizer).
Folders:
  - pages/: Streamlit multipage files
  - backend/: spaCy training, evaluation, utils
  - models/intent_model: saved spaCy model will be stored here after training
  - data/: uploaded datasets and annotations

Quick start:
  - pip install -r requirements.txt
  - python -m spacy download en_core_web_sm
  - python -m streamlit run app.py
