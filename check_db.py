from rag.vector_store import get_vector_store

db = get_vector_store()

data = db.get(include=["metadatas"])

files = {}

for meta in data["metadatas"]:
    file_name = meta.get("file_name", "unknown")
    files[file_name] = files.get(file_name, 0) + 1

print("Stored chunks by PDF:")
for file_name, count in files.items():
    print(file_name, ":", count)