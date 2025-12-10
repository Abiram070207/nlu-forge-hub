import streamlit as st, pandas as pd, os, json
import spacy
from backend.spacy_intent_model import load_intent_model, predict_textcats

st.set_page_config(page_title="Annotate", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.section-title {
    font-size: 22px;
    font-weight: 700;
}
.intent-pill {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(148,163,184,0.6);
    font-size: 11px;
    margin-right: 4px;
    margin-bottom: 4px;
}
.entity-chip {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 999px;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.4);
    font-size: 11px;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN / WORKSPACE CHECK ----------
if 'user' not in st.session_state or 'workspace' not in st.session_state:
    st.warning("Login and select workspace first.")
    st.stop()

st.markdown('<div class="section-title">✏ Annotation – Intents & Entities</div>', unsafe_allow_html=True)

ws = f"data/workspaces/{st.session_state['user']}/{st.session_state['workspace']}"
dataset_path = os.path.join(ws, "dataset.csv")
ann_path = os.path.join(ws, "annotations.json")

if not os.path.exists(dataset_path):
    st.info("Upload a dataset first on the **Upload Dataset** page.")
    st.stop()

df = pd.read_csv(dataset_path)

# ---------- LOAD / INIT ANNOTATIONS ----------
if os.path.exists(ann_path):
    with open(ann_path, "r") as f:
        annotations = json.load(f)
else:
    annotations = [
        {"sentence": row["sentence"], "intent": None, "entities": None}
        for _, row in df.iterrows()
    ]

# Make sure length matches
while len(annotations) < len(df):
    annotations.append({
        "sentence": df.iloc[len(annotations)]["sentence"],
        "intent": None,
        "entities": None
    })

# Progress
total = len(df)
done = sum(1 for a in annotations if a.get("intent"))
st.progress(done / total if total else 0.0)
st.caption(f"Annotated: {done}/{total} sentences")

st.markdown("---")

colL, colR = st.columns([2, 1])

with colL:
    idx = st.number_input("Sentence Index", min_value=0, max_value=total-1, value=0)
    idx = int(idx)
    sentence = df.iloc[idx]["sentence"]
    st.markdown(f"### 🔹 Sentence #{idx}:")
    st.info(sentence)

with colR:
    st.markdown("**Quick Navigation**")
    if st.button("⏮ Previous", use_container_width=True) and idx > 0:
        st.session_state["annot_idx"] = idx - 1
    if st.button("⏭ Next", use_container_width=True) and idx < total-1:
        st.session_state["annot_idx"] = idx + 1

# ---------- LOAD MODELS ----------
nlp_ner = spacy.load("en_core_web_sm")
intent_nlp = load_intent_model()

# Predict intent
predicted = predict_textcats(intent_nlp, sentence) if intent_nlp else None

tabs = st.tabs(["Model Suggestion", "Entities", "Annotation Form"])

with tabs[0]:
    st.subheader("Model Suggestion")
    if predicted:
        st.success(f"Suggested intent: **{predicted[0]}**")
    else:
        st.info("No trained intent model found. Train in **Train Model** page first.")

with tabs[1]:
    st.subheader("Named Entities")
    doc = nlp_ner(sentence)
    ents = [f"{e.text}->{e.label_}" for e in doc.ents]
    if ents:
        for e in ents:
            st.markdown(f"<span class='entity-chip'>{e}</span>", unsafe_allow_html=True)
    else:
        st.write("No entities detected.")

with tabs[2]:
    st.subheader("Annotation Form")

    # Define allowed intents (you can edit this)
    allowed_intents = [
        "book_flight",
        "cancel_flight",
        "check_flight_status",
        "order_food",
        "check_balance",
        "book_appointment",
        "play_music",
        "get_weather"
    ]

    prev_intent = annotations[idx].get("intent") or (predicted[0] if predicted else None)

    intent_in = st.selectbox(
        "Select / Correct Intent",
        options=[""] + allowed_intents,
        index=(allowed_intents.index(prev_intent) + 1) if prev_intent in allowed_intents else 0
    )

    entities_str = ", ".join([f"{e.text}->{e.label_}" for e in doc.ents])
    entities_in = st.text_input("Entities (editable)", value=entities_str)

    if st.button("💾 Save Annotation", type="primary"):
        annotations[idx]["sentence"] = sentence
        annotations[idx]["intent"] = intent_in if intent_in else None
        annotations[idx]["entities"] = entities_in if entities_in else None

        with open(ann_path, "w") as f:
            json.dump(annotations, f, indent=2)

        st.success(f"✅ Annotation saved for sentence #{idx}")
