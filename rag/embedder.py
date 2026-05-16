"""
embedder.py - Embeds mental health journal entries using SentenceTransformers
Author: VitaTwin AI Team
"""

import json
import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH  = os.path.join(BASE_DIR, "data", "mental_health_logs.json")
INDEX_PATH = os.path.join(BASE_DIR, "data", "faiss_index.bin")
META_PATH  = os.path.join(BASE_DIR, "data", "entry_metadata.pkl")

MODEL_NAME = "all-MiniLM-L6-v2"   # fast, free, no API key needed


def load_data(path: str = DATA_PATH) -> list[dict]:
    with open(path, "r") as f:
        return json.load(f)


def build_text(entry: dict) -> str:
    """
    Combines all meaningful fields into a single string for embedding.
    """
    activities = ", ".join(entry.get("activities", [])) or "none"
    text = (
        f"Date: {entry['date']}. "
        f"Mood: {entry['mood_score']}/10. "
        f"Stress: {entry['stress_level']}/10. "
        f"Sleep: {entry['sleep_hours']} hours. "
        f"Energy: {entry['energy_level']}/10. "
        f"Anxiety: {entry['anxiety_score']}/10. "
        f"Social interaction: {entry.get('social_interaction', 'unknown')}. "
        f"Activities: {activities}. "
        f"Journal: {entry['journal']}"
    )
    return text


def build_index(data: list[dict], model: SentenceTransformer) -> tuple:
    """
    Builds a FAISS index from the data entries.
    Returns (faiss_index, metadata_list).
    """
    texts    = [build_text(e) for e in data]
    vectors  = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    vectors  = vectors.astype(np.float32)

    dim   = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    metadata = [
        {
            "entry_id":          e["entry_id"],
            "user_id":           e["user_id"],
            "date":              e["date"],
            "mood_score":        e["mood_score"],
            "stress_level":      e["stress_level"],
            "sleep_hours":       e["sleep_hours"],
            "energy_level":      e["energy_level"],
            "anxiety_score":     e["anxiety_score"],
            "social_interaction":e.get("social_interaction", "unknown"),
            "activities":        e.get("activities", []),
            "journal":           e["journal"],
            "text":              texts[i],
        }
        for i, e in enumerate(data)
    ]
    return index, metadata


def save_index(index, metadata: list[dict]) -> None:
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)
    print(f"[Embedder] Index saved → {INDEX_PATH}")
    print(f"[Embedder] Metadata saved → {META_PATH}")


def load_index():
    """
    Loads existing FAISS index and metadata from disk.
    Returns (faiss_index, metadata_list, model).
    """
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        raise FileNotFoundError(
            "FAISS index not found. Run embedder.py directly first: "
            "python rag/embedder.py"
        )
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
    model = SentenceTransformer(MODEL_NAME)
    return index, metadata, model


def run_embedding_pipeline() -> None:
    """
    Full pipeline: load data → embed → save index.
    Call this once before launching the app, or on first run.
    """
    print("[Embedder] Loading data...")
    data = load_data()
    print(f"[Embedder] Loaded {len(data)} entries.")

    print("[Embedder] Loading sentence transformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("[Embedder] Building FAISS index...")
    index, metadata = build_index(data, model)

    save_index(index, metadata)
    print(f"[Embedder] Done. {len(metadata)} entries indexed.")


# ── Run directly to build index ─────────────────────────────────────────────
if __name__ == "__main__":
    run_embedding_pipeline()