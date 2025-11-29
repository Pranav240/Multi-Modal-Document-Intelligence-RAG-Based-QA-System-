# src/rag/qa_pipeline.py

from __future__ import annotations

from typing import List, Dict, Any, Optional

from openai import OpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS
from src.retrieval.faiss_retriever import FaissRetriever


class RAGQASystem:
    """
    RAG QA system: FAISS retrieval + GPT-4o answer generation.
    """

    def __init__(self, k: int = 5) -> None:
        # OpenAI client
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        # Retriever (MiniLM + FAISS)
        self.retriever = FaissRetriever(k=k)

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------
    def _format_context(self, hits: List[Dict[str, Any]]) -> str:
        """
        Turn retrieved chunks into a single context string for the LLM.
        """
        parts: List[str] = []
        for h in hits:
            chunk = h["chunk"]
            page = chunk.get("page", "?")
            modality = chunk.get("modality", "text")
            content = chunk.get("content", "")

            parts.append(f"[page {page}, {modality}] {content}")

        return "\n\n".join(parts)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def answer_question(
        self,
        question: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Main entry point.

        Returns dict with:
          - "answer": str
          - "hits": list of retrieved chunks
        """
        # 1) Retrieve
        hits = self.retriever.search(question, top_k=top_k)

        # 2) Context for GPT-4o
        context = self._format_context(hits)

        system_msg = (
            "You are a helpful assistant for question-answering about the "
            "IMF 2024 Article IV Consultation report for Qatar. "
            "Use ONLY the context from the report that I provide. "
            "If the answer is not contained in the context, say you do not know. "
            "When possible, mention page numbers from the context."
        )

        user_msg = (
            f"Question:\n{question}\n\n"
            f"Context from the report:\n{context}\n\n"
            "Answer based only on this context."
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ]

        # 3) Call GPT-4o
        resp = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=OPENAI_MAX_TOKENS,
            temperature=0.1,
        )

        answer_text = resp.choices[0].message.content.strip()

        return {
            "answer": answer_text,
            "hits": hits,
        }
