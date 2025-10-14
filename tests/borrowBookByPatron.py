import pytest
from library_service import (
    borrow_book_by_patron
)

def test_borrow_book_valid_input():
    """Test borrowing a book with valid input."""
    success, message = borrow_book_by_patron("246891", 6)
    
    assert success == True
    assert "successfully borrowed" in message.lower()

def test_borrow_book_invalid_patron_id_too_short():
    """Test borrowing a book with patron id too short."""
    success, message = borrow_book_by_patron("123", 5)
    
    assert success == False
    assert "invalid patron id" in message

def test_borrow_book_invalid_patron_id_too_long():
    """Test borrowing a book with patron id too long."""
    success, message = borrow_book_by_patron("123679526436", 7)
    
    assert success == False
    assert "invalid patron id" in message

def test_borrow_book_invalid_patron_id_not_numeric():
    """Test borrowing a book with patron id not numeric."""
    success, message = borrow_book_by_patron("x77hij", 7)
    
    assert success == False
    assert "invalid patron id" in message

def test_borrow_book_invalid_too_many_withdrawn():
    """Test borrowing a book when patron has already withdrawn 5."""
    success, message = borrow_book_by_patron("123456", 6)
    
    assert success == False
    assert "maximum borrowing limit" in message

def test_borrow_book_invalid_book_id():
    """Test borrowing a book when the book id is not valid."""
    success, message = borrow_book_by_patron("345689", 99999999999999)
    
    assert success == False
    assert "book not found" in message

