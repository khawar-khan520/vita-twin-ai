# VitaTwin Mind AI

## Overview
An AI-powered mental health intelligence system combining:

- Retrieval-Augmented Generation (RAG)
- FAISS vector search
- Rule-based risk detection
- Knowledge graph reasoning
- Explainable AI outputs

## Architecture

1. User query
2. Sentence embedding (MiniLM)
3. FAISS retrieval of mental health logs
4. Risk analysis (stress + sleep patterns)
5. Graph-based mental health relationships
6. Explainable output in Streamlit UI

## Tech Stack
- Python
- SentenceTransformers
- FAISS
- Streamlit
- NetworkX

## Key Features
- Early stress/burnout detection
- Explainable reasoning
- Semantic search over mental health logs
- Graph-based mental health relationships

## How to Run
```bash
streamlit run app/streamlit_app.py