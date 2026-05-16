"""
retriever.py - Retrieves relevant mental health entries from FAISS vector store
Author: VitaTwin AI Team
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from rag.embedder import load_index


# ── Module-level cache (loaded once per session) ───────────────────────────────
_index    = None
_metadata = None
_model    = None


def _ensure_loaded():
    global _index, _metadata, _model
    if _index is None:
        _index, _metadata, _model = load_index()


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """
    Embeds the query and returns the top_k most relevant entries.

    Args:
        query:  Natural language question about mental health state.
        top_k:  Number of entries to retrieve.

    Returns:
        List of metadata dicts for the closest entries.
    """
    _ensure_loaded()

    query_vec = _model.encode([query], convert_to_numpy=True).astype(np.float32)
    distances, indices = _index.search(query_vec, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        entry = dict(_metadata[idx])
        entry["similarity_score"] = float(1 / (1 + dist))   # normalised 0-1
        results.append(entry)

    return results


def retrieve_by_user(user_id: str, top_k: int = 10) -> list[dict]:
    """
    Returns all entries for a specific user, sorted by date.
    """
    _ensure_loaded()
    user_entries = [m for m in _metadata if m["user_id"] == user_id]
    user_entries.sort(key=lambda x: x["date"])
    return user_entries[:top_k]


def retrieve_recent(days: int = 7) -> list[dict]:
    """
    Returns entries from the most recent N days across all users.
    """
    _ensure_loaded()
    from datetime import datetime, timedelta

    cutoff = datetime(2024, 1, 1)   # baseline for dataset; adjust for live data
    results = [
        m for m in _metadata
        if datetime.strptime(m["date"], "%Y-%m-%d") >= cutoff
    ]
    results.sort(key=lambda x: x["date"], reverse=True)
    return results[:days * 3]   # rough estimate: 3 users active per day


def format_retrieved_context(entries: list[dict]) -> str:
    """
    Formats retrieved entries into a readable context string for generation.
    """
    if not entries:
        return "No relevant entries found."

    lines = []
    for e in entries:
        lines.append(
            f"[{e['date']} | {e['user_id']}] "
            f"Mood={e['mood_score']}/10, Stress={e['stress_level']}/10, "
            f"Sleep={e['sleep_hours']}h, Anxiety={e['anxiety_score']}/10 — "
            f"\"{e['journal']}\""
        )
    return "\n".join(lines)


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    results = retrieve("user feeling overwhelmed and not sleeping", top_k=3)
    print(format_retrieved_context(results))