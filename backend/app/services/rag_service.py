from chromadb import PersistentClient

from app.config import (
    CHROMA_COLLECTION,
    CHROMA_PATH,
)
from app.services.embedding_service import EmbeddingService


class RagService:
    """
    Service responsible for retrieving relevant book documents
    from ChromaDB using semantic similarity search.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        """
        Initialize the RAG retrieval service.

        Parameters
        ----------
        embedding_service : EmbeddingService
            Service used to generate embeddings for user queries.
        """

        self._embedding_service = embedding_service

        self._client = PersistentClient(
            path=str(CHROMA_PATH)
        )

        self._collection = self._client.get_or_create_collection(
            name=CHROMA_COLLECTION
        )

    def search(
        self,
        query: str,
        n_results: int = 3,
    ) -> list[str]:
        """
        Retrieve the most semantically relevant book documents.

        Parameters
        ----------
        query : str
            User question or book preference.

        n_results : int
            Maximum number of documents to retrieve.

        Returns
        -------
        list[str]
            Relevant book documents ordered by semantic similarity.
        """

        normalized_query = query.strip()

        if not normalized_query:
            raise ValueError("Search query cannot be empty.")

        if n_results <= 0:
            raise ValueError("n_results must be greater than zero.")

        collection_size = self._collection.count()

        if collection_size == 0:
            return []

        result_limit = min(n_results, collection_size)

        query_embedding = (
            self._embedding_service
            .generate_embedding(normalized_query)
        )

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=result_limit,
            include=["documents"],
        )

        document_groups = results.get("documents")

        if not document_groups or not document_groups[0]:
            return []

        return [
            document
            for document in document_groups[0]
            if document is not None
        ]