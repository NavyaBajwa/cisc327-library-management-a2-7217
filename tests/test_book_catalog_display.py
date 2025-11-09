import pytest
from database import get_all_books

from database import init_database, reset_database, add_sample_data

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_database()
    reset_database()
    add_sample_data()

def test_catalog_structure():
    catalog = get_all_books()

    if catalog:  
        book = catalog[0]

        assert "id" in book
        assert "title" in book
        assert "author" in book
        assert "isbn" in book
        assert "available_copies" in book
        assert "total_copies" in book

def test_catalog_types():
    catalog = get_all_books()

    if catalog:  
        book = catalog[0]

        assert isinstance(book["id"], int)
        assert isinstance(book["title"], str)
        assert isinstance(book["author"], str)
        assert isinstance(book["isbn"], str)
        assert isinstance(book["available_copies"], int)
        assert isinstance(book["total_copies"], int)

def test_book_availibility_structure():
    catalog = get_all_books()
    for book in catalog:
        assert 0 <= book["available_copies"] <= book["total_copies"]





