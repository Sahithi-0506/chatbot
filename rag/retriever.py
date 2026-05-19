from config import RETRIEVAL_TOP_K
from rag.vector_store import get_vector_store


def retrieve_documents(query: str, top_k: int = RETRIEVAL_TOP_K):
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=top_k)
