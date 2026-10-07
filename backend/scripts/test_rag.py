from app.services.embedding_service import EmbeddingService
from app.services.rag_service import RagService


def main() -> None:
    """
    Test semantic retrieval from ChromaDB.
    """

    embedding_service = EmbeddingService()

    rag_service = RagService(
        embedding_service=embedding_service
    )

    query = "Vreau o carte despre magie și prietenie."

    results = rag_service.search(
        query=query,
        n_results=3,
    )

    print(f"\nQuery: {query}\n")

    if not results:
        print("No relevant books were found.")
        return

    for index, document in enumerate(results, start=1):
        print(f"Result {index}")
        print(document)
        print("-" * 60)


if __name__ == "__main__":
    main()