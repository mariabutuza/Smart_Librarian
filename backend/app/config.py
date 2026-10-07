import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHAT_MODEL = os.getenv(
    "CHAT_MODEL",
    "gpt-5.5"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small"
)

IMAGE_MODEL = os.getenv(
    "IMAGE_MODEL",
    "gpt-image-2"
)

CHROMA_COLLECTION = os.getenv(
    "CHROMA_COLLECTION",
    "books"
)

CHROMA_PATH = BASE_DIR / "vector_store" / "chroma_db"
