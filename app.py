# app.py  - Streamlit conversational chat for Qatar IMF RAG

import streamlit as st

from src.rag.qa_pipeline import RAGQASystem


@st.cache_resource(show_spinner=True)
def load_rag_system() -> RAGQASystem:
    """
    Load RAG system once and reuse (FAISS + MiniLM + GPT-4o).
    """
    return RAGQASystem(k=5)


def main() -> None:
    st.set_page_config(
        page_title="Qatar IMF 2024 – RAG QA Chat",
        page_icon="📄",
        layout="wide",
    )

    st.title("Qatar IMF 2024 – RAG QA Chat")
    st.write(
        "Ask anything about the IMF 2024 Article IV Consultation report for Qatar. "
        
    )

    # Session state for chat
    if "messages" not in st.session_state:
        st.session_state["messages"] = []  # list of {role, content}
    if "last_hits" not in st.session_state:
        st.session_state["last_hits"] = []

    qa_system = load_rag_system()

    # ---------------- Chat history display ---------------- #
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"🧑‍💻 **You:** {msg['content']}")
        else:
            st.markdown(f"🤖 **Assistant:** {msg['content']}")

    st.markdown("---")

    # ---------------- Input form ---------------- #
    with st.form("qa_form", clear_on_submit=True):
        user_input = st.text_input(
            "Type your question and press Enter:",
            key="user_input",
            placeholder="Ask something from the Qatar IMF 2024 report...",
        )
        submitted = st.form_submit_button("Ask")

    if submitted and user_input.strip():
        question = user_input.strip()

        # Add user message to history
        st.session_state["messages"].append({"role": "user", "content": question})

        # Call RAG pipeline
        with st.spinner("Retrieving context and generating answer..."):
            result = qa_system.answer_question(
                question,
                chat_history=st.session_state["messages"],
            )

        answer_text = result["answer"]
        st.session_state["messages"].append(
            {"role": "assistant", "content": answer_text}
        )
        st.session_state["last_hits"] = result["hits"]

        # ✅ NEW: use st.rerun() instead of experimental_rerun
        st.rerun()

    # ---------------- Debug: show retrieved chunks ---------------- #
    if st.session_state["last_hits"]:
        with st.expander("Show retrieved chunks (debug)"):
            for h in st.session_state["last_hits"]:
                chunk = h["chunk"]
                page = chunk.get("page", "?")
                modality = chunk.get("modality", "text")
                content = chunk.get("content", "")

                st.markdown(
                    f"**Rank {h['rank']} | Score {h['score']:.3f} | "
                    f"Page {page} | {modality}**"
                )
                st.write(content[:2000])
                st.markdown("---")


if __name__ == "__main__":
    main()
