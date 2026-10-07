import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.repositories.book_repository import BookRepository
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService


def main() -> None:
    """
    Populate ChromaDB with all books from the local knowledge base.
    """

    repository = BookRepository()

    embedding_service = EmbeddingService()

    ingestion_service = IngestionService(
        repository=repository,
        embedding_service=embedding_service,
    )

    count = ingestion_service.ingest_books()

    print(f"Successfully ingested {count} books into ChromaDB.")


if __name__ == "__main__":
    main()
