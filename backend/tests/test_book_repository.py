from app.repositories.book_repository import BookRepository


def test_book_repository_loads_and_normalizes_titles():
    repository = BookRepository()
    first_book = repository.get_all_books()[0]

    assert repository.get_all_books()
    assert repository.get_book_by_title(f"  {first_book.title.upper()}  ") == first_book
    assert repository.get_book_by_title("Unknown book") is None
