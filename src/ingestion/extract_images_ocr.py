# src/ingestion/extract_images_ocr.py

from typing import List, Dict
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image
import pytesseract


# ✅ Point pytesseract to your local Tesseract exe
pytesseract.pytesseract.tesseract_cmd = r"D:\rag_qatar\Tesseract-OCR\tesseract.exe"


def extract_image_chunks(pdf_path: Path, images_dir: Path) -> List[Dict]:
    """
    Render each page of the PDF as an image, run OCR using Tesseract,
    and return a list of 'image' modality chunks.
    """
    images_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    chunks: List[Dict] = []

    for page_idx in range(len(doc)):
        page = doc[page_idx]

        # Render page to an image
        pix = page.get_pixmap(dpi=200)
        img_path = images_dir / f"page_{page_idx + 1}.png"
        pix.save(str(img_path))

        # Convert raw pixmap to PIL image
        mode = "RGB" if pix.alpha == 0 else "RGBA"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)

        # OCR with Tesseract
        ocr_text = pytesseract.image_to_string(img)

        if not ocr_text.strip():
            # Skip pages where OCR found nothing meaningful
            continue

        chunk = {
            "modality": "image",
            "page": page_idx + 1,
            "section_title": None,
            "content": f"OCR text from page {page_idx + 1}:\n{ocr_text}",
            "raw_payload": {
                "image_path": str(img_path),
                "ocr_text": ocr_text,
            },
        }
        chunks.append(chunk)

    doc.close()

    print(f"[extract_images_ocr] extracted {len(chunks)} image/OCR chunks")
    return chunks
