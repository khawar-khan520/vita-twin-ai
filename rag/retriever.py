import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("data/mental_health.index")

# Load original data
with open("data/mental_health_logs.json", "r") as f:
    data = json.load(f)

def retrieve(query, top_k=3):
    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    distances, indices = index.search(query_vec, top_k)

    results = [data[i] for i in indices[0]]

    return results


# quick test
if __name__ == "__main__":
    q = "stress and burnout"
    print(retrieve(q))