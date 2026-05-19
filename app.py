import streamlit as st
from dotenv import load_dotenv
from rag.pipeline import answer_question

load_dotenv()

st.set_page_config(page_title="Hybrid Academic RAG Assistant", page_icon="📚")
st.title("📚 Hybrid Academic RAG Assistant")
st.write("Ask questions from PDFs already ingested into ChromaDB.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("📌 Project Flow")
    st.write("1. Run `streamlit run ingest.py`")
    st.write("2. Upload PDFs and build ChromaDB")
    st.write("3. Run this app and ask questions")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared.")

st.subheader("📌 Quick Question Suggestions")

suggestions = [
    "Summarize the stored documents",
    "List important topics from the stored documents",
    "Explain this concept simply",
    "Give 5 exam questions from the stored documents"
]

cols = st.columns(2)
selected_question = None

for index, suggestion in enumerate(suggestions):
    with cols[index % 2]:
        if st.button(suggestion):
            selected_question = suggestion

st.subheader("💬 Ask Questions")
typed_question = st.chat_input("Ask a question from stored PDFs...")
question = selected_question if selected_question else typed_question

if question:
    with st.spinner("Rewriting query, retrieving, reranking, and generating answer..."):
        try:
            result = answer_question(question, st.session_state.chat_history)
            st.session_state.chat_history.append({
                "question": question,
                "answer": result["answer"],
                "sources": result["sources"],
                "rewritten_query": result["rewritten_query"]
            })
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure you ran `streamlit run ingest.py` and built ChromaDB first.")

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])
        with st.expander("Retrieved details"):
            st.write("Rewritten query:", chat.get("rewritten_query", ""))
            if chat.get("sources"):
                st.write("Sources:")
                for source in chat["sources"]:
                    st.write(f"- {source}")
