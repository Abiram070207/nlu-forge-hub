import streamlit as st
import os, json, pandas as pd
from backend.spacy_intent_model import load_intent_model
from backend.trainer import train_and_save_spacy_textcat
from backend.evaluator import evaluate_model_on_annotations

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠 Admin Dashboard – NLU Forge Hub")

BASE_PATH = "data/workspaces/"

# -----------------------------
# 1. SELECT USER & WORKSPACE
# -----------------------------
if not os.path.exists(BASE_PATH):
    st.error("No workspaces found yet.")
    st.stop()

users = os.listdir(BASE_PATH)
if not users:
    st.error("No user folders found in data/workspaces/")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    user = st.selectbox("Select User", users)

workspaces = os.listdir(os.path.join(BASE_PATH, user))
with col2:
    workspace = st.selectbox("Select Workspace", workspaces)

if not workspace:
    st.stop()

ws_path = os.path.join(BASE_PATH, user, workspace)
dataset_path = os.path.join(ws_path, "dataset.csv")
ann_path = os.path.join(ws_path, "annotations.json")
model_dir = "models/intent_model"

st.markdown(f"**Active Workspace:** `{user} / {workspace}`")

# -----------------------------
# 2. BASIC STATS (DATA LAYER)
# -----------------------------
colA, colB, colC = st.columns(3)

# Dataset stats
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)
    num_samples = len(df)
else:
    df = None
    num_samples = 0

with colA:
    st.metric("Total Sentences in Dataset", num_samples)

# Annotation stats
if os.path.exists(ann_path):
    with open(ann_path, "r") as f:
        annotations = json.load(f)
    num_annotated = sum(1 for a in annotations if a.get("intent"))
    num_unlabeled = num_samples - num_annotated
else:
    annotations = []
    num_annotated = 0
    num_unlabeled = num_samples

with colB:
    st.metric("Annotated Sentences", num_annotated)
with colC:
    st.metric("Unlabeled Sentences", max(num_unlabeled, 0))

# -----------------------------
# 3. MODEL STATUS (BACKEND CALL)
# -----------------------------
st.markdown("---")
st.subheader("📦 Model Status")

nlp_model = load_intent_model(model_dir)
model_exists = nlp_model is not None

colM1, colM2 = st.columns(2)

with colM1:
    st.write("Model Directory:", model_dir)
    st.write("Loaded:", "✅ Yes" if model_exists else "❌ No")

if len(annotations) == 0:
    st.info("No annotations available yet. Go to Annotate page first.")
else:
    # Show available intent labels
    intents = sorted(list(set(a["intent"] for a in annotations if a.get("intent"))))
    with colM2:
        st.write("Detected Intent Labels:", intents if intents else "None")

# -----------------------------
# 4. ADMIN ACTIONS – TRAIN & EVALUATE
# -----------------------------
st.markdown("---")
st.subheader("⚙ Admin Actions")

colT1, colT2 = st.columns(2)

with colT1:
    epochs = st.number_input("Training Epochs", min_value=1, max_value=30, value=8)
    if st.button("🔁 Retrain Model from Annotations"):
        if not os.path.exists(ann_path):
            st.error("No annotations.json found for this workspace.")
        else:
            with st.spinner("Training spaCy TextCat model..."):
                result = train_and_save_spacy_textcat(ann_path, model_out_dir=model_dir, epochs=epochs)
            st.success("Model retrained successfully.")
            st.json(result)

with colT2:
    if st.button("📊 Evaluate Current Model"):
        if not os.path.exists(ann_path):
            st.error("No annotations found for evaluation.")
        elif not os.path.exists(model_dir):
            st.error("Model directory not found. Train the model first.")
        else:
            with st.spinner("Evaluating model on annotations..."):
                report, cm_path = evaluate_model_on_annotations(ann_path, model_dir=model_dir)
            st.subheader("Classification Report")
            st.text(report)
            if cm_path and os.path.exists(cm_path):
                st.image(cm_path, caption="Confusion Matrix")

# -----------------------------
# 5. OPTIONAL: QUICK PREVIEW
# -----------------------------
st.markdown("---")
st.subheader("📄 Quick Dataset Preview")

if df is not None:
    st.dataframe(df.head(10), use_container_width=True)
else:
    st.info("No dataset loaded for this workspace.")
