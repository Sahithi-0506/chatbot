# config.py

PDF_DIR = "./data/pdfs"

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "academic_rag"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

RETRIEVAL_TOP_K = 8

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 3

GEMINI_MODEL = "gemini-2.5-flash"