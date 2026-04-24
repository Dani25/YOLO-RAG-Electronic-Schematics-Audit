from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

class Retriever:

    def __init__(self, dataset_path):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        with open(dataset_path) as f:
            self.data = json.load(f)

        self.texts = [
            f"{d['part_number']} {d.get('category','')} {d.get('description','')}"
            for d in self.data
        ]

        self.embeddings = self.model.encode(self.texts)

        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings))

    def search(self, query, k=5):
        q_emb = self.model.encode([query])
        D, I = self.index.search(np.array(q_emb), k)

        results = [self.data[i] for i in I[0]]
        return results
