# src/retrieval/faiss_retriever.py

import json
from typing import List, Dict, Any

import faiss

from src.config import CHUNKS_FILE, FAISS_FILE, TOP_K
from src.embeddings.embedder import MultiModalEmbedder


class FaissRetriever:
    """
    FAISS-based retriever over pre-computed text / table / image-OCR chunks.
    """

    def __init__(
        self,
        faiss_path: str | None = None,
        chunks_path: str | None = None,
        k: int = TOP_K,
    ) -> None:
        self.k = k

        self.chunks_path = str(chunks_path or CHUNKS_FILE)
        self.faiss_path = str(faiss_path or FAISS_FILE)

        # Load chunks
        self.chunks: List[Dict[str, Any]] = []
        with open(self.chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    self.chunks.append(json.loads(line))

        # Load FAISS index
        self.index = faiss.read_index(self.faiss_path)

        # Text embedder (MiniLM, matches index)
        self.embedder = MultiModalEmbedder()

    def search(self, query: str, top_k: int | None = None) -> List[Dict[str, Any]]:
        """
        Return top-k chunks for a text query.

        Each result dict has: rank, score, chunk (original dict).
        """
        k = top_k or self.k

        query_vec = self.embedder.embed_texts([query])  # shape (1, d)
        scores, ids = self.index.search(query_vec, k)

        scores = scores[0]
        ids = ids[0]

        results: List[Dict[str, Any]] = []
        for rank, (score, idx) in enumerate(zip(scores, ids), start=1):
            if idx < 0 or idx >= len(self.chunks):
                continue
            chunk = self.chunks[idx]
            results.append(
                {
                    "rank": rank,
                    "score": float(score),
                    "chunk": chunk,
                }
            )
        return results
