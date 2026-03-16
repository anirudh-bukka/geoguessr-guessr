import faiss
import numpy as np
import pickle
from config import INDEX_PATH, METADATA_PATH


class VectorStore:

    def __init__(self, dim=512):

        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embedding, meta):

        self.index.add(np.array([embedding]))
        self.metadata.append(meta)

    def save(self):

        faiss.write_index(self.index, INDEX_PATH)

        with open(METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):

        self.index = faiss.read_index(INDEX_PATH)

        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, embedding, k=5):

        distances, indices = self.index.search(np.array([embedding]), k)

        results = []

        for i in indices[0]:
            results.append(self.metadata[i])

        return results