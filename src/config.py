# src/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load variables from .env (OPENAI_API_KEY, etc.)
load_dotenv()

# -----------------------------
# OpenAI settings
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "400"))

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

CHUNKS_FILE = DATA_DIR / "chunks.jsonl"
FAISS_FILE = DATA_DIR / "embeddings_text.faiss"
METADATA_FILE = DATA_DIR / "chunks_metadata.jsonl"

# -----------------------------
# Retrieval settings
# -----------------------------
TOP_K = 5  # default number of chunks per query

# -----------------------------
# OCR (used only at ingestion stage)
# -----------------------------
TESSERACT_PATH = r"D:\rag_qatar\Tesseract-OCR\tesseract.exe"
