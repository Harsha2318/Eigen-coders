import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load FAISS index
index = faiss.read_index("medical_index.faiss")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample documents (should be same as indexed)
documents = [
    "AI improves healthcare diagnosis",
    "Machine learning in medicine",
    "Blockchain for secure medical records"
]

def search_articles(query, k=2):
    """Searches indexed articles based on a query."""
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k)

    results = [{"document": documents[i], "score": float(D[0][j])} for j, i in enumerate(I[0])]
    return results

if __name__ == "__main__":
    query = "AI in medicine"
    results = search_articles(query)
    print(f"🔎 Search Results for '{query}':", results)
