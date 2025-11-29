# src/embeddings/build_index.py

import json
from typing import List, Dict

import numpy as np
import faiss

from src.config import CHUNKS_PATH, FAISS_TEXT
from .embedder import MultiModalEmbedder


def load_chunks() -> List[Dict]:
    """
    Load all chunks from chunks.jsonl.
    """
    print(f"[build_index] Loading chunks from {CHUNKS_PATH}")
    chunks: List[Dict] = []
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            chunks.append(json.loads(line))

    print(f"[build_index] Loaded {len(chunks)} chunks")
    return chunks


def build_faiss_index(vectors: np.ndarray) -> faiss.Index:
    """
    Build a FAISS L2 index from embeddings.
    """
    dim = vectors.shape[1]
    print(f"[build_index] Building FAISS IndexFlatL2 with dim={dim}")
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    print(f"[build_index] Index now contains {index.ntotal} vectors")
    return index


def main() -> None:
    print("[build_index] START")

    # 1) Load chunks
    chunks = load_chunks()
    if not chunks:
        print("[build_index] No chunks found, aborting.")
        return

    # 2) Embed them
    embedder = MultiModalEmbedder()
    embeddings = embedder.embed_chunks(chunks)
    print(f"[build_index] Embeddings shape: {embeddings.shape}")
    assert embeddings.shape[0] == len(chunks), "Embedding count mismatch"

    # 3) Build FAISS index
    index = build_faiss_index(embeddings)

    # 4) Save index to disk
    print(f"[build_index] Saving FAISS index to {FAISS_TEXT}")
    faiss.write_index(index, str(FAISS_TEXT))

    # 5) Save lightweight metadata for retrieval (position, ids, modality)
    meta_path = CHUNKS_PATH.with_name("chunks_metadata.jsonl")
    print(f"[build_index] Saving metadata to {meta_path}")
    with open(meta_path, "w", encoding="utf-8") as f:
        for i, c in enumerate(chunks):
            meta = {
                "pos": i,
                "id": c.get("id"),
                "doc_id": c.get("doc_id"),
                "modality": c.get("modality"),
                "page": c.get("page"),
                "section_title": c.get("section_title"),
            }
            f.write(json.dumps(meta, ensure_ascii=False) + "\n")

    print("[build_index] DONE ✅")


if __name__ == "__main__":
    main()
