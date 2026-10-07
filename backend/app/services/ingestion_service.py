from chromadb import PersistentClient

from app.config import (
    CHROMA_COLLECTION,
    CHROMA_PATH,
)
from app.repositories.book_repository import BookRepository
from app.services.book_formatter import BookFormatter
from app.services.embedding_service import EmbeddingService


class IngestionService:
    """
    Service responsible for populating ChromaDB
    with the local book knowledge base.
    """

    def __init__(
        self,
        repository: BookRepository,
        embedding_service: EmbeddingService,
    ) -> None:
        """
        Initialize the ingestion service.
        """

        self._repository = repository
        self._embedding_service = embedding_service

        self._client = PersistentClient(
            path=str(CHROMA_PATH)
        )

        self._collection = (
            self._client.get_or_create_collection(
                name=CHROMA_COLLECTION
            )
        )

    def ingest_books(self) -> int:
        """
        Generate embeddings for all books and store them in ChromaDB.

        Returns
        -------
        int
            Number of books ingested.
        """

        books = self._repository.get_all_books()

        try:
            self._client.delete_collection(
                name=CHROMA_COLLECTION
            )
        except Exception:
            pass

        self._collection = (
            self._client.get_or_create_collection(
                name=CHROMA_COLLECTION
            )
        )

        ids: list[str] = []
        documents: list[str] = []
        embeddings: list[list[float]] = []
        metadatas: list[dict] = []

        for book in books:

            document = BookFormatter.to_embedding_text(book)

            embedding = (
                self._embedding_service
                .generate_embedding(document)
            )

            ids.append(str(book.id))

            documents.append(document)

            embeddings.append(embedding)

            metadatas.append(
                {
                    "title": book.title,
                    "author": book.author,
                    "genres": ", ".join(book.genres),
                    "themes": ", ".join(book.themes),
                }
            )

        self._collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(books)