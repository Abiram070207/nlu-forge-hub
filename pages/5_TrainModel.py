import streamlit as st, os, json
from backend.trainer import train_and_save_spacy_textcat

st.set_page_config(page_title="Train Model", layout="wide")
if 'user' not in st.session_state or 'workspace' not in st.session_state:
    st.warning("Login and select workspace first.")
else:
    st.title("Train spaCy Intent Model")
    ws = f"data/workspaces/{st.session_state['user']}/{st.session_state['workspace']}"
    ann_path = os.path.join(ws, 'annotations.json')
    if not os.path.exists(ann_path):
        st.info('No annotations found. Annotate some data first.')
    else:
        epochs = st.number_input('Epochs', min_value=1, max_value=50, value=8)
        if st.button('Start Training'):
            with st.spinner('Training...'):
                out = train_and_save_spacy_textcat(ann_path, epochs=epochs)
                st.success('Training completed. Model saved.')
                st.write(out)
