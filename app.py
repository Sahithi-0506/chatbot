import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()

st.set_page_config(page_title="Hybrid Academic RAG Assistant", page_icon="📚")

st.title("📚 Hybrid Academic RAG Assistant")
st.write("Upload academic PDFs and ask multiple questions with chat history.")


def get_pdf_text(pdf_docs):
    documents = []

    for pdf in pdf_docs:
        reader = PdfReader(pdf)

        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if page_text:
                documents.append({
                    "file_name": pdf.name,
                    "page": page_num,
                    "text": page_text
                })

    return documents


def get_text_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = []

    for doc in documents:
        split_texts = splitter.split_text(doc["text"])

        for i, chunk in enumerate(split_texts, start=1):
            if len(chunk.strip()) > 30:
                chunks.append({
                    "content": chunk,
                    "file_name": doc["file_name"],
                    "page": doc["page"],
                    "chunk_id": i
                })

    return chunks


def create_vector_store(chunks):
    documents = []

    for chunk in chunks:
        documents.append(
            Document(
                page_content=chunk["content"],
                metadata={
                    "file_name": chunk["file_name"],
                    "page": chunk["page"],
                    "chunk_id": chunk["chunk_id"]
                }
            )
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store


def retrieve_relevant_chunks(question, vector_store, top_k=4):
    docs = vector_store.similarity_search(question, k=top_k)

    context = "\n\n".join([doc.page_content for doc in docs])

    sources = []
    for doc in docs:
        source = f'{doc.metadata["file_name"]} - Page {doc.metadata["page"]}'
        if source not in sources:
            sources.append(source)

    return context, sources


def get_answer(question, context, chat_history):
    history_text = ""

    for chat in chat_history[-4:]:
        history_text += f"User: {chat['question']}\nAssistant: {chat['answer']}\n\n"

    prompt_template = """
    You are an academic study assistant.
    Answer the question clearly using only the given context and previous conversation history.

    If the answer is not available in the context, say:
    "The answer is not available in the uploaded document."

    Previous Conversation:
    {history}

    Context:
    {context}

    Current Question:
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )

    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | model

    response = chain.invoke({
        "history": history_text,
        "context": context,
        "question": question
    })

    return response.content


def summarize_documents(chunks):
    combined_text = "\n\n".join([chunk["content"] for chunk in chunks[:12]])

    prompt_template = """
    You are an academic study assistant.

    Summarize the uploaded academic documents clearly.

    Include:
    1. Main topic
    2. Important concepts
    3. Short exam-focused summary
    4. Key points to revise

    Context:
    {context}

    Summary:
    """

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )

    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | model

    response = chain.invoke({
        "context": combined_text
    })

    return response.content


if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_summary" not in st.session_state:
    st.session_state.document_summary = ""


with st.sidebar:
    st.header("📄 Upload Notes")

    pdf_docs = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process PDFs"):
        if pdf_docs:
            with st.spinner("Processing PDFs..."):
                documents = get_pdf_text(pdf_docs)

                if len(documents) == 0:
                    st.error("No readable text found in the uploaded PDFs.")
                else:
                    st.session_state.text_chunks = get_text_chunks(documents)
                    st.session_state.vector_store = create_vector_store(st.session_state.text_chunks)
                    st.session_state.chat_history = []
                    st.session_state.document_summary = ""

                    st.success("PDFs processed successfully!")

                    st.write("Uploaded files:")
                    for pdf in pdf_docs:
                        st.write(f"✅ {pdf.name}")
        else:
            st.warning("Please upload at least one PDF.")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared.")


st.subheader("📌 Quick Question Suggestions")

suggestions = [
    "Summarize this document",
    "List important topics from this document",
    "Explain this concept simply",
    "Give 5 exam questions from this document"
]

cols = st.columns(2)

selected_question = None

for index, suggestion in enumerate(suggestions):
    with cols[index % 2]:
        if st.button(suggestion):
            selected_question = suggestion


st.subheader("📝 Document Summary")

if st.button("Summarize Uploaded PDFs"):
    if st.session_state.text_chunks:
        with st.spinner("Generating summary..."):
            st.session_state.document_summary = summarize_documents(
                st.session_state.text_chunks
            )
    else:
        st.warning("Please upload and process PDFs first.")

if st.session_state.document_summary:
    st.write(st.session_state.document_summary)


st.subheader("💬 Ask Questions")

typed_question = st.chat_input("Ask a question from your uploaded PDFs...")

question = selected_question if selected_question else typed_question

if question:
    if st.session_state.text_chunks:
        context, sources = retrieve_relevant_chunks(
            question,
            st.session_state.vector_store
        )

        answer = get_answer(
            question,
            context,
            st.session_state.chat_history
        )

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
            "sources": sources
        })
    else:
        st.warning("Please upload and process PDFs first.")


for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

        if chat["sources"]:
            st.caption("Sources: " + ", ".join(chat["sources"]))