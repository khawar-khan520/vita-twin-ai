# 🧠 VitaTwin Mind AI

An AI-powered Mental Health Intelligence System combining **RAG, Knowledge Graphs, and Explainable AI** for early stress and burnout detection.

---

## 🚀 Overview

VitaTwin Mind AI is a prototype system that analyzes user mental health signals (mood, stress, sleep, journal entries) and generates **early risk insights** using AI.

It combines:

- Retrieval-Augmented Generation (RAG)
- FAISS vector similarity search
- Rule-based risk detection
- Knowledge graph reasoning
- Explainable AI outputs
- Streamlit interactive UI

---

## 🏗 Architecture

1. User enters a mental health query
2. Query is embedded using SentenceTransformer
3. FAISS retrieves relevant historical entries
4. Risk detection engine analyzes:
   - stress levels
   - sleep patterns
   - mood trends
5. Knowledge graph models relationships:
   - low sleep → stress → burnout
6. System returns explainable insights in UI

---

## 🧰 Tech Stack

- Python
- SentenceTransformers
- FAISS
- Streamlit
- NetworkX

---

## ⚙️ Features

- Semantic search over mental health logs
- Early burnout/stress detection
- Explainable AI reasoning
- Knowledge graph relationships
- Interactive Streamlit dashboard

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py