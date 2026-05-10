import streamlit as st
from dotenv import load_dotenv
import os

from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

st.set_page_config(page_title="AI Academic Study Assistant", page_icon="📚")

st.title("📚 AI Academic Study Assistant using RAG")
st.write("Upload your subject PDF and ask questions from it.")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_text(text)
    return [chunk for chunk in chunks if len(chunk.strip()) > 30]


def retrieve_relevant_chunks(question, chunks, top_k=4):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(chunks + [question])

    question_vector = vectors[-1]
    chunk_vectors = vectors[:-1]

    similarities = cosine_similarity(question_vector, chunk_vectors).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]

    relevant_chunks = [chunks[i] for i in top_indices]
    return "\n\n".join(relevant_chunks)


def get_answer(question, context):
    prompt_template = """
    Answer the question clearly using only the given context.
    If the answer is not available in the context, say:
    "The answer is not available in the uploaded document."

    Context:
    {context}

    Question:
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
        "context": context,
        "question": question
    })

    return response.content


if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = []


with st.sidebar:
    st.header("Upload Notes")

    pdf_docs = st.file_uploader(
        "Upload your PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process PDFs"):
        if pdf_docs:
            with st.spinner("Processing PDFs..."):
                raw_text = get_pdf_text(pdf_docs)

                if raw_text.strip() == "":
                    st.error("No text found in the uploaded PDF.")
                else:
                    st.session_state.text_chunks = get_text_chunks(raw_text)
                    st.success("PDFs processed successfully!")
        else:
            st.warning("Please upload at least one PDF.")


question = st.text_input("Ask a question from your uploaded PDF:")

if question:
    if st.session_state.text_chunks:
        context = retrieve_relevant_chunks(question, st.session_state.text_chunks)
        answer = get_answer(question, context)

        st.write("### Answer:")
        st.write(answer)
    else:
        st.warning("Please upload and process PDFs first.")