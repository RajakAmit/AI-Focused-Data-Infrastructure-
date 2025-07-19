# src/api/rag_api.py

from typing import List

from fastapi import FastAPI, Query
from pydantic import BaseModel

from src.embed.query_faiss import query_faiss

app = FastAPI(title="RAG API", version="1.0")

class RAGResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/ask", response_model=RAGResponse)
def ask_question(question: str = Query(..., description="Your question"), top_k: int = 5):
    results = query_faiss(question, top_k)

    if not results:
        answer = "Sorry, I couldn't find any relevant documents."
    else:
        answer = "Summary based on top sources:\n" + "\n".join(
            f"- {res['title']}" for res in results if res.get("title")
        )

    return {
        "answer": answer,
        "sources": results
    }
