# app/faiss_store.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class FAISSStore:
    def __init__(self, dim=384):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []   # store original text chunks
        self.metadatas = []  # phone dicts

    def add(self, text, metadata):
        embedding = self.model.encode([text])[0].astype("float32")
        self.index.add(np.array([embedding]))
        self.texts.append(text)
        self.metadatas.append(metadata)

    def search(self, query, k=3):
        q_emb = self.model.encode([query])[0].astype("float32")
        distances, idxs = self.index.search(np.array([q_emb]), k)
        results = []
        for idx in idxs[0]:
            if idx < len(self.texts):
                results.append(self.metadatas[idx])
        return results
