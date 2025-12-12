# 🔥 NLU Model Trainer and Evaluator for Chatbots
### A Complete Intent Classification & Entity Extraction System (Built with Streamlit + spaCy)

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![spaCy](https://img.shields.io/badge/NLP-spaCy-09A3D5?logo=spacy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![GitHub Repo Size](https://img.shields.io/github/repo-size/Abiram070207/nlu-forge-hub)
![Last Commit](https://img.shields.io/github/last-commit/Abiram070207/nlu-forge-hub)

---

## 📌 **Project Overview**

NLU Forge Hub is a modular Natural Language Understanding (NLU) system designed for:
- **Intent Classification**
- **Entity Recognition**
- **Dataset Annotation**
- **Model Training**
- **Active Learning**
- **Admin Dashboard Monitoring**

The platform provides a **complete workflow** starting from dataset upload → annotation → spaCy model training → evaluation → active learning loop → admin analytics.

This project demonstrates a production-style NLU pipeline suitable for conversational agents, chatbots, customer service AI, and task automation systems.

---

## 🚀 **Key Features**

### ✅ **1. User Authentication**
Secure login system with user workspace isolation.

### ✅ **2. Workspace Management**
Each user can create multiple workspaces for different NLU projects.

### ✅ **3. Dataset Upload Module**
Supports:
- `.csv`
- `.json`
- `.txt`

### ✅ **4. Annotation Tool**
Using spaCy NER + ML intent prediction with editable corrections:
- Shows predicted intent
- Extracts entities automatically
- Saves annotations in JSON format

### ✅ **5. spaCy Model Training**
Includes:
- Training–test split
- Loss tracking
- Multiple epochs
- Model saved to `/models/intent_model`

### ✅ **6. Model Evaluation**
Generates:
- Classification Report
- Accuracy / Precision / Recall / F1
- Confusion Matrix (saved as image)

### ✅ **7. Active Learning**
Filters low-confidence samples (<50–60%) for re-annotation.

### ✅ **8. Admin Dashboard**
Shows:
- Workspace usage
- Dataset stats
- Annotation completeness
- Model status
- Buttons to retrain & evaluate model

---

## 🏗 **System Architecture**

               ┌────────────────────────────┐
               │          Frontend           │
               │      Streamlit Pages        │
               ├────────────────────────────┤
               │ Login / Workspaces          │
               │ Dataset Upload              │
               │ Annotator (Model + NER)     │
               │ Train spaCy Model           │
               │ Evaluate Model              │
               │ Active Learning             │
               │ Admin Dashboard             │
               └───────────────┬────────────┘
                               │
                               ▼
               ┌────────────────────────────┐
               │          Backend            │
               │     Python Modules          │
               ├────────────────────────────┤
               │ trainer.py                  │
               │ evaluator.py                │
               │ spacy_intent_model.py       │
               │ File-based DB (JSON/CSV)    │
               └───────────────┬────────────┘
                               │
                               ▼
               ┌────────────────────────────┐
               │      Data & Models         │
               ├────────────────────────────┤
               │ data/workspaces            │
               │ annotations.json           │
               │ trained spaCy model        │
               └────────────────────────────┘

---

## 📂 **Project Structure**

INFOSYS_PROJECT/
│── app.py                         # Main Streamlit entry point
│── requirements.txt               # All required Python packages
│── README.md                      # Documentation
│── LICENSE                        # MIT License
│
├── pages/                         # Streamlit multipage interface
│   │
│   ├── 1_Login.py                 # User authentication
│   ├── 2_Workspace.py             # Workspace creation & selection
│   ├── 3_UploadDataset.py         # Dataset upload (CSV/TXT/JSON)
│   ├── 4_Annotate.py              # Annotation (intent + entities)
│   ├── 5_TrainModel.py            # Train spaCy textcat model
│   ├── 6_TestEvaluate.py          # Evaluate model (report + matrix)
│   ├── 7_ActiveLearning.py        # Low-confidence sample mining
│   ├── 0_Admin_Dashboard.py       # Admin control dashboard
│
├── backend/                       # All backend logic (Python modules)
│   │
│   ├── trainer.py                 # Train spaCy intent classifier
│   ├── evaluator.py               # Evaluate model performance
│   ├── spacy_intent_model.py      # Load / Predict intents using spaCy
│   ├── utils.py                   # Optional helper utilities
│
├── models/                        # Stores trained models
│   └── intent_model/              # Generated after training (spaCy)
│
├── data/                          # All user data stored here
│   └── workspaces/
│       └── USERNAME/              # Each user's directory
│           └── WORKSPACE_NAME/    # Workspace directory
│               │── dataset.csv    # Uploaded dataset
│               │── annotations.json # User-annotated data
│               └── any other outputs
│
└── assets/                        # Optional (images, icons, diagrams)
    └── architecture.png


---

## ⚙️ **Installation**

### 1️⃣ Create environment

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m streamlit run app.py
py -m streamlit run app.py


## **Modular Training workflow**
1. Upload a dataset

2. Annotate intents + entities

3. Go to Train spaCy Model

4. Choose epochs

5. Train model → saved into /models/intent_model

6. Evaluate model under Test & Evaluate

7. Low-confidence predictions appear in Active Learning

## **📦 Datasets Included**

Travel dataset (40 samples)

Food ordering dataset (40 samples)

Economics / Banking dataset (40 samples)

You can extend your own datasets via the Upload module.

## **📜 License**

This project is licensed under the MIT License.
See the LICENSE file for details.

## **👨‍💻 Author**

Abiram
NLU / ML Developer

## **⭐ If you like this project**

Don’t forget to star the repo ⭐
