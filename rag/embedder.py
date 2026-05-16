from sentence_transformers import SentenceTransformer
import json
import faiss

from sentence_transformers import SentenceTransformer

# LOAD ONCE (GLOBAL)
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading dataset...")

with open("data/mental_health_logs.json", "r") as f:
    data = json.load(f)

texts = [entry["journal"] for entry in data]

print("Generating embeddings...")

embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

print("Creating FAISS index...")

dimension = embeddings.shape[1]


index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, "data/mental_health.index")

print("FAISS index created successfully.")