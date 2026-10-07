from app.repositories.book_repository import BookRepository


class SummaryTool:
    """
    Tool responsible for retrieving the full summary
    of a book by its title.
    """

    def __init__(
        self,
        repository: BookRepository,
    ) -> None:
        """
        Initialize the summary tool.

        Parameters
        ----------
        repository : BookRepository
            Repository used to access the local knowledge base.
        """

        self._repository = repository

    def get_summary_by_title(self, title: str) -> str:
        """
        Retrieve the complete summary of a book.

        Parameters
        ----------
        title : str
            Book title.

        Returns
        -------
        str
            Full book summary.

        Raises
        ------
        ValueError
            If the requested book does not exist.
        """

        book = self._repository.get_book_by_title(title)

        if book is None:
            raise ValueError(
                f'Book "{title}" was not found.'
            )

        return book.full_summary