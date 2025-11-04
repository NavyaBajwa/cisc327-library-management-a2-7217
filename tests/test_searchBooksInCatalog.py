import pytest
from services.library_service import (
    search_books_in_catalog
)

def test_search_book_partial_title():
    """Test searching for a book with a partial title"""
    bookList = search_books_in_catalog("Pride", "title") or []

    # check that each book in the list has "Pride" in the title
    for book in bookList:
        assert "pride" in book['title'].lower()

def test_search_book_partial_author():
    """Test searching for a book with a partial author"""
    bookList = search_books_in_catalog("George", "author") or []

    for book in bookList:
        assert "george" in book['author'].lower()

def test_search_book_isbn():
    """Test searching for a book with a valid isbn"""

    bookList = search_books_in_catalog("9780451524935", "isbn") or []
    # check that the book has the correct isbn
    for book in bookList:
        assert "9780451524935" == book['isbn']

def test_search_book_that_doesnt_exist_title():
    """Test searching for a book with a valid isbn"""

    bookList = search_books_in_catalog("book does not exist", "title") or []
    # bookList should be empty because book doesn't exist
    assert bookList == []

def test_search_book_that_doesnt_exist_author():
    """Test searching for a book with a valid isbn"""

    bookList = search_books_in_catalog("book does not exist", "author") or []
    # bookList should be empty because book doesn't exist
    assert bookList == []

def test_search_book_with_empty_title_term():
    """Test searching for a book with empty title"""

    bookList = search_books_in_catalog("", "title") or []
    # check that the bookList is empty because no title searched
    assert bookList == []

def test_search_book_with_space_title():
    """Test searching for a book with empty title"""

    bookList = search_books_in_catalog(" ", "title") or []
    # check that the bookList is empty because we won't accept spaces as a search term
    assert bookList == [] 

def test_search_book_with_space_author():
    """Test searching for a book with empty title"""

    bookList = search_books_in_catalog(" ", "author") or []
    # check that the bookList is empty because we won't accept spaces as a search term
    assert bookList == [] 

def test_search_book_with_empty_author_term():
    """Test searching for a book with empty title"""

    bookList = search_books_in_catalog("", "author") or []
    # check that the bookList is empty bc no author searched
    assert bookList == []

def test_search_book_with_invalid_isbn_alpha():
    """Test searching for a book with invalid isbn"""

    bookList = search_books_in_catalog("abcdefghikjep", "isbn") or []
    # check that the bookList is empty bc isbn doesn't exist
    assert bookList == []

def test_search_book_with_invalid_isbn_numeric():
    """Test searching for a book with invalid isbn"""

    bookList = search_books_in_catalog("9999999999999", "isbn") or []
    # check that the bookList is empty bc isbn doesn't exist
    assert bookList == []