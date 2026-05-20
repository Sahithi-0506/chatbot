from rag.query_rewriter import rewrite_query
from rag.retriever import retrieve_documents
from rag.reranker import rerank_documents
from rag.prompt_builder import build_context, build_prompt
from rag.generator import generate_answer


def answer_question(question: str, chat_history: list, selected_pdf: str = "All PDFs"):
    rewritten_query = rewrite_query(question, chat_history)

    retrieved_docs = retrieve_documents(
        rewritten_query,
        selected_pdf
    )

    reranked_docs = rerank_documents(
        rewritten_query,
        retrieved_docs
    )

    context, sources = build_context(reranked_docs)

    prompt_data = build_prompt(
        question,
        rewritten_query,
        context,
        chat_history
    )

    answer = generate_answer(prompt_data)

    return {
        "answer": answer,
        "sources": sources,
        "rewritten_query": rewritten_query,
        "selected_pdf": selected_pdf
    }