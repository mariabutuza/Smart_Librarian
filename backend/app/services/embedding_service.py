from openai import OpenAI

from app.config import (
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
)


class EmbeddingService:
    """
    Service responsible for generating vector embeddings
    using the OpenAI Embeddings API.
    """

    def __init__(self) -> None:
        """
        Initialize the OpenAI client.
        """

        self._client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the provided text.

        Parameters
        ----------
        text : str
            Input text to embed.

        Returns
        -------
        list[float]
            Embedding vector.
        """

        response = self._client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        )

        return response.data[0].embedding