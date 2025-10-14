import pytest

from library_service import (
    return_book_by_patron,
    borrow_book_by_patron
)

def test_return_book_valid():
    """Test returning a book with valid input."""
    borrow_book_by_patron("123456", 1)
    success, message = return_book_by_patron("123456", 1)
    
    assert success == True
    assert "successfully returned" in message.lower()

def test_return_book_not_borrowed():
    """Test returning a book that the patron didn't withdraw."""
    success, message = return_book_by_patron("999999", 2)
    
    assert success == False
    assert "book not found" in message.lower()

def test_return_book_invalid_patron():
    """Test returning a book with non-existant patron."""
    success, message = return_book_by_patron("000000", 3)
    
    assert success == False
    assert "book not found" in message.lower()

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