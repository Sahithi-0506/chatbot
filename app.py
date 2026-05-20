import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from rag.pipeline import answer_question
from rag.vector_store import get_vector_store

load_dotenv()

CHAT_HISTORY_FILE = "chat_history.json"


def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []
    return []


def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, indent=4, ensure_ascii=False)


def clear_chat_history():
    st.session_state.chat_history = []

    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)


@st.cache_data(show_spinner=False)
def get_available_pdfs():
    try:
        db = get_vector_store()
        data = db.get(include=["metadatas"])

        pdfs = sorted({
            meta.get("file_name")
            for meta in data["metadatas"]
            if meta.get("file_name")
        })

        return ["All PDFs"] + pdfs

    except Exception:
        return ["All PDFs"]


st.set_page_config(
    page_title="Hybrid Academic RAG Assistant",
    page_icon="📚"
)

st.title("📚 Hybrid Academic RAG Assistant")
st.write("Ask questions from PDFs already ingested into ChromaDB.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

with st.sidebar:
    st.header("📌 Project Flow")
    st.write("1. Run `streamlit run ingest.py`")
    st.write("2. Upload PDFs and build ChromaDB")
    st.write("3. Run this app and ask questions")

    st.divider()

    selected_pdf = st.selectbox(
        "📄 Select PDF for answering",
        get_available_pdfs()
    )

    st.info(f"Currently selected: {selected_pdf}")

    st.divider()

    st.write(f"💬 Total chats: {len(st.session_state.chat_history)}")

    if st.button("Clear Chat History"):
        clear_chat_history()
        st.success("Chat history cleared.")
        st.rerun()

st.subheader("📌 Quick Question Suggestions")

suggestions = [
    "Summarize the selected PDF",
    "List important topics from the selected PDF",
    "Explain this concept simply from the selected PDF",
    "Give 5 exam questions from the selected PDF"
]

cols = st.columns(2)
selected_question = None

for index, suggestion in enumerate(suggestions):
    with cols[index % 2]:
        if st.button(suggestion):
            selected_question = suggestion

st.subheader("💬 Ask Questions")

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

        with st.expander("Retrieved details"):
            st.write("Selected PDF:", chat.get("selected_pdf", "All PDFs"))
            st.write("Rewritten query:", chat.get("rewritten_query", ""))

            if chat.get("sources"):
                st.write("Sources:")
                for source in chat["sources"]:
                    st.write(f"- {source}")

            if chat.get("timestamp"):
                st.caption(f"Asked at: {chat['timestamp']}")

typed_question = st.chat_input("Ask a question from stored PDFs...")
question = selected_question if selected_question else typed_question

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Rewriting query, retrieving, reranking, and generating answer..."):
        try:
            result = answer_question(
                question,
                st.session_state.chat_history,
                selected_pdf
            )

            new_chat = {
                "question": question,
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "rewritten_query": result.get("rewritten_query", ""),
                "selected_pdf": selected_pdf,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            st.session_state.chat_history.append(new_chat)
            save_chat_history(st.session_state.chat_history)

            with st.chat_message("assistant"):
                st.write(new_chat["answer"])

                with st.expander("Retrieved details"):
                    st.write("Selected PDF:", new_chat["selected_pdf"])
                    st.write("Rewritten query:", new_chat["rewritten_query"])

                    if new_chat["sources"]:
                        st.write("Sources:")
                        for source in new_chat["sources"]:
                            st.write(f"- {source}")

                    st.caption(f"Asked at: {new_chat['timestamp']}")

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure you ran `streamlit run ingest.py` and built ChromaDB first.")