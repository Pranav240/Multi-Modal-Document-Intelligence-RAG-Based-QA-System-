# src/ingestion/extract_text.py

from typing import List, Dict
import pdfplumber
from pathlib import Path


def extract_text_chunks(pdf_path: Path) -> List[Dict]:
    """
    Extracts text from each page of the PDF and returns a list of chunk dicts.
    For now, we use one chunk per page. We can make chunking smarter later.
    """
    chunks: List[Dict] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue  # skip empty pages

            chunk = {
                "modality": "text",
                "page": page_idx + 1,          # 1-based page index
                "section_title": None,         # can set later if we do heading detection
                "content": text,
                "raw_payload": {}
            }
            chunks.append(chunk)

    print(f"[extract_text] extracted {len(chunks)} text chunks")
    return chunks
