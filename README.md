# Multi-Modal Document Intelligence — RAG-Based QA System

## Overview
A Retrieval-Augmented Generation (RAG) system for question answering over documents that contain a mix of text, tables, and scanned/image content. Built around a Streamlit chat interface, it currently targets the Qatar IMF 2024 Article IV Consultation report as its sample corpus, but the pipeline is generalizable to other multi-modal PDF documents.

## Architecture
- **Ingestion**: PDFs are parsed with `pdfplumber` and `pymupdf` for native text, while `camelot-py` and `tabula-py` handle structured table extraction. Pages containing scanned or image-based content are processed via `pdf2image` + `pytesseract` OCR.
- **Embeddings**: Each extracted chunk (text, table, or OCR'd image content) is embedded using `sentence-transformers` MiniLM models.
- **Retrieval**: Embeddings are indexed with FAISS (`faiss-cpu`) for fast approximate nearest-neighbor search; the top-k (default k=5) most relevant chunks are retrieved per query.
- **Generation**: Retrieved chunks and chat history are passed to GPT-4o (via the OpenAI API) to generate a grounded answer.
- **UI**: A Streamlit chat interface displays conversation history and includes a debug panel to inspect retrieved chunks, their similarity scores, source page numbers, and modality (text/table/image).

Project layout:
```
src/
  ingestion/     # PDF parsing, table extraction, OCR
  embeddings/    # MiniLM embedding generation
  retrieval/     # FAISS indexing and similarity search
  rag/           # RAGQASystem — orchestrates retrieval + GPT-4o generation
  config.py
app.py           # Streamlit entry point
requirements.txt
```

## Example Usage

Screenshots below show the system answering questions from the Qatar IMF 2024 report, including a text-based query, a table-lookup query, and the debug panel showing retrieved chunks with similarity scores and page citations.

Text-based query:

[screenshot placeholder]

Table-lookup query:

[screenshot placeholder]

Retrieved chunks (debug view):

[screenshot placeholder]

## Setup & Running

1. Clone the repository and navigate into it.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Some dependencies require external binaries:
   - `pytesseract` requires Tesseract OCR installed on your system.
   - `pdf2image` requires `poppler` installed on your system.
   - `camelot-py[cv]` requires Ghostscript.
5. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```
6. Run the app:
   ```
   streamlit run app.py
   ```

## Known Limitations
- **Multi-row numeric table extraction**: There is an intermittent decimal-point parsing bug when extracting tables that span multiple rows of numeric data — decimal points can occasionally be dropped or misplaced during extraction, affecting the accuracy of numeric values pulled from tables. This is a known issue under investigation.
