def build_context(docs):
    context_parts = []
    sources = []

    for doc in docs:
        file_name = doc.metadata.get("file_name", "Unknown file")
        page = doc.metadata.get("page", "Unknown page")
        content_type = doc.metadata.get("content_type", "text")
        source = f"{file_name} - Page {page} ({content_type})"

        context_parts.append(f"Source: {source}\n{doc.page_content}")
        if source not in sources:
            sources.append(source)

    return "\n\n---\n\n".join(context_parts), sources


def build_prompt(question: str, rewritten_query: str, context: str, chat_history: list) -> dict:
    history = "\n".join(
        [f"User: {chat['question']}\nAssistant: {chat['answer']}" for chat in chat_history[-2:]]
    )

    template = """
You are a helpful academic RAG assistant.
Use only the retrieved context to answer.
If the answer is not present in the context, say:
"The answer is not available in the stored documents."

Rules:
1. Give a clear student-friendly explanation.
2. Use headings and simple language.
3. Mention sources at the end.
4. Do not hallucinate.
5. If tables are present, explain them clearly.
6. If image placeholders are present, say image understanding needs OCR/Gemini Vision unless a description is provided.

Previous conversation:
{history}

Original question:
{question}

Rewritten retrieval query:
{rewritten_query}

Retrieved context:
{context}

Answer:
"""

    return {
        "template": template,
        "values": {
            "history": history,
            "question": question,
            "rewritten_query": rewritten_query,
            "context": context
        }
    }
