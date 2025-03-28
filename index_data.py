import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample documents (Replace with real PubMed articles)
documents = [
    "AI improves healthcare diagnosis",
    "Machine learning in medicine",
    "Blockchain for secure medical records"
]

# Convert documents to embeddings
embeddings = model.encode(documents)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save the index
faiss.write_index(index, "medical_index.faiss")

print("✅ Data indexed successfully!")
