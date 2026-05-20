from rag.vector_store import get_vector_store

db = get_vector_store()

query = "From AI.pdf, what is LLM?"

docs = db.similarity_search(query, k=5)

for i, doc in enumerate(docs, start=1):
    print("\n====================")
    print("Result", i)
    print("Metadata:", doc.metadata)
    print("Content:")
    print(doc.page_content[:800])