"""
retriever.py - FAISS-based retrieval layer for VitaTwin AI
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from datetime import datetime, timedelta
from rag.embedder import load_index

# ── Global cache ─────────────────────────────


# 🔥 GLOBAL LOAD (RUNS ONCE ONLY)
_index, _metadata, _model = load_index()

def _ensure_loaded():
    global _index, _metadata, _model

    if _index is None:
        _index, _metadata, _model = load_index()

    if _model is None:
        raise ValueError("Embedding model not loaded from embedder.py")


# ── Main retrieval ───────────────────────────
def retrieve(query: str, top_k: int = 5):

    query_vec = _model.encode([query], convert_to_numpy=True)
    query_vec = np.array(query_vec).astype("float32")

    distances, indices = _index.search(query_vec, top_k)

    results = []

    for dist, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        entry = _metadata[idx]

        if not isinstance(entry, dict):
            entry = dict(entry)

        entry["similarity_score"] = float(1 / (1 + dist))

        results.append(entry)

    return results

# ── User-based retrieval ─────────────────────
def retrieve_by_user(user_id: str, top_k: int = 10):

    _ensure_loaded()

    user_entries = [
        m for m in _metadata
        if isinstance(m, dict) and m.get("user_id") == user_id
    ]

    user_entries.sort(key=lambda x: x.get("date", ""))

    return user_entries[:top_k]


# ── Recent retrieval (FIXED) ─────────────────
def retrieve_recent(days: int = 7):

    _ensure_loaded()

    cutoff = datetime.now() - timedelta(days=days)

    results = []

    for m in _metadata:

        if not isinstance(m, dict):
            continue

        try:
            entry_date = datetime.strptime(m["date"], "%Y-%m-%d")
        except:
            continue

        if entry_date >= cutoff:
            results.append(m)

    results.sort(key=lambda x: x["date"], reverse=True)

    return results


# ── Formatting ───────────────────────────────
def format_retrieved_context(entries: list[dict]) -> str:

    if not entries:
        return "No relevant entries found."

    lines = []

    for e in entries:
        lines.append(
            f"[{e.get('date', '?')} | {e.get('user_id', '?')}] "
            f"Mood={e.get('mood_score', '?')}/10, "
            f"Stress={e.get('stress_level', '?')}/10, "
            f"Sleep={e.get('sleep_hours', '?')}h, "
            f"Anxiety={e.get('anxiety_score', '?')}/10 — "
            f'"{e.get("journal", "")}"'
        )

    return "\n".join(lines)


# ── Test ─────────────────────────────────────
if __name__ == "__main__":

    results = retrieve("stress burnout poor sleep", top_k=3)

    print(format_retrieved_context(results))

