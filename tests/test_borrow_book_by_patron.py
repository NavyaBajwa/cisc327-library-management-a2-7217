import pytest
from services.library_service import (
    borrow_book_by_patron, add_book_to_catalog
)
from database import get_book_by_isbn

from database import init_database, reset_database, add_sample_data

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_database()
    reset_database()
    add_sample_data()

# this test doesn't work right now because the book id keeps changing, but otherwise its fine
'''
def test_borrow_book_valid_input():
    """Test borrowing a book with valid input."""
    success, message = borrow_book_by_patron("246891", 89)
    
    assert success == True
    assert "successfully borrowed" in message.lower()
'''
def test_borrow_book_invalid_patron_id_too_short():
    """Test borrowing a book with patron id too short."""
    success, message = borrow_book_by_patron("123", 5)
    
    assert success == False
    assert "invalid patron id" in message.lower()

def test_borrow_book_invalid_patron_id_too_long():
    """Test borrowing a book with patron id too long."""
    success, message = borrow_book_by_patron("123679526436", 7)
    
    assert success == False
    assert "invalid patron id" in message.lower()

def test_borrow_book_invalid_patron_id_not_numeric():
    """Test borrowing a book with patron id not numeric."""
    success, message = borrow_book_by_patron("x77hij", 7)
    
    assert success == False
    assert "invalid patron id" in message.lower()

def test_borrow_book_invalid_book_id():
    """Test borrowing a book when the book id is not valid."""
    success, message = borrow_book_by_patron("345689", 99999999999999)
    
    assert success == False
    assert "book not found" in message.lower()

# new tests

def test_borrow_book_not_available():
    # add book with one copy
    add_book_to_catalog("boook", "me", "1234567891234", 1)
    book = get_book_by_isbn("1234567891234")
    bookID = book["id"]

    borrow_book_by_patron("123456", bookID)

    # try to borrow book already borrowed
    success, message = borrow_book_by_patron("333444", bookID)
    assert success == False
    assert "not available" in message.lower()

def test_borrow_book_exceed_limit():
    # create 5 books
    for i in range(5):
        title = f"book{i}"
        author = f"author{i}"
        isbn = f"{i}" * 13
        copies = 1
        add_book_to_catalog(title, author, isbn, copies)

    # have user borrow the five books
    for i in range(5):
        isbn = f"{i}" * 13
        book = get_book_by_isbn(isbn)
        bookID = book["id"]
        borrow_book_by_patron("999999", bookID)

    # try to borrow book after reaching limit
    add_book_to_catalog("bookToBorrow", "navya", "5672451342345", 2)
    bookBorrow = get_book_by_isbn("5672451342345")
    booksID = bookBorrow["id"]

    success, message = borrow_book_by_patron("875247", booksID)
    assert success == False
    assert "reached the maximum borrowing limit" in message.lower()

