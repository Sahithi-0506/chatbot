from functools import lru_cache
from typing import List
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from config import RERANKER_MODEL, RERANK_TOP_K


@lru_cache(maxsize=1)
def get_reranker():
    return CrossEncoder(RERANKER_MODEL)


def rerank_documents(query: str, docs: List[Document], top_k: int = RERANK_TOP_K) -> List[Document]:
    if not docs:
        return []

    pairs = [(query, doc.page_content) for doc in docs]
    scores = get_reranker().predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda item: item[1], reverse=True)
    reranked_docs = []
    for doc, score in ranked[:top_k]:
        doc.metadata["rerank_score"] = float(score)
        reranked_docs.append(doc)
    return reranked_docs
