# This script builds a vector index for the dataset using CLIP embeddings.

from dataset.dataset_loader import load_dataset
from embeddings.clip_encoder import ClipEncoder
from retrieval.vector_store import VectorStore
from tqdm import tqdm


samples = load_dataset()

encoder = ClipEncoder()
store = VectorStore()

for sample in tqdm(samples):

    emb = encoder.encode(sample["path"])

    store.add(emb, sample)

store.save()

print("Vector index built successfully")