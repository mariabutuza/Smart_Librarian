from pydantic import BaseModel, Field
from typing import List


class Book(BaseModel):
    """
    Represents a book stored in the local knowledge base.
    """

    id: int = Field(..., description="Unique identifier of the book.")

    title: str = Field(..., description="Book title.")

    author: str = Field(..., description="Book author.")

    publication_year: int = Field(
        ...,
        description="Year when the book was first published."
    )

    genres: List[str] = Field(
        ...,
        description="Book genres."
    )

    themes: List[str] = Field(
        ...,
        description="Main themes covered by the book."
    )

    keywords: List[str] = Field(
        ...,
        description="Keywords used to improve semantic search."
    )

    short_summary: str = Field(
        ...,
        description="Short summary used for embeddings and retrieval."
    )

    full_summary: str = Field(
        ...,
        description="Complete summary returned by the tool."
    )