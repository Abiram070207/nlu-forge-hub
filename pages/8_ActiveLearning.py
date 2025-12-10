import streamlit as st
import os, json, pandas as pd
import spacy
from backend.spacy_intent_model import load_intent_model, predict_textcats

st.set_page_config(page_title="Active Learning", layout="wide")
st.title("🤖 Active Learning – Improve Low Confidence Samples")

# -----------------------------------
# 1. SELECT WORKSPACE
# -----------------------------------
base_path = "data/workspaces/"
users = os.listdir(base_path)
user = st.selectbox("Select User", users)

if user:
    workspaces = os.listdir(os.path.join(base_path, user))
    workspace = st.selectbox("Select Workspace", workspaces)

if not user or not workspace:
    st.stop()

# Paths
ws_path = os.path.join(base_path, user, workspace)
dataset_path = os.path.join(ws_path, "dataset.csv")
ann_path = os.path.join(ws_path, "annotations.json")

# -----------------------------------
# 2. LOAD DATA
# -----------------------------------
if not os.path.exists(dataset_path):
    st.error("No dataset found! Upload dataset first.")
    st.stop()

df = pd.read_csv(dataset_path)
st.subheader("📘 Dataset Preview:")
st.dataframe(df.head(5), use_container_width=True)

if os.path.exists(ann_path):
    with open(ann_path, "r") as f:
        annotations = json.load(f)
else:
    annotations = [{"sentence": row["sentence"], "intent": None, "entities": None} 
                    for _, row in df.iterrows()]

# Load model
intent_nlp = load_intent_model()
nlp_ner = spacy.load("en_core_web_sm")

if not intent_nlp:
    st.error("Model NOT found! Go to Train Model page first.")
    st.stop()

# -----------------------------------
# 3. PREDICT CONFIDENCE FOR ALL SENTENCES
# -----------------------------------
low_conf_samples = []

for i, row in enumerate(df["sentence"]):
    pred = predict_textcats(intent_nlp, row)

    if pred:     # pred = ['intent_name', score]
        intent, score = pred
        if score < 0.60:   # <-- CHANGE THRESHOLD (0.50 or 0.60)
            low_conf_samples.append((i, row, intent, score))

# -----------------------------------
# 4. SHOW LOW-CONFIDENCE SENTENCES
# -----------------------------------
if not low_conf_samples:
    st.success("🎉 All predictions above confidence threshold!")
    st.stop()

st.warning(f"⚠ Found {len(low_conf_samples)} low-confidence samples")

# Select sentence
idx = st.selectbox("Choose sentence to review:", [x[0] for x in low_conf_samples])
row = df.iloc[idx]["sentence"]

st.markdown(f"### ✏ Sentence: **{row}**")

predicted = predict_textcats(intent_nlp, row)
if predicted:
    st.info(f"Predicted Intent: **{predicted[0]}**")
    st.write(f"Confidence: {predicted[1]:.2f}")

doc = nlp_ner(row)
entities = ", ".join([f"{e.text}->{e.label_}" for e in doc.ents]) or "None"

st.write("Extracted Entities:", entities)

# -------------------------
# MANUAL CORRECTION
# -------------------------
intent_in = st.text_input("Correct/Set Intent", value=(predicted[0] if predicted else ""))
entities_in = st.text_input("Edit Entities", value=entities)

if st.button("💾 Save Update"):
    annotations[idx]["intent"] = intent_in
    annotations[idx]["entities"] = entities_in

    with open(ann_path, "w") as f:
        json.dump(annotations, f, indent=2)

    st.success(f"Updated index {idx} successfully.")
    st.experimental_rerun()

