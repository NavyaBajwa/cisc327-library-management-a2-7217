import pytest

from services.library_service import (
    borrow_book_by_patron, add_book_to_catalog, return_book_by_patron
)
import datetime
from database import get_book_by_isbn

from database import init_database, reset_database, add_sample_data

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_database()
    reset_database()
    add_sample_data()

'''
def test_return_book_valid(monkeypatch):
    """Test returning a book with valid input."""
    # Create a fake borrowed book
    fake_books = [{
        "book_id": 1,
        "title": "Book A",
        "author": "Author A",
        "borrow_date": datetime.datetime.now() - datetime.timedelta(days=5),
        "due_date": datetime.datetime.now() + datetime.timedelta(days=9),
        "return_date": None,
        "is_overdue": False
    }]
    # Mock the function that gets borrowed books
    monkeypatch.setattr(ls, "get_patron_borrowed_books", lambda patron_id: fake_books)
    
    # Mock the functions that update the database
    monkeypatch.setattr(ls, "update_borrow_record_return_date", lambda *args: True)
    monkeypatch.setattr(ls, "update_book_availability", lambda *args: True)

    success, message = ls.return_book_by_patron("123456", 1)
    
    assert success == True
    assert "successfully returned" in message.lower()
'''

def test_return_book_not_borrowed():
    """Test returning a book that the patron didn't withdraw."""
    add_book_to_catalog("boooook", "meeeeee", "7642678944427", 2)
    book = get_book_by_isbn("7642678944427")
    bookID = book["id"]
    borrow_book_by_patron("137865", bookID)

    add_book_to_catalog("book2", "me3", "6642678944427", 2)
    book2 = get_book_by_isbn("6642678944427")
    bookIDnotBorrowed = book2["id"]
    
    success, message = return_book_by_patron("137865", bookIDnotBorrowed)
    
    assert success == False
    assert "not currently borrowed" in message.lower()

def test_return_book_successful():
    add_book_to_catalog("book3", "author3", "5642648944427", 2)
    book = get_book_by_isbn("5642648944427")
    bookID = book["id"]
    borrow_book_by_patron("133865", bookID)    

    success, message = return_book_by_patron("133865", bookID)
    assert success == True
    assert "returned successfully" in message.lower()


def test_return_book_invalid_book_id():
    """Test returning a book with non-existent book id."""
    success, message = return_book_by_patron("345678", 999)
    
    assert success == False
    assert "book not found" in message.lower()

def test_return_book_no_patron_id():
    """Test returning a book with no patron id."""
    success, message = return_book_by_patron(" ", 4)
    
    assert success == False
    assert "invalid patron" in message.lower()

def test_return_book_no_book_id():
    """Test returning a book with no book id."""
    success, message = return_book_by_patron("567890", None)
    
    assert success == False
    assert "invalid book" in message.lower()

'''
def test_return_book_invalid_patron():
    """Test returning a book with non-existant patron."""
    success, message = ls.return_book_by_patron("000000", 3)
    
    assert success == False
    assert "book not found" in message.lower()
'''