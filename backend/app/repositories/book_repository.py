import json
from pathlib import Path

from app.models.book import Book


class BookRepository:
    """
    Repository responsible for loading and providing access
    to the local book knowledge base.
    """

    def __init__(self, json_path: Path | None = None):
        """
        Initialize the repository.

        Parameters
        ----------
        json_path : Path | None
            Optional custom path to the JSON knowledge base.
            If not provided, the default project path is used.
        """

        if json_path is None:
            json_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "book_summaries.json"
            )

        self._json_path = json_path

        self._books: list[Book] = []
        self._books_by_title: dict[str, Book] = {}

        self._load_books()

    def _load_books(self) -> None:
        """
        Load all books from the JSON knowledge base.
        """

        if not self._json_path.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: {self._json_path}"
            )

        with self._json_path.open(
            mode="r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Knowledge base must contain a JSON array."
            )

        self._books = [
            Book(**book_data)
            for book_data in data
        ]

        self._books_by_title = {
            self._normalize_title(book.title): book
            for book in self._books
        }

    @staticmethod
    def _normalize_title(title: str) -> str:
        """
        Normalize a title for case-insensitive lookups.
        """

        return " ".join(title.strip().lower().split())

    def get_all_books(self) -> list[Book]:
        """
        Return all books from the knowledge base.
        """

        return self._books

    def get_book_by_title(self, title: str) -> Book | None:
        """
        Retrieve a book by its title.

        Parameters
        ----------
        title : str
            Book title.

        Returns
        -------
        Book | None
            Matching book or None if not found.
        """

        normalized_title = self._normalize_title(title)

        return self._books_by_title.get(normalized_title)