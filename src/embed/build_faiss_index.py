import pathlib
import pickle

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

DATA_GOLD_PATH = pathlib.Path("data/gold/gold.parquet")
FAISS_INDEX_PATH = pathlib.Path("data/faiss/index.faiss")
METADATA_PATH = pathlib.Path("data/faiss/metadata.pkl")

def build_faiss_index():
    print(f"Loading gold data from {DATA_GOLD_PATH}")
    df = pd.read_parquet(DATA_GOLD_PATH)

    # Extract the text content to embed
    texts = df['content'].fillna("").tolist()

    print("Loading SentenceTransformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print(f"Generating embeddings for {len(texts)} documents...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    dim = embeddings.shape[1]
    print(f"Embedding dimension: {dim}")

    # Create FAISS index (IndexFlatL2)
    index = faiss.IndexFlatL2(dim)

    print("Adding embeddings to the FAISS index...")
    index.add(embeddings)

    # Save index
    FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    print(f"Saved FAISS index to {FAISS_INDEX_PATH}")

    # Save metadata for retrieval (title, link)
    metadata = df[['title', 'link', 'published']].to_dict(orient='records')
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"Saved metadata to {METADATA_PATH}")

if __name__ == "__main__":
    build_faiss_index()
      