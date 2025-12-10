import streamlit as st, pandas as pd, os, json

st.set_page_config(page_title="Upload Dataset", layout="wide")
if 'user' not in st.session_state or 'workspace' not in st.session_state:
    st.warning("Login and select workspace first.")
else:
    st.title("Upload Dataset")
    uploaded = st.file_uploader("Upload .txt or .csv", type=['txt','csv'])
    if uploaded is not None:
        if uploaded.name.endswith('.txt'):
            text = uploaded.read().decode('utf-8').splitlines()
            df = pd.DataFrame([{'sentence':t} for t in text if t.strip()])
        else:
            df = pd.read_csv(uploaded)
        st.dataframe(df)
        save = st.button("Save dataset to workspace")
        if save:
            ws = f"data/workspaces/{st.session_state['user']}/{st.session_state['workspace']}/"
            os.makedirs(ws, exist_ok=True)
            path = os.path.join(ws, "dataset.csv")
            df.to_csv(path, index=False)
            st.success(f"Saved to {path}")
