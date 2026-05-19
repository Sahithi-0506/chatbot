import shutil
from langchain_chroma import Chroma

from config import CHROMA_PATH, COLLECTION_NAME
from rag.embeddings import get_embedding_function


def get_chroma_db():
    embedding_function = get_embedding_function()

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

    return db


def add_documents_to_chroma(documents, batch_size=1000):
    db = get_chroma_db()

    total = len(documents)

    for i in range(0, total, batch_size):
        batch = documents[i:i + batch_size]
        db.add_documents(batch)
        print(f"Added batch {i // batch_size + 1}: {len(batch)} documents")

    print(f"All {total} documents added to ChromaDB successfully.")


def reset_chroma_collection():
    shutil.rmtree(CHROMA_PATH, ignore_errors=True)

    print("ChromaDB reset successfully.")


def get_vector_store():
    return get_chroma_db()