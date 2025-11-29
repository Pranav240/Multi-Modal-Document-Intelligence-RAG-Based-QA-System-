# src/ingestion/build_chunks.py

import json
import uuid
from pathlib import Path
from typing import List, Dict

from src.config import RAW_PDF, CHUNKS_PATH, IMAGES_DIR
from .extract_text import extract_text_chunks
from .extract_tables import extract_table_chunks
from .extract_images_ocr import extract_image_chunks


def build_all_chunks() -> List[Dict]:
    """
    Run all ingestion steps (text, tables, images/OCR) and combine
    into a single list of chunks with IDs and doc_id.
    """
    print(f"[build_chunks] Using PDF: {RAW_PDF}")

    text_chunks = extract_text_chunks(RAW_PDF)
    table_chunks = extract_table_chunks(RAW_PDF)
    image_chunks = extract_image_chunks(RAW_PDF, IMAGES_DIR)

    all_chunks: List[Dict] = []

    for c in text_chunks + table_chunks + image_chunks:
        c["id"] = str(uuid.uuid4())
        c["doc_id"] = "qatar_imf_2024"
        all_chunks.append(c)

    CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"[build_chunks] Saved {len(all_chunks)} chunks to {CHUNKS_PATH}")
    return all_chunks


if __name__ == "__main__":
    build_all_chunks()
