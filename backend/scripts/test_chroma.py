from chromadb import PersistentClient
from pathlib import Path

db_path = (
    Path(__file__).resolve().parent.parent
    / "app"
    / "vector_store"
    / "chroma_db"
)

client = PersistentClient(path=str(db_path))

collection = client.get_or_create_collection("books")

print("ChromaDB connected successfully!")
print(collection.count())