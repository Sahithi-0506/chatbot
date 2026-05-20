from config import RETRIEVAL_TOP_K
from rag.vector_store import get_vector_store


def retrieve_documents(query, selected_pdf="All PDFs"):
    db = get_vector_store()

    if selected_pdf and selected_pdf != "All PDFs":
        docs = db.similarity_search(
            query,
            k=RETRIEVAL_TOP_K,
            filter={"file_name": selected_pdf}
        )
    else:
        docs = db.similarity_search(
            query,
            k=RETRIEVAL_TOP_K
        )

    return docs