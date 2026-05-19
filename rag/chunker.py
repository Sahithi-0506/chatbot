from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []
    for doc in documents:
        split_docs = splitter.split_documents([doc])
        for index, chunk in enumerate(split_docs, start=1):
            if len(chunk.page_content.strip()) > 30:
                chunk.metadata["chunk_id"] = index
                chunks.append(chunk)
    return chunks
