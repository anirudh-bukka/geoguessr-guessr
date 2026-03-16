import os
from dotenv import load_dotenv

load_dotenv()

# API KEYS
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# DATASET
DATASET_PATH = "dataset/geoguessr"

# VECTOR DB
INDEX_PATH = "dataset/faiss.index"
METADATA_PATH = "dataset/metadata.pkl"

# MODEL CONFIG
CLIP_MODEL = "openai/clip-vit-base-patch32"

# RETRIEVAL
TOP_K = 5