import pytest
from library_service import (
    add_book_to_catalog
)
from database import reset_database, add_sample_data

reset_database()
add_sample_data()

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message

# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.
"""My tests"""

def test_add_book_invalid_title_too_short():
    """Test adding a book with title is too short."""
    success, message = add_book_to_catalog("", "Navya", "1234567881123", 3)

    assert success == False
    assert "Title too short, should be more than 0 less than 200 chars" in message

def test_add_book_invalid_title_too_long():
    """Test adding a book with title is too long."""
    """Title has 208 characters"""
    success, message = add_book_to_catalog("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", "Test Author", "2224567881123", 3)

    assert success == False
    assert "Title too long, should be less than 200 chars" in message

def test_add_book_invalid_author_too_long():
    """Test adding a book with title is too long."""
    """Author has 208 characters"""

    success, message = add_book_to_catalog("Percy Jackson", "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", "1234567881123", 3)

    assert success == False
    assert "Author too long, should be less than 100" in message

def test_add_book_invalid_author_too_short():
    """Test adding a book with author too short."""

    success, message = add_book_to_catalog("Harry Potter", "", "1234567881123", 3)

    assert success == False
    assert "Author too short, should be between 0 and 100 chars" in message

def test_add_book_invalid_isbn_too_long():
    """Test adding a book with isbn too long."""

    success, message = add_book_to_catalog("Schoolbox", "Rick Riordan", "123456788111222323786253", 3)

    assert success == False
    assert "ISBN too long, should be exactly 13 digits" in message

def test_add_book_invalid_isbn_not_digits():
    """Test adding a book with isbn too long."""

    success, message = add_book_to_catalog("Lunch Meat", "Earnest Hemingway", "abcdefghijklm", 4)

    assert success == False
    assert "ISBN is not numeric, should be numeric" in message

def test_add_book_invalid_total_copies_negative():
    """Test adding a book with total copies is negative int."""

    success, message = add_book_to_catalog("Jump Rope", "Brick", "1234567897853", -3)

    assert success == False
    assert "total copies is negative, should be positive integer" in message

def test_add_book_invalid_total_copies_null():
    """Test adding a book with total copies is 0"""

    success, message = add_book_to_catalog("DumbBum", "HumBum", "1234567897853", 0)

    assert success == False
    assert "total copies is zero, should be positive integer" in message

def test_add_book_valid_max_title_length():
    """Test adding a book with title length of 200 chars"""

    success, message = add_book_to_catalog("a"*200, "West", "1234564497853", 2)

    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_valid_max_author_length():
    """Test adding a book with author length of 100 chars"""

    success, message = add_book_to_catalog("Best", "b"*100, "1234567398843", 2)

    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_valid_min_total_copies():
    """Test adding a book with 1 total copy"""

    success, message = add_book_to_catalog(" Title", "Writer", "1234567897853", 1)

    assert success == True
    assert "successfully added" in message.lower()



