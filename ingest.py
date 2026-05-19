import os
import shutil
import streamlit as st
from config import PDF_DIR
from rag.document_loader import load_all_pdfs
from rag.chunker import chunk_documents
from rag.vector_store import add_documents_to_chroma, reset_chroma_collection


st.set_page_config(page_title="Admin PDF Ingestion", page_icon="⚙️")
st.title("⚙️ Admin PDF Ingestion")
st.write("Upload PDFs once. They will be extracted, chunked, embedded, and stored permanently in ChromaDB.")

os.makedirs(PDF_DIR, exist_ok=True)

uploaded_pdfs = st.file_uploader(
    "Upload PDF files for knowledge base",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_pdfs:
    for pdf in uploaded_pdfs:
        save_path = os.path.join(PDF_DIR, pdf.name)
        with open(save_path, "wb") as f:
            f.write(pdf.getbuffer())
    st.success("PDFs saved into data/pdfs folder.")

if st.button("Build / Rebuild ChromaDB"):
    with st.spinner("Extracting PDFs, chunking, embedding, and storing in ChromaDB..."):
        reset_chroma_collection()
        documents = load_all_pdfs(PDF_DIR)
        if not documents:
            st.error("No readable PDF content found.")
        else:
            chunks = chunk_documents(documents)
            add_documents_to_chroma(chunks)
            st.success(f"Ingestion completed. Stored {len(chunks)} chunks in ChromaDB.")

if st.button("Clear Stored PDFs"):
    shutil.rmtree(PDF_DIR, ignore_errors=True)
    os.makedirs(PDF_DIR, exist_ok=True)
    st.success("PDF folder cleared.")
