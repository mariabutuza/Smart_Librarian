from app.models.book import Book


class BookFormatter:
    """
    Format Book objects for embedding generation.
    """

    @staticmethod
    def to_embedding_text(book: Book) -> str:
        """
        Convert a Book object into a structured text
        suitable for semantic embeddings.
        """

        genres = ", ".join(book.genres)
        themes = ", ".join(book.themes)
        keywords = ", ".join(book.keywords)

        return f"""
Title: {book.title}

Author: {book.author}

Genres: {genres}

Themes: {themes}

Keywords: {keywords}

Summary:
{book.short_summary}
""".strip()