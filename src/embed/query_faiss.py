# import pathlib
# import pickle

# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# FAISS_INDEX_PATH = pathlib.Path("data/faiss/index.faiss")
# METADATA_PATH = pathlib.Path("data/faiss/metadata.pkl")

# class FaissRetriever:
#     def __init__(self):
#         print("Loading FAISS index...")
#         self.index = faiss.read_index(str(FAISS_INDEX_PATH))
#         print("Loading metadata...")
#         with open(METADATA_PATH, 'rb') as f:
#             self.metadata = pickle.load(f)

#         print("Loading embedding model...")
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')

#     def query(self, text, top_k=5):
#         query_vec = self.model.encode([text], convert_to_numpy=True)
#         distances, indices = self.index.search(query_vec, top_k)

#         results = []
#         for dist, idx in zip(distances[0], indices[0]):
#             if idx < 0 or idx >= len(self.metadata):
#                 continue
#             meta = self.metadata[idx]
#             results.append({
#                 'title': meta['title'],
#                 'link': meta['link'],
#                 'published': meta['published'],
#                 'distance': float(dist),
#             })
#         return results

# if __name__ == "__main__":
#     retriever = FaissRetriever()
#     query_text = input("Enter your question: ")
#     results = retriever.query(query_text)
#     print("\nTop results:")
#     for res in results:
#         print(f"- {res['title']} ({res['published']})\n  Link: {res['link']}\n  Distance: {res['distance']:.4f}\n")



# src/embed/query_faiss.py

import pathlib
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

FAISS_INDEX_PATH = pathlib.Path("data/faiss/index.faiss")
METADATA_PATH = pathlib.Path("data/faiss/metadata.pkl")

class FaissRetriever:
    def __init__(self):
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))
        with open(METADATA_PATH, 'rb') as f:
            self.metadata = pickle.load(f)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def query(self, text, top_k=5):
        query_vec = self.model.encode([text], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if 0 <= idx < len(self.metadata):
                meta = self.metadata[idx]
                results.append({
                    'title': meta['title'],
                    'link': meta['link'],
                    'published': meta['published'],
                    'distance': float(dist),
                })
        return results

# This is the function used by rag_api.py
retriever = FaissRetriever()

def query_faiss(text, top_k=5):
    return retriever.query(text, top_k)

if __name__ == "__main__":
    while True:
        q = input("Ask a question: ")
        results = query_faiss(q)
        for r in results:
            print(f"{r['title']} - {r['distance']:.4f}")
