import pytest

import library_service as ls
import datetime
import database as db

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
    success, message = ls.return_book_by_patron("999999", 2)
    
    assert success == False
    assert "book not found" in message.lower()

def test_return_book_invalid_patron():
    """Test returning a book with non-existant patron."""
    success, message = ls.return_book_by_patron("000000", 3)
    
    assert success == False
    assert "book not found" in message.lower()

def test_return_book_invalid_book_id():
    """Test returning a book with non-existent book id."""
    success, message = ls.return_book_by_patron("345678", 999)
    
    assert success == False
    assert "book not found" in message.lower()

def test_return_book_no_patron_id():
    """Test returning a book with no patron id."""
    success, message = ls.return_book_by_patron(" ", 4)
    
    assert success == False
    assert "invalid patron" in message.lower()

def test_return_book_no_book_id():
    """Test returning a book with no book id."""
    success, message = ls.return_book_by_patron("567890", None)
    
    assert success == False
    assert "invalid book" in message.lower()