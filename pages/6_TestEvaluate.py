import streamlit as st, os
from backend.evaluator import evaluate_model_on_annotations

st.set_page_config(page_title="Test & Evaluate", layout="wide")
if 'user' not in st.session_state or 'workspace' not in st.session_state:
    st.warning("Login and select workspace first.")
else:
    st.title("Test & Evaluate Model")
    ws = f"data/workspaces/{st.session_state['user']}/{st.session_state['workspace']}"
    ann_path = os.path.join(ws, 'annotations.json')
    model_dir = 'models/intent_model'
    if not os.path.exists(ann_path):
        st.info('No annotations available.')
    else:
        if st.button('Run Evaluation'):
            with st.spinner('Evaluating...'):
                report, cm_path = evaluate_model_on_annotations(ann_path, model_dir)
                st.subheader('Classification Report')
                st.text(report)
                if cm_path:
                    st.image(cm_path, caption='Confusion Matrix')
