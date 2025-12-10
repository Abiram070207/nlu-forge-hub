import streamlit as st
import os
import pandas as pd
import json

st.set_page_config(page_title="NLU Forge Hub", layout="wide")

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
.main-header {
    font-size: 32px;
    font-weight: 800;
    padding: 0.5rem 0;
}
.sub-header {
    font-size: 16px;
    opacity: 0.85;
}
.card {
    background: linear-gradient(135deg,#1e293b,#020617);
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 12px 30px rgba(15,23,42,0.7);
    border: 1px solid rgba(148,163,184,0.4);
}
.card h3 {
    margin-bottom: 0.3rem;
}
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    background: rgba(56,189,248,0.15);
    color: #38bdf8;
    font-size: 11px;
    margin-bottom: 6px;
}
.step-pill {
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(148,163,184,0.4);
    font-size: 12px;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-header">🧠 NLU Forge Hub – Admin & Trainer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    'End-to-end workflow: dataset → annotation → model training → active learning → admin monitoring.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- QUICK STATS ACROSS WORKSPACES ----------
base_path = "data/workspaces"
total_sentences = 0
total_annotated = 0
workspace_count = 0

if os.path.exists(base_path):
    for user in os.listdir(base_path):
        user_path = os.path.join(base_path, user)
        if not os.path.isdir(user_path):
            continue
        for ws in os.listdir(user_path):
            ws_path = os.path.join(user_path, ws)
            dataset_path = os.path.join(ws_path, "dataset.csv")
            ann_path = os.path.join(ws_path, "annotations.json")
            if os.path.exists(dataset_path):
                workspace_count += 1
                df = pd.read_csv(dataset_path)
                total_sentences += len(df)
                if os.path.exists(ann_path):
                    with open(ann_path, "r") as f:
                        ann = json.load(f)
                    total_annotated += sum(1 for a in ann if a.get("intent"))

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🗂 Workspaces", workspace_count)
with col2:
    st.metric("📝 Total Sentences", total_sentences)
with col3:
    st.metric("✅ Annotated Samples", total_annotated)

progress = (total_annotated / total_sentences) if total_sentences else 0
st.progress(progress)

st.caption(f"Overall annotation progress: {progress*100:.1f} %")

st.markdown("---")

# ---------- FEATURE CARDS ----------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="badge">Step 1 & 2</div>', unsafe_allow_html=True)
    st.markdown("### 📥 Workspace & Annotation")
    st.write(
        "- Create workspace per project\n"
        "- Upload domain datasets\n"
        "- Annotate intents & entities\n"
        "- Use model suggestions to speed up"
    )
    st.markdown(
        '<span class="step-pill">1️⃣ Login</span>'
        '<span class="step-pill">2️⃣ Workspace</span>'
        '<span class="step-pill">3️⃣ Upload</span>'
        '<span class="step-pill">4️⃣ Annotate</span>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="badge">Step 3</div>', unsafe_allow_html=True)
    st.markdown("### 🧠 Model Training & Evaluation")
    st.write(
        "- Train spaCy intent model from annotations\n"
        "- Track loss across epochs\n"
        "- Evaluate with accuracy & confusion matrix\n"
        "- Save reusable model under /models"
    )
    st.markdown(
        '<span class="step-pill">5️⃣ Train Model</span>'
        '<span class="step-pill">6️⃣ Test & Evaluate</span>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="badge">Step 4</div>', unsafe_allow_html=True)
    st.markdown("### 🔁 Active Learning & Admin")
    st.write(
        "- Filter low-confidence samples\n"
        "- Review & correct noisy labels\n"
        "- Admin view for monitoring workspaces\n"
        "- Retrain models from dashboard"
    )
    st.markdown(
        '<span class="step-pill">7️⃣ Active Learning</span>'
        '<span class="step-pill">8️⃣ Admin Dashboard</span>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.info(
    "Use the left sidebar to open individual modules: "
    "**Login, Workspace, Upload Dataset, Annotate, Train Model, Test/Evaluate, Active Learning, Admin Dashboard**."
)
