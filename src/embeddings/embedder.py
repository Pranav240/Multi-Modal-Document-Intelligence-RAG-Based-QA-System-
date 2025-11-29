# src/embeddings/embedder.py

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class MultiModalEmbedder:
    """
    Wrapper around a SentenceTransformer text model.

    This is used only for retrieval embeddings.
    The FAISS index on disk was built with this same model:
    'sentence-transformers/all-MiniLM-L6-v2'.

    Do NOT change the model name unless you re-embed everything
    and rebuild the FAISS index.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Encode a list of strings to a (N, D) float32 numpy array."""
        vecs = self.model.encode(texts, show_progress_bar=False)
        return np.asarray(vecs, dtype="float32")
