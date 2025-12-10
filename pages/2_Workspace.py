import streamlit as st, os

st.set_page_config(page_title="Workspaces", layout="wide")
if 'user' not in st.session_state:
    st.warning("Please login first (go to Login page).")
else:
    user = st.session_state['user']
    st.title(f"Workspaces — {user}")
    base = f"data/workspaces/{user}"
    os.makedirs(base, exist_ok=True)
    existing = os.listdir(base)
    if existing:
        st.subheader("Existing Workspaces")
        for w in existing:
            if st.button(f"Open: {w}"):
                st.session_state['workspace'] = w
                st.success(f"Workspace set to {w}. Open Upload Dataset page.")
    new = st.text_input("New workspace name")
    if st.button("Create Workspace"):
        if new:
            os.makedirs(os.path.join(base,new), exist_ok=True)
            st.success("Workspace created.")
        else:
            st.error("Enter a valid name")
