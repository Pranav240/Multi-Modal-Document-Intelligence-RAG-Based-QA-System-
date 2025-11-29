# src/ingestion/extract_tables.py

from typing import List, Dict
from pathlib import Path
import pdfplumber
import pandas as pd


def extract_table_chunks(pdf_path: Path) -> List[Dict]:
    """
    Extract tables from each page using pdfplumber.
    Each table is converted to a pandas DataFrame and then to CSV-like text
    for embeddings. The original table data is stored in raw_payload.
    """
    chunks: List[Dict] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if not tables:
                continue

            for t_idx, t in enumerate(tables):
                # pdfplumber returns a list of rows; first row is header (often)
                if not t or len(t) < 2:
                    continue

                header = t[0]
                rows = t[1:]

                # Fallback headers if something is weird
                if any(h is None for h in header):
                    header = [f"col_{i}" for i in range(len(header))]

                df = pd.DataFrame(rows, columns=header)

                # Convert to CSV-like string for embedding
                csv_str = df.to_csv(index=False)

                chunk = {
                    "modality": "table",
                    "page": page_idx + 1,
                    "section_title": None,
                    "content": f"Table on page {page_idx + 1} (table {t_idx + 1}):\n{csv_str}",
                    "raw_payload": {
                        "table": df.to_dict(orient="records"),
                        "columns": list(df.columns),
                    },
                }
                chunks.append(chunk)

    print(f"[extract_tables] extracted {len(chunks)} table chunks")
    return chunks
